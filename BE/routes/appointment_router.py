from flask import Blueprint, request, jsonify
from models import db
from models.appointment import Appointment
from models.customer import Customer
from models.vaccines import Vaccine
from datetime import datetime

appointment_bp = Blueprint('appointments', __name__)


@appointment_bp.route('/', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id_appointment': a.id_appointment,
        'scheduled_date': a.scheduled_date.strftime('%Y-%m-%d'),
        'time_slot': a.time_slot,
        'location': a.location,
        'id_customer': a.id_customer,
        'id_vaccine': a.id_vaccine,
        'dose_number': a.dose_number
    } for a in appointments]), 200


@appointment_bp.route('/', methods=['POST'])
def register_appointment():
    data = request.get_json()

    if not data:
        return jsonify({'Lỗi': 'Phải cung cấp dữ liệu JSON'}), 400
    
    scheduled_date = data.get('scheduled_date')
    time_slot = data.get('time_slot')
    location = data.get('location')
    id_customer = data.get('id_customer')
    id_vaccine = data.get('id_vaccine')
    dose_number = data.get('dose_number')  # Mũi 1, Mũi 2, Mũi nhắc lại

    # Kiểm tra bắt buộc
    if not all([scheduled_date, time_slot, location, id_customer, id_vaccine, dose_number  ]):
        return jsonify({'Lỗi': 'Thiếu thông tin bắt buộc'}), 400

    try:
        # Định dạng ngày
        scheduled_date_obj = datetime.strptime(scheduled_date, '%Y-%m-%d').date()

        # Kiểm tra khách hàng và vaccine có tồn tại không
        customer = Customer.query.get(id_customer)
        vaccine = Vaccine.query.get(id_vaccine)

        if not customer:
            return jsonify({'Lỗi': 'Khách hàng không tồn tại'}), 404
        if not vaccine:
            return jsonify({'Lỗi': 'Vaccine không tồn tại'}), 404

        # Tạo lịch hẹn
        appointment = Appointment(
            scheduled_date=scheduled_date_obj,
            time_slot=time_slot,
            location=location,
            id_customer=id_customer,
            id_vaccine=id_vaccine,
            dose_number=dose_number
        )
        db.session.add(appointment)
        db.session.commit()

        customer = db.session.get(Customer, id_customer)
        vaccine = db.session.get(Vaccine, id_vaccine)
        return jsonify({
            'message': 'Đăng ký lịch tiêm thành công',
            'appointment': {
                'date': scheduled_date,
                'time_slot': time_slot,
                'location': location,
                'customer': customer.customer_name,
                'vaccine': vaccine.name,
                'dose': dose_number
            }
        }), 201

    except ValueError:
        return jsonify({'Lỗi': 'Định dạng ngày phải là YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi đăng ký: {str(e)}'}), 500
    

@appointment_bp.route('/<int:id>', methods=['PUT'])
def update_appointment(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Yêu cầu gửi dữ liệu JSON'}), 400

    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Không tìm thấy lịch tiêm với ID này'}), 404

    # Cập nhật từng trường nếu có
    try:
        if 'scheduled_date' in data:
            appointment.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        if 'time_slot' in data:
            appointment.time_slot = data['time_slot']
        if 'location' in data:
            appointment.location = data['location']
        if 'dose_number' in data:
            appointment.dose_number = data['dose_number']
        if 'id_customer' in data:
            appointment.id_customer = data['id_customer']
        if 'id_vaccine' in data:
            appointment.id_vaccine = data['id_vaccine']

        db.session.commit()
        return jsonify({'Thông báo': 'Cập nhật lịch tiêm thành công'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi cập nhật lịch tiêm: {str(e)}'}), 500

@appointment_bp.route('/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'Lỗi': 'Không tìm thấy lịch tiêm với ID này'}), 404

    try:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'Thông báo': 'Xóa lịch tiêm thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Lỗi': f'Lỗi khi xóa lịch tiêm: {str(e)}'}), 500
