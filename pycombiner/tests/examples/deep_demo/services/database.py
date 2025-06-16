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