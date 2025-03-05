import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.event import EventCategory

def init_categories():
    categories = [
        ('Conference', 'Professional gatherings and conferences'),
        ('Workshop', 'Interactive learning and skill-building sessions'),
        ('Seminar', 'Educational presentations and discussions'),
        ('Networking', 'Social and professional networking events'),
        ('Concert', 'Musical performances and entertainment'),
        ('Exhibition', 'Art, culture, and showcase events'),
        ('Sports', 'Athletic events and competitions'),
        ('Corporate', 'Business and corporate events'),
        ('Social', 'Community and social gatherings'),
        ('Other', 'Other event types')
    ]
    
    for name, description in categories:
        if not EventCategory.query.filter_by(name=name).first():
            category = EventCategory(name=name, description=description)
            db.session.add(category)
    
    db.session.commit()
    print("Categories initialized successfully!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_categories()
