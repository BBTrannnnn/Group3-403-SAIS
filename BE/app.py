from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from routes.customer_router import customer_bp  # Route quản lý khách hàng
from datetime import datetime
from models.customer import Customer, db
from models.vaccines import db, Vaccine
from routes.vaccines_router import vaccines_bp  # Route quản lý vaccine
from models.appointment import Appointment,db  # Import model Appointment
from routes.appointment_router import appointment_bp  # Route quản lý lịch hẹn


app = Flask(__name__)
# Cấu hình ứng dụng
app.config.from_object(Config)  

# Khởi tạo CSDL
db.init_app(app)
CORS(app)

# Đăng ký blueprint cho vaccine
app.register_blueprint(vaccines_bp, url_prefix='/api/vaccines')
# Đăng ký blueprint cho khách hàng
app.register_blueprint(customer_bp, url_prefix='/api/customers')
# Đăng ký blueprint cho lịch hẹn
app.register_blueprint(appointment_bp, url_prefix='/api/appointments')

# Tạo bảng nếu chưa có
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
