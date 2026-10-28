from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from techclubevent import db
from techclubevent.models import Attendee, EventPost, Registration, User
from techclubevent.list_attendees.forms import RegistrationForm  

list_attendees = Blueprint('list_attendees', __name__)

@list_attendees.route('/show_attendees/<int:event_id>/attendees')
def show_attendees(event_id):
    event = EventPost.query.get_or_404(event_id)
    attendees = User.query.join(Registration, Registration.user_id ==User.id).filter(Registration.event_id ==event_id).all()
    return render_template('list_attendees.html', event=event, attendees=attendees)

#end
######## Create a route for handling registration:


@list_attendees.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.event.choices = [(e.id, e.title) for e in EventPost.query.all()]

    if form.validate_on_submit():
        registration = Registration(user_id=current_user.id, 
                                    event_id=form.event.data)
        db.session.add(registration)
        db.session.commit()
        flash('You have successfully registered for the event!')
        return redirect(url_for('core.index'))

    return render_template('register.html', form=form)

################ Create a route to handle check-ins:

@list_attendees.route('/check_in/<int:event_id>', methods=['POST'])
def check_in(event_id):
    registration = Registration.query.filter_by(user_id=current_user.id, 
                                                event_id=event_id).first()
    if registration:
        registration.checked_in = True
        db.session.commit()
        flash('You have successfully checked in!')
    else:
        flash('Registration not found!')

    return redirect(url_for('core.index'))

