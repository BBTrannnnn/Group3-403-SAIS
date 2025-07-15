from models import db
from datetime import datetime


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id_appointment = db.Column(db.Integer, primary_key=True)
    scheduled_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.Unicode(50), nullable=False)
    location = db.Column(db.Unicode(255), nullable=False)

    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id_customer'), nullable=False)
    id_vaccine = db.Column(db.Integer, db.ForeignKey('vaccines.id_vaccines'), nullable=False)
    dose_number = db.Column(db.Unicode(20), nullable=False)  # Mũi 1, Mũi 2, Nhắc lại
    status = db.Column(db.Unicode(255), default='Chờ duyệt')
    def __repr__(self):
        return f'<Appointment {self.id_appointment} for Customer {self.id_customer}>'
class AppointmentBackup(db.Model):
    __bind_key__ = 'backup'
    __tablename__ = 'appointments_backup'

    id_appointment = db.Column(db.Integer, primary_key=True)
    scheduled_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.Unicode(50), nullable=False)
    location = db.Column(db.Unicode(255), nullable=False)

    id_customer = db.Column(db.Integer, db.ForeignKey('customers_backup.id_customer'), nullable=False)
    id_vaccine = db.Column(db.Integer, db.ForeignKey('vaccines_backup.id_vaccines'), nullable=False)
    dose_number = db.Column(db.Unicode(20), nullable=False)  # Mũi 1, Mũi 2, Nhắc lại
    status = db.Column(db.Unicode(255), default='Chờ duyệt')
    
    def __repr__(self):
        return f'<AppointmentBackup {self.id_appointment} for Customer {self.id_customer}>'