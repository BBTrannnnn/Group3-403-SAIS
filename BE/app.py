from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

from routes.customer_router import customer_bp
from routes.vaccines_router import vaccines_bp
from routes.appointment_router import appointment_bp

from models.customer import db  # Đảm bảo chỉ khởi tạo db 1 lần ở đây

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# Đăng ký các blueprint
app.register_blueprint(vaccines_bp, url_prefix='/api/vaccines')

app.register_blueprint(customer_bp, url_prefix='/api/customers')

app.register_blueprint(appointment_bp, url_prefix='/api/appointments')

# ✅ Tạo bảng DB chính + DB phụ
with app.app_context():
    db.create_all()  # DB chính
    engine_backup = db.engines['backup']  # ✅ cú pháp mới thay vì get_engine
    db.metadata.create_all(bind=engine_backup)
    print("✅ Tạo bảng DB chính + DB phụ xong")
if __name__ == '__main__':
    app.run(debug=True)
