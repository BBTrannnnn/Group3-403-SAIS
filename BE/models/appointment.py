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
    def __repr__(self):
        return f'<Appointment {self.id_appointment} for Customer {self.id_customer}>'