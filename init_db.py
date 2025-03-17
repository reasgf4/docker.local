from app import create_app, db
from app.models.user import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_db():
    """Initialize the database."""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")
        
        # Check if admin user exists
        admin_email = os.environ.get('ADMIN_EMAIL')
        if admin_email:
            existing_admin = User.query.filter_by(email=admin_email).first()
            if not existing_admin:
                admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
                admin_password = os.environ.get('ADMIN_PASSWORD')
                if admin_password:
                    admin = User(username=admin_username, email=admin_email, is_admin=True)
                    admin.set_password(admin_password)
                    db.session.add(admin)
                    db.session.commit()
                    print(f"Admin user '{admin_username}' created.")
                else:
                    print("Admin password not set in environment variables.")
            else:
                print(f"Admin user with email '{admin_email}' already exists.")
        else:
            print("No admin email set in environment variables.")

if __name__ == "__main__":
    init_db()
    print("Database initialization complete.") 