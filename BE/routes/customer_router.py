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
        return jsonify({'error': 'Yêu cầu phải gửi dữ liệu JSON hợp lệ'}), 400

    # Lấy dữ liệu từ JSON
    id_customer = data.get('id')
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
    if id_customer is None:
        return jsonify({'error': 'ID khách hàng là bắt buộc'}), 400
    if Customer.query.get(id_customer):
        return jsonify({'error': 'ID khách hàng đã tồn tại'}), 400
    if not customer_name:
        return jsonify({'error': 'Tên khách hàng là bắt buộc'}), 400
    if not day_of_birth:
        return jsonify({'error': 'Ngày sinh là bắt buộc'}), 400

    # Kiểm tra ngày sinh hợp lệ, không ở tương lai và >= 18 tuổi
    try:
        dob = datetime.strptime(day_of_birth, '%Y-%m-%d').date()
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if dob > today:
            return jsonify({'error': 'Ngày sinh không hợp lệ '}), 400
        if age < 18:
            return jsonify({'error': 'Khách hàng phải từ 18 tuổi trở lên để đăng ký'}), 400
    except ValueError:
        return jsonify({'error': 'Định dạng ngày sinh không hợp lệ. Dùng YYYY-MM-DD'}), 400
    if not sex:
        return jsonify({'error': 'Giới tính là bắt buộc'}), 400
    if not phone_number:
        return jsonify({'error': 'Số điện thoại là bắt buộc'}), 400
    if not isinstance(cccd, str) or not cccd.isdigit() or len(cccd) < 10:
        return jsonify({'error': 'Số căn cước là chuỗi số ít nhất 10 chữ số'}), 400
    if not isinstance(phone_number, str) or not phone_number.isdigit() or len(phone_number) < 10:
        return jsonify({'error': 'Số điện thoại phải là chuỗi số ít nhất 10 chữ số'}), 400
    if email and (not isinstance(email, str) or '@' not in email):
        return jsonify({'error': 'Email không hợp lệ'}), 400
    if address and not isinstance(address, str):
        return jsonify({'error': 'Địa chỉ phải là chuỗi ký tự'}), 400
    if medical_history and not isinstance(medical_history, str):
        return jsonify({'error': 'Tiền sử bệnh phải là chuỗi ký tự'}), 400
    if vaccine_reaction_history and not isinstance(vaccine_reaction_history, str):
        return jsonify({'error': 'Tiền sử phản ứng vaccine phải là chuỗi ký tự'}), 400
    try:
        customer = Customer(
            id_customer=id_customer,
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
        return jsonify({'message': 'Thêm khách hàng thành công'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi khi thêm khách hàng: {str(e)}'}), 500

