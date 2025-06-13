import requests

# --- Content from: services\api_client.py ---
"""
API Client service module
"""


API_URL = "https://api.example.com/data"

def get_data():
    # Simulate an API call. In a real scenario, the following lines would be used.
    # response = requests.get(API_URL)
    # text_data = response.text
    text_data = "raw data from api"
    return format_output(text_data) 

# --- Content from: utils\helper.py ---
"""
Helper utility functions
"""

def greet(name: str) -> str:
    """
    Generate a greeting message
    
    Args:
        name: Name to greet
        
    Returns:
        Greeting message
    """
    return f"Hello, {name}!"

def format_output(text: str) -> str:
    return f"[PROCESSED] {text.upper()}" 


def main():
    print("Starting test application...")
    data = get_data()
    print(f"Received data: {data}")
    print("Test application finished.")
if __name__ == "__main__":
    main()