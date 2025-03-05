from app import db
from datetime import datetime
from app.models.ticket import Ticket
from app.models.task import Task

class EventCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published, cancelled, completed
    category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    banner_image = db.Column(db.String(200))  # URL to the banner image
    
    # Analytics fields
    views_count = db.Column(db.Integer, default=0)
    registration_count = db.Column(db.Integer, default=0)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='event', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='event', lazy=True, cascade='all, delete-orphan')
    registrations = db.relationship('Registration', backref='event', lazy=True)
    ticket_types = db.relationship('TicketType', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'

    def get_ticket_stats(self):
        stats = {
            'total_tickets': sum(ticket_type.quantity for ticket_type in self.ticket_types),
            'tickets_sold': sum(ticket_type.tickets_sold for ticket_type in self.ticket_types),
            'revenue': sum(ticket_type.revenue for ticket_type in self.ticket_types)
        }
        return stats

class TicketType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<TicketType {self.name}>'

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled
    attended = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Registration {self.id}>'
