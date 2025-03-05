from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='organizer', lazy=True)

class EventCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=1))
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
    banner_image = db.Column(db.String(200))
    views_count = db.Column(db.Integer, default=0)
    registration_count = db.Column(db.Integer, default=0)
    
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=False, default=1)
    
    ticket_types = db.relationship('TicketType', backref='event', lazy=True)

class TicketType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0.0)
    
    tickets = db.relationship('Ticket', backref='ticket_type', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # e.g., 'valid', 'used', 'cancelled'
