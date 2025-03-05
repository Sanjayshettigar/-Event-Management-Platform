from app import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, cancelled, used
    qr_code = db.Column(db.String(200))
    
    # Relationships
    ticket_type = db.relationship('TicketType', backref='tickets')
    
    def __repr__(self):
        return f'<Ticket {self.id} for Event {self.event_id}>'
