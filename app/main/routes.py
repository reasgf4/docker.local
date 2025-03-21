from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models.user import User

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html', title='Dashboard')

@bp.route('/about')
def about():
    return render_template('main/about.html', title='About')

@bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('main.index'))
    
    # Convert ScalarResult to a list
    users_query = db.session.execute(db.select(User).order_by(User.username)).scalars()
    users = list(users_query)
    
    # Get configuration for the template
    config = {
        'DOCKER_HOST': current_app.config['DOCKER_HOST'],
        'SQLALCHEMY_DATABASE_URI': current_app.config['SQLALCHEMY_DATABASE_URI']
    }
    
    return render_template('main/admin.html', title='Admin Panel', users=users, config=config) 