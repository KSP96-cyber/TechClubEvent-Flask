from flask import abort, render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from techclubevent import db
from techclubevent.models import EventPost, User, Registration
from techclubevent.event_posts.forms import EventPostForm, EventRegistrationForm

event_posts = Blueprint('event_posts',__name__)

#create:
@event_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = EventPostForm()
    if form.validate_on_submit():
        event_post = EventPost(
            title=form.title.data,
            text=form.text.data,
            author_id=current_user.id
        )
        db.session.add(event_post)
        db.session.commit()
        flash("Event Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


# Event Post (view): 
# int: makes sure that the event_post_id gets passed as in integer
# instead of a string.
@event_posts.route('/<int:event_post_id>')
def event_post(event_post_id):
    # grab the requested event post by id number or return 404
    event_post = EventPost.query.get_or_404(event_post_id)
    return render_template('event_post.html',title=event_post.title,
                            date=event_post.date,post=event_post
    )
# update:
@event_posts.route("/<int:event_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(event_post_id):
    event_post = EventPost.query.get_or_404(event_post_id)
    if event_post.author_id !=current_user.id:
        # Forbidden, No Access
        abort(403)
    form = EventPostForm()
    if form.validate_on_submit():
        event_post.title = form.title.data
        event_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('event_posts.event_post', event_post_id=event_post.id))
    # Pass back the old event post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = event_post.title
        form.text.data = event_post.text
    return render_template('create_post.html', title='Update',
                           form=form)

# delete:
@event_posts.route("/<int:event_post_id>/delete", methods=['POST'])
@login_required
def delete_post(event_post_id):
    event_post = EventPost.query.get_or_404(event_post_id)
    if current_user.role != User.AUTHOR:
        abort(403)
    db.session.delete(event_post)
    db.session.commit()
    flash('Event has been deleted')
    return redirect(url_for('core.index'))

@event_posts.route("/event-register", methods=['GET', 'POST'])
@login_required
def register_for_event():
    form = EventRegistrationForm()
    
    form.event.choices = [(event.id, event.title)
                         for event in EventPost.query.all()]
    
    
    if form.validate_on_submit():
        existing_registration = Registration.query.filter_by(
            user_id=current_user.id,
            event_id=form.event.data
        ).first()

        if existing_registration:
            flash('You are already registered for this event!', 'warning')
            return redirect(url_for('core.index'))
        
        
        registration = Registration(user_id=current_user.id, event_id=form.event.data)
        db.session.add(registration)
        db.session.commit()
        flash('You have successfully registered for the event!', 'success')
        return redirect(url_for('core.index'))  # Redirect to homepage or event page
    return render_template('register_event.html', form=form)



