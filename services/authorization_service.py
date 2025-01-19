from models.user.admin import Admin
from models.user.customer import Customer
from services.base_service import BaseService
from services.database import ROLE, USER_ID, USERNAME, PASSWORD
import bcrypt

ADMIN_ROLE = 'admin'
CUSTOMER_ROLE = 'customer'

class AuthorizationService(BaseService):
    def __init__(self):
        super().__init__()

    def authenticate(self):
        username = input("Username: ")
        password = input("Password: ")

        user_data = self.__login(username, password)
        if not user_data:
            print("Invalid credentials.")
            return None
        if user_data[ROLE] == ADMIN_ROLE:
            return Admin(user_data[USER_ID], user_data[USERNAME])
        else:
            return Customer(user_data[USER_ID], user_data[USERNAME])

    def register_user(self):
        username = input("Choose a username: ")
        password = input("Choose a password: ")

        role_choice = input("Are you an admin or customer? (admin/customer): ").strip().lower()  # TODO Y/N
        role = ADMIN_ROLE if role_choice == ADMIN_ROLE else CUSTOMER_ROLE
        if self.__register(username, password, role):
            print("User registered successfully.")
        else:
            print("Registration failed. Username might be taken.")

    def __register(self, username, password, role=CUSTOMER_ROLE):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                           (username, hashed_pw.decode('utf-8'), role))
            conn.commit()
            return True
        except:
            return False

    def __login(self, username, password):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[PASSWORD].encode('utf-8')):
            return user
        return None
