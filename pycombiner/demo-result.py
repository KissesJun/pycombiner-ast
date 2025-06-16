"""
Database service
"""

class Database:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        """Connect to the database"""
        self.connected = True
        print("Connected to database")
    
    def disconnect(self):
        """Disconnect from the database"""
        self.connected = False
        print("Disconnected from database")

def connect_db() -> Database:
    """Create and connect to a database"""
    db = Database()
    db.connect()
    return db 
"""
String utility functions
"""

def format_name(name: str) -> str:
    """Format a name with proper capitalization"""
    return name.title()

def reverse_string(text: str) -> str:
    """Reverse a string"""
    return text[::-1]

def count_words(text: str) -> int:
    """Count the number of words in a string"""
    return len(text.split()) 

print("Import Successfully")
"""
User model
"""

class User:
    def __init__(self, name: str):
        self.name = name
        self.is_logged_in = False
    
    def __str__(self) -> str:
        return f"User({self.name})"
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "name": self.name,
            "is_logged_in": self.is_logged_in
        } 
"""
Math utility functions
"""

def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b 
"""
Authentication service
"""


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