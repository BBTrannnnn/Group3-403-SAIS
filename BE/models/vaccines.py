from models import db

class Vaccine(db.Model):
    __tablename__ = 'vaccines'
    
    id_vaccines = db.Column(db.Integer, primary_key=True)  # phải đúng tên này!
    name = db.Column(db.Unicode(100), nullable=False)
    description = db.Column(db.Unicode(100), nullable=True)
    manufacturer = db.Column(db.Unicode(100), nullable=True)
    efficacy = db.Column(db.Float, nullable=True)
    side_effects = db.Column(db.Unicode(100), nullable=True)
    category = db.Column(db.Unicode(50), nullable=False, default='Bắt buộc')
    quantity = db.Column(db.Integer, nullable=False, default=1)

    appointments = db.relationship('Appointment', backref='vaccine', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Vaccine {self.name}>'