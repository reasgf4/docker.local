import os
import sys
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User

# Load environment variables
load_dotenv()

def create_admin_user(username, email, password):
    """Create an admin user."""
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return False
        
        # Create new admin user
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user {username} created successfully.")
        return True

if __name__ == "__main__":
    # Get admin credentials from environment or command line
    admin_username = os.environ.get('ADMIN_USERNAME') or input("Enter admin username: ")
    admin_email = os.environ.get('ADMIN_EMAIL') or input("Enter admin email: ")
    admin_password = os.environ.get('ADMIN_PASSWORD') or input("Enter admin password: ")
    
    if not admin_username or not admin_email or not admin_password:
        print("Error: Username, email, and password are required.")
        sys.exit(1)
    
    create_admin_user(admin_username, admin_email, admin_password) 