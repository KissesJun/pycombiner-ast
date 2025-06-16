"""
Main entry point for the deep demo
"""

from utils.helpers.math_utils import add, subtract
from utils.helpers.string_utils import format_name
from models.user import User
from services.auth import login, logout
from services.database import connect_db

def main():
    # Initialize database
    db = connect_db()
    
    # Create a user
    user = User("John Doe")
    formatted_name = format_name(user.name)
    
    # Perform some calculations
    result1 = add(10, 5)
    result2 = subtract(10, 5)
    
    # Login and logout
    login(user)
    logout(user)
    
    print(f"Results: {result1}, {result2}")
    print(f"Formatted name: {formatted_name}")

if __name__ == "__main__":
    main() 