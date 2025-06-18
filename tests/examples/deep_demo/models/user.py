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

if __name__ == "__main__":
    User() 