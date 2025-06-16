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