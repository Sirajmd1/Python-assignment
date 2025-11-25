import re
import json

def check_password_strength(password: str) -> bool:
    """
    Returns True if the password meets all of the following criteria:
    • At least 8 characters long
    • Contains both uppercase and lowercase letters
    • Contains at least one digit
    • Contains at least one special character (!@#$%)
    """
    if len(password) < 8:
        return False

    # Use regular expressions to verify each requirement
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special = re.search(r'[!@#$%]', password)

    return all([has_upper, has_lower, has_digit, has_special])


def main():
    # Configuration data
    config = {
        "Database": {
            "host": "localhost",
            "port": "3306",
            "username": "admin",
            "password": "secret"
        },
        "Server": {
            "address": "192.168.0.1",
            "port": "8080"
        }
    }

    password = input("Enter a password to check its strength: ")

    if check_password_strength(password):
        print("✅ Strong password! It meets all the criteria.")
    else:
        print("❌ Weak password. It must contain:")
        if len(password) < 8:
            print("- At least 8 characters")
        if not re.search(r'[A-Z]', password):
            print("- At least one uppercase letter")
        if not re.search(r'[a-z]', password):
            print("- At least one lowercase letter")
        if not re.search(r'\d', password):
            print("- At least one digit")
        if not re.search(r'[!@#$%]', password):
            print("- At least one special character (! @ # $ %)")


if __name__ == "__main__":
    main()