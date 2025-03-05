from app import db
from datetime import datetime

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # catering, decoration, photography, etc.
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20))
    rating = db.Column(db.Float, default=0.0)
    price_range = db.Column(db.String(20))  # $, $$, $$$
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assignments = db.relationship('VendorAssignment', backref='vendor', lazy=True)
    reviews = db.relationship('VendorReview', backref='vendor', lazy=True)
    
    def __repr__(self):
        return f'<Vendor {self.name}>'

class VendorAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    service_details = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed
    contract_file = db.Column(db.String(200))
    price = db.Column(db.Float)
    
    def __repr__(self):
        return f'<VendorAssignment {self.vendor_id} - {self.event_id}>'

class VendorReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VendorReview {self.vendor_id} - {self.rating}>'
