from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from routes.customer_router import customer_bp  # Route quản lý khách hàng
from datetime import datetime
from models.customer import Customer, db
from models.vaccines import db, Vaccine
from routes.vaccines_router import vaccines_bp  # Route quản lý vaccine

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

# Tạo bảng nếu chưa có
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
