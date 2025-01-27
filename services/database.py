import configparser
import mysql.connector

# Sample car data
SAMPLE_CARS = [
    ("Toyota", "Corolla", 2018, 25000, True, 2, 14),
    ("Honda", "Civic", 2019, 20000, True, 1, 10),
    ("Ford", "Focus", 2020, 15000, True, 3, 15),
    ("Chevrolet", "Cruze", 2017, 30000, True, 2, 12),
    ("Nissan", "Sentra", 2021, 10000, True, 1, 7),
    ("Hyundai", "Elantra", 2019, 22000, True, 2, 14),
    ("Kia", "Rio", 2020, 18000, True, 1, 10),
    ("Volkswagen", "Jetta", 2018, 27000, True, 3, 15),
    ("Subaru", "Impreza", 2021, 8000, True, 1, 7),
    ("Mazda", "Mazda3", 2020, 16000, True, 2, 14)
]

CONFIG_PATH = "config.ini"

# Constants for a user table
ROLE = 'role'
USER_ID = 'user_id'
USERNAME = 'username'
PASSWORD = 'password'

# Constants for a car table
CAR_ID = "car_id"
MAKE = "make"
MODEL = "model"
YEAR = "year"
MILEAGE = "mileage"
AVAILABLE = "available"
MIN_RENT_PERIOD = "min_rent_period"
MAX_RENT_PERIOD = "max_rent_period"

# Constants for a booking table
BOOKING_ID = 'booking_id'
START_DATE = 'start_date'
END_DATE = 'end_date'
TOTAL_COST = 'total_cost'
STATUS = 'status'

class Database:
    _instance = None

    def __new__(cls):
        #Singleton
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # To avoid reinitializing,
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.connection = None

        self._initialize_config()
        self._initialize_tables()

        self._initialized = True

    def _initialize_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)

        self.host = self.config.get('database', 'host')
        self.user = self.config.get('database', 'user')
        self.password = self.config.get('database', 'password')
        self.database_name = self.config.get('database', 'database')
        self.port = self.config.getint('database', 'port')

    def _initialize_tables(self):
        # Connect without selecting a DB to create/check the database
        self.connect(database=None)
        cursor = self.connection.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (self.database_name,))
        db_exists = cursor.fetchone() is not None

        # Create the database if it doesn't exist
        if not db_exists:
            cursor.execute(f"CREATE DATABASE `{self.database_name}`")
            print(f"Database '{self.database_name}' created successfully.")

        # Connect to the database
        self.connect(self.database_name)
        cursor = self.connection.cursor()

        self._create_tables(cursor)
        self._seed_cars_if_empty(cursor)

        self.connection.commit()
        print("Database initialization completed. All necessary tables exist and the cars table is populated if it was empty.")

    def connect(self, database=None):
        # Close any existing connection
        self.close()

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=database
        )

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect(self.database_name)
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def _create_tables(self, cursor):
        self._create_users_table(cursor)
        self._create_cars_table(cursor)
        self._create_bookings_table(cursor)

    def _create_users_table(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
          `user_id` INT AUTO_INCREMENT PRIMARY KEY,
          `username` VARCHAR(50) UNIQUE NOT NULL,
          `password` VARCHAR(255) NOT NULL,
          `role` BIT(10) NOT NULL
        ) ENGINE=INNODB;
        """)

    def _create_cars_table(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `cars` (
          `car_id` INT AUTO_INCREMENT PRIMARY KEY,
          `make` VARCHAR(50),
          `model` VARCHAR(50),
          `year` INT,
          `mileage` INT,
          `available` BOOLEAN DEFAULT TRUE,
          `min_rent_period` INT,
          `max_rent_period` INT
        ) ENGINE=INNODB;
        """)

    def _create_bookings_table(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `bookings` (
          `booking_id` INT AUTO_INCREMENT PRIMARY KEY,
          `car_id` INT,
          `user_id` INT,
          `start_date` DATE,
          `end_date` DATE,
          `total_cost` DECIMAL(10,2),
          `status` BIT(10),
          FOREIGN KEY (`car_id`) REFERENCES `cars`(`car_id`) ON DELETE CASCADE,
          FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
        ) ENGINE=INNODB;
        """)

    def _seed_cars_if_empty(self, cursor):
        cursor.execute("SELECT COUNT(*) AS count FROM cars")
        result = cursor.fetchone()
        if result and result[0] == 0:
            cursor.executemany("""
            INSERT INTO cars (make, model, year, mileage, available, min_rent_period, max_rent_period)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, SAMPLE_CARS)
            print("The cars table was empty, so 10 sample records were added.")
