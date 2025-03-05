from app import create_app, db
from app.models import EventCategory

def add_default_categories():
    categories = [
        ('General', 'General events and gatherings'),
        ('Conference', 'Professional and academic conferences'),
        ('Workshop', 'Interactive learning sessions'),
        ('Seminar', 'Educational presentations and discussions'),
        ('Concert', 'Musical performances and shows'),
        ('Exhibition', 'Art, technology, and cultural exhibitions'),
        ('Sports', 'Sporting events and competitions'),
        ('Social', 'Social gatherings and networking events')
    ]
    
    with create_app().app_context():
        for name, description in categories:
            if not EventCategory.query.filter_by(name=name).first():
                category = EventCategory(name=name, description=description)
                db.session.add(category)
        db.session.commit()
        print("Default categories added successfully!")

if __name__ == '__main__':
    add_default_categories()
