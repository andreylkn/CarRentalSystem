from models.car import Car
from services.base_service import BaseService
from services.database import CAR_ID, MAKE, MODEL, YEAR, MILEAGE, AVAILABLE, MIN_RENT_PERIOD, MAX_RENT_PERIOD

class CarService(BaseService):
    def __init__(self):
        super().__init__()

    def add_car(self, make, model, year, mileage, min_period, max_period):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO cars (make, model, year, mileage, available, min_rent_period, max_rent_period) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (make, model, year, mileage, True, min_period, max_period)
            )
            conn.commit()
            print("Car added successfully.")
        except Exception as e:
            print("Error adding car:", str(e))

    def update_car(self, car_id, **kwargs):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        updates = []
        vals = []
        for k, v in kwargs.items():
            updates.append(f"{k}=%s")
            vals.append(v)
        vals.append(car_id)
        sql = f"UPDATE cars SET {', '.join(updates)} WHERE car_id=%s"
        try:
            cursor.execute(sql, tuple(vals))
            conn.commit()
            if cursor.rowcount == 0:
                print("No car found with the given ID to update.")
            else:
                print("Car updated successfully.")
        except Exception as e:
            print("Error updating car:", str(e))

    def delete_car(self, car_id):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cars WHERE car_id=%s", (car_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("No car found with the given ID to delete.")
            else:
                print("Car deleted successfully.")
        except Exception as e:
            print("Error deleting car:", str(e))

    def get_all_cars(self):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM cars")
            rows = cursor.fetchall()
            return [Car(row[CAR_ID], row[MAKE], row[MODEL], row[YEAR], row[MILEAGE], row[AVAILABLE], row[MIN_RENT_PERIOD], row[MAX_RENT_PERIOD])
                    for row in rows]
        except Exception as e:
            print("Error fetching cars:", str(e))
            return []

    def get_available_cars(self):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM cars WHERE available = TRUE")
            rows = cursor.fetchall()
            return [Car(row[CAR_ID], row[MAKE], row[MODEL], row[YEAR], row[MILEAGE], row[AVAILABLE], row[MIN_RENT_PERIOD], row[MAX_RENT_PERIOD])
                    for row in rows]
        except Exception as e:
            print("Error fetching available cars:", str(e))
            return []

    def get_car_by_id(self, car_id):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE car_id=%s", (car_id,))
        return cursor.fetchone()

    def get_available_car_by_id(self, car_id):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE car_id=%s AND available=TRUE", (car_id,))
        row = cursor.fetchone()
        if not row:
            return None
        else:
            return Car(row[CAR_ID], row[MAKE], row[MODEL], row[YEAR], row[MILEAGE], row[AVAILABLE], row[MIN_RENT_PERIOD], row[MAX_RENT_PERIOD])
