from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.task import Task
from app.models.event import Event

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/create/<int:event_id>', methods=['POST'])
@login_required
def create(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        flash('You do not have permission to add tasks to this event.', 'error')
        return redirect(url_for('events.view', event_id=event_id))
    
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    
    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        event_id=event_id
    )
    
    db.session.add(task)
    db.session.commit()
    
    flash('Task created successfully!', 'success')
    return redirect(url_for('events.view', event_id=event_id))

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
@login_required
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.event.organizer_id != current_user.id:
        flash('You do not have permission to modify this task.', 'error')
        return redirect(url_for('events.view', event_id=task.event_id))
    
    task.completed = True
    db.session.commit()
    
    flash('Task marked as complete!', 'success')
    return redirect(url_for('events.view', event_id=task.event_id))
