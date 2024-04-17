import json
import hashlib
# Authentication
class UserManagement:
    def __init__(self):
        self.users = self.load_users()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in users.json file.")
            return {}

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username]["password"] == hashed_password:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False

    def create_user():
        username = input("Enter new username: ")
        if username in UserManagement.users:
            print("Username already exists.")
            return
        password = input("Enter new password: ")
        hashed_password = UserManagement.hash_password(password)
        UserManagement.users[username] = {"password": hashed_password}
        UserManagement.save_users()
        print("User created successfully.")

UserManagement.create_user()
UserManagement.login()