"""
Authentication service
"""

from models.user import User

def login(user: User) -> None:
    """Log in a user"""
    user.is_logged_in = True
    print(f"User {user.name} logged in")

def logout(user: User) -> None:
    """Log out a user"""
    user.is_logged_in = False
    print(f"User {user.name} logged out")

def is_authenticated(user: User) -> bool:
    """Check if a user is authenticated"""
    return user.is_logged_in 