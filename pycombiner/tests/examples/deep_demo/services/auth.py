"""
Authentication service
"""

from models.user import User
import re
import pathlib

def login(user: User) -> None:
    """Log in a user"""
    user.is_logged_in = True
    res = re.match(r'2(\d)4', "333254")
    print(f"User {user.name} logged in")

def logout(user: User) -> None:
    """Log out a user"""
    user.is_logged_in = False
    print(f"User {user.name} logged out")

def is_authenticated(user: User) -> bool:
    """Check if a user is authenticated"""
    return user.is_logged_in 