from models import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id_customer = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.Unicode(100), nullable=False)
    day_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.Unicode(10), nullable=False)  # 'Nam' hoặc 'Nữ'
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    cccd = db.Column(db.String(20), nullable=False, unique=True)  # lowercase tên cột để đồng bộ tốt hơn
    email = db.Column(db.String(100), nullable=True, unique=True)
    address = db.Column(db.Unicode(255), nullable=True)
    medical_history = db.Column(db.Unicode(255), nullable=True)
    vaccine_reaction_history = db.Column(db.Unicode(255), nullable=True)

    appointments = db.relationship('Appointment', backref='customer', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Customer {self.customer_name}>'
class CustomerBackup(db.Model):
    __bind_key__ = 'backup'
    __tablename__ = 'customers_backup'

    id_customer = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.Unicode(100), nullable=False)
    day_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.Unicode(10), nullable=False)  # 'Nam' hoặc 'Nữ'
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    cccd = db.Column(db.String(20), nullable=False, unique=True)  # lowercase tên cột để đồng bộ tốt hơn
    email = db.Column(db.String(100), nullable=True, unique=True)
    address = db.Column(db.Unicode(255), nullable=True)
    medical_history = db.Column(db.Unicode(255), nullable=True)
    vaccine_reaction_history = db.Column(db.Unicode(255), nullable=True)

    def __repr__(self):
        return f'<Customer {self.customer_name}>'