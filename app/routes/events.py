from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models.event import Event, EventCategory, TicketType, Registration
from app.models.task import Task
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

events = Blueprint('events', __name__, url_prefix='/events')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return os.path.join('uploads', filename)
    return None

@events.route('/')
def home():
    # Get categories with event counts
    categories = EventCategory.query.all()
    
    # Get upcoming events (next 30 days)
    upcoming_events = Event.query.filter(
        Event.date >= datetime.now(),
        Event.date <= datetime.now() + timedelta(days=30)
    ).order_by(Event.date).limit(6).all()
    
    # Get featured events (events with most registrations)
    featured_events = Event.query.order_by(Event.registration_count.desc()).limit(4).all()
    
    # Add has_available_tickets property to events
    for event in upcoming_events + featured_events:
        event.has_available_tickets = any(
            ticket_type.tickets_sold < ticket_type.quantity 
            for ticket_type in event.ticket_types
        )
    
    return render_template('home.html',
                         categories=categories,
                         upcoming_events=upcoming_events,
                         featured_events=featured_events)

@events.route('/list')
def list():
    category_id = request.args.get('category_id', type=int)
    query = Event.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Filter out past events
    query = query.filter(Event.date >= datetime.now())
    
    # Order by date
    events = query.order_by(Event.date).all()
    
    # Add has_available_tickets property
    for event in events:
        event.has_available_tickets = any(
            ticket_type.tickets_sold < ticket_type.quantity 
            for ticket_type in event.ticket_types
        )
    
    return render_template('events/list.html', 
                         events=events,
                         selected_category_id=category_id,
                         categories=EventCategory.query.all())

@events.route('/dashboard')
@login_required
def dashboard():
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    now = datetime.utcnow()
    
    # Get upcoming tasks
    upcoming_tasks = Task.query.join(Event).filter(
        Event.organizer_id == current_user.id,
        Task.due_date >= now
    ).order_by(Task.due_date.asc()).limit(5).all()
    
    # Calculate event statistics
    total_events = len(events)
    upcoming_events = sum(1 for e in events if e.date > now)
    past_events = sum(1 for e in events if e.date <= now)
    total_registrations = sum(e.registration_count for e in events)
    
    return render_template('events/dashboard.html',
                         events=events,
                         now=now,
                         upcoming_tasks=upcoming_tasks,
                         total_events=total_events,
                         upcoming_events=upcoming_events,
                         past_events=past_events,
                         total_registrations=total_registrations)

@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Get all categories
    categories = EventCategory.query.all()
    
    if request.method == 'POST':
        try:
            # Get basic event information
            title = request.form.get('title')
            description = request.form.get('description')
            date = datetime.strptime(request.form.get('date'), '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
            location = request.form.get('location')
            capacity = int(request.form.get('capacity'))
            category_id = int(request.form.get('category_id'))

            # Handle banner image
            banner_image = None
            if 'banner_image' in request.files:
                file = request.files['banner_image']
                banner_image = save_file(file)

            # Create event
            event = Event(
                title=title,
                description=description,
                date=date,
                end_date=end_date,
                location=location,
                capacity=capacity,
                organizer_id=current_user.id,
                category_id=category_id,
                banner_image=banner_image,
                status='draft'
            )
            db.session.add(event)
            
            # Handle ticket types
            ticket_names = request.form.getlist('ticket_names[]')
            ticket_prices = request.form.getlist('ticket_prices[]')
            ticket_quantities = request.form.getlist('ticket_quantities[]')
            ticket_descriptions = request.form.getlist('ticket_descriptions[]')
            
            for i in range(len(ticket_names)):
                ticket_type = TicketType(
                    event=event,
                    name=ticket_names[i],
                    price=float(ticket_prices[i]),
                    quantity=int(ticket_quantities[i]),
                    description=ticket_descriptions[i] if ticket_descriptions[i] else None
                )
                db.session.add(ticket_type)
            
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('events.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'error')
    
    return render_template('events/create.html', categories=categories)

@events.route('/<int:event_id>')
def view(event_id):
    event = Event.query.get_or_404(event_id)
    event.views_count += 1
    db.session.commit()
    return render_template('events/view.html', event=event)

@events.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register(event_id):
    event = Event.query.get_or_404(event_id)
    ticket_type_id = request.form.get('ticket_type_id')
    
    # Check if tickets are available
    ticket_type = TicketType.query.get_or_404(ticket_type_id)
    if ticket_type.tickets_sold >= ticket_type.quantity:
        flash('Sorry, this ticket type is sold out!', 'error')
        return redirect(url_for('events.view', event_id=event_id))
    
    # Create registration
    registration = Registration(
        event_id=event_id,
        user_id=current_user.id,
        ticket_type_id=ticket_type_id
    )
    
    # Update ticket stats
    ticket_type.tickets_sold += 1
    ticket_type.revenue += ticket_type.price
    event.registration_count += 1
    
    try:
        db.session.add(registration)
        db.session.commit()
        flash('Registration successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration.', 'error')
    
    return redirect(url_for('events.view', event_id=event_id))

@events.route('/analytics')
@login_required
def analytics():
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    analytics_data = {
        'total_events': len(events),
        'total_views': sum(event.views_count for event in events),
        'total_registrations': sum(event.registration_count for event in events),
        'total_revenue': sum(
            sum(ticket_type.revenue for ticket_type in event.ticket_types)
            for event in events
        ),
        'events': [{
            'title': event.title,
            'views': event.views_count,
            'registrations': event.registration_count,
            'revenue': sum(tt.revenue for tt in event.ticket_types),
            'ticket_stats': event.get_ticket_stats()
        } for event in events]
    }
    return render_template('events/analytics.html', analytics=analytics_data)
