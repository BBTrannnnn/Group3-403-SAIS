from flask import Blueprint, request, jsonify
from models.customer import Customer, db
from datetime import datetime
from sqlalchemy import func

customer_bp = Blueprint('customers', __name__)  
@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id_customer,
        'name': c.customer_name,
        'day_of_birth': c.day_of_birth.strftime('%Y-%m-%d'),
        'sex':c.sex,
        'phone_number': c.phone_number,
        'cccd': c.cccd,
        'email': c.email,
        'address': c.address,
        'medical_history': c.medical_history,
        'vaccine_reaction_history': c.vaccine_reaction_history
    } for c in customers]), 200
@customer_bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json()

    if not data:
        return jsonify({'Lỗi': 'Yêu cầu phải gửi dữ liệu JSON hợp lệ'}), 400

    # Lấy dữ liệu từ JSON

    customer_name = data.get('name')
    day_of_birth = data.get('day_of_birth')
    sex = data.get('sex')
    phone_number = data.get('phone_number')
    cccd = data.get('cccd')
    email = data.get('email')
    address = data.get('address')
    medical_history = data.get('medical_history')
    vaccine_reaction_history = data.get('vaccine_reaction_history')
    # Kiểm tra các trường bắt buộc

    if not customer_name:
        return jsonify({'Lỗi': 'Tên khách hàng là bắt buộc'}), 400
    if not day_of_birth:
        return jsonify({'Lỗi': 'Ngày sinh là bắt buộc'}), 400

    # Kiểm tra ngày sinh hợp lệ, không ở tương lai và >= 18 tuổi
    try:
        dob = datetime.strptime(day_of_birth, '%Y-%m-%d').date()
        today = datetime.today().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if dob > today:
            return jsonify({'Lỗi': 'Ngày sinh không hợp lệ '}), 400
        if age < 18:
            return jsonify({'Lỗi': 'Khách hàng phải từ 18 tuổi trở lên để đăng ký'}), 400
    except ValueError:
        return jsonify({'Lỗi': 'Định dạng ngày sinh không hợp lệ. Dùng YYYY-MM-DD'}), 400
    if not sex:
        return jsonify({'Lỗi': 'Giới tính là bắt buộc'}), 400
    if not phone_number:
        return jsonify({'Lỗi': 'Số điện thoại là bắt buộc'}), 400
    if not isinstance(cccd, str) or not cccd.isdigit() or len(cccd) < 10:
        return jsonify({'Lỗi': 'Số căn cước là chuỗi số ít nhất 10 chữ số'}), 400
    if not isinstance(phone_number, str) or not phone_number.isdigit() or len(phone_number) < 10:
        return jsonify({'Lỗi': 'Số điện thoại phải là chuỗi số ít nhất 10 chữ số'}), 400
    if email and (not isinstance(email, str) or '@' not in email):
        return jsonify({'Lỗi': 'Email không hợp lệ'}), 400
    if address and not isinstance(address, str):
        return jsonify({'Lỗi': 'Địa chỉ phải là chuỗi ký tự'}), 400
    if medical_history and not isinstance(medical_history, str):
        return jsonify({'Lỗi': 'Tiền sử bệnh phải là chuỗi ký tự'}), 400
    if vaccine_reaction_history and not isinstance(vaccine_reaction_history, str):
        return jsonify({'Lỗi': 'Tiền sử phản ứng vaccine phải là chuỗi ký tự'}), 400
    try:
        customer = Customer(
            customer_name=customer_name,
            day_of_birth=dob,
            sex=sex,
            phone_number=phone_number,
            cccd=cccd,
            email=email,
            address=address,
            medical_history=medical_history,
            vaccine_reaction_history=vaccine_reaction_history
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'Thông báo': 'Thêm khách hàng thành công'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi thêm khách hàng: {str(e)}'}), 500
    
@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()

    if not data:
        return jsonify({'Lỗi': 'Yêu cầu phải gửi dữ liệu JSON hợp lệ'}), 400  

    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'Lỗi': 'Không tìm thấy khách hàng với ID này'}), 404  

    try:
        customer.customer_name = data.get('name', customer.customer_name)
        if 'day_of_birth' in data:
            customer.day_of_birth = datetime.strptime(data['day_of_birth'], '%Y-%m-%d').date()
        customer.sex = data.get('sex', customer.sex)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        customer.cccd = data.get('cccd', customer.cccd)
        customer.email = data.get('email', customer.email)
        customer.address = data.get('address', customer.address)
        customer.medical_history = data.get('medical_history', customer.medical_history)
        customer.vaccine_reaction_history = data.get('vaccine_reaction_history', customer.vaccine_reaction_history)

        db.session.commit()
        return jsonify({'Thông báo': 'Cập nhật thông tin khách hàng thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi cập nhật: {str(e)}'}), 500
@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):    
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'Lỗi': 'Không tìm thấy khách hàng với ID này'}), 404  

    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'Thông báo': 'Xóa khách hàng thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi xóa khách hàng: {str(e)}'}), 500

