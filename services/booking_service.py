from services.base_service import BaseService
from datetime import datetime

from services.database import MIN_RENT_PERIOD, MAX_RENT_PERIOD, CAR_ID, MILEAGE

MIN_RENTAL_DAYS = 1
INSURANCE_COST = 20.0
BASE_RATE = 50.0

class BookingService(BaseService):
    def __init__(self):
        super().__init__()

    def create_booking(self, user_id, car, start_date, end_date, include_insurance=False):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validate date range
        rental_days = (end_date - start_date).days
        if rental_days < MIN_RENTAL_DAYS:
            print("End date must be after the start date.")
            return None

        if rental_days < car.min_rent_period or rental_days > car.max_rent_period:
            print(f"Rental period must be between {car.min_rent_period} and {car.max_rent_period} days.")
            return None

        # Check for overlapping approved bookings
        if self._is_overlapping_approved_booking(car, start_date, end_date):
            print("This car is already booked for the selected date range.")
            return None

        # Calculate cost
        total_cost = self.calculate_rental_fee(car.mileage, rental_days, include_insurance)

        try:
            cursor.execute("INSERT INTO bookings (car_id, user_id, start_date, end_date, total_cost, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (car.id, user_id, start_date, end_date, total_cost, 'pending')
            )
            conn.commit()
            print(f"Booking request created with total cost: ${total_cost}. Waiting for approval.")
            return cursor.lastrowid
        except Exception as e:
            print("An error occurred while creating the booking:", str(e))
            return None

    def get_pending_bookings(self):
        """
        Return pending bookings with car make/model and customer username.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT b.booking_id, b.car_id, b.user_id, b.start_date, b.end_date, b.total_cost, b.status,
               c.make, c.model,
               u.username
        FROM bookings b
        JOIN cars c ON b.car_id = c.car_id
        JOIN users u ON b.user_id = u.user_id
        WHERE b.status='pending'
        ORDER BY b.booking_id ASC
        """
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_bookings(self):
        """
        Return all bookings (regardless of status) with car make/model and customer username.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT b.booking_id, b.car_id, b.user_id, b.start_date, b.end_date, b.total_cost, b.status,
               c.make, c.model,
               u.username
        FROM bookings b
        JOIN cars c ON b.car_id = c.car_id
        JOIN users u ON b.user_id = u.user_id
        ORDER BY b.booking_id ASC
        """
        cursor.execute(query)
        return cursor.fetchall()

    def get_user_bookings(self, user_id):
        """
        Retrieve all bookings for a specific user along with car details.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT b.booking_id, b.car_id, b.user_id, b.start_date, b.end_date, b.total_cost, b.status,
               c.make, c.model
        FROM bookings b
        JOIN cars c ON b.car_id = c.car_id
        WHERE b.user_id = %s
        ORDER BY b.booking_id ASC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    def cancel_booking(self, booking_id, user_id):
        """
        Cancel a user's booking if it is pending.
        Set status to 'rejected'.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if booking belongs to this user and is pending
        cursor.execute("SELECT * FROM bookings WHERE booking_id=%s AND user_id=%s AND status='pending'",
                       (booking_id, user_id))
        booking = cursor.fetchone()
        if not booking:
            print("You can only cancel pending bookings that belong to you.")
            return False

        # Cancel the booking
        cursor.execute("UPDATE bookings SET status='rejected' WHERE booking_id=%s", (booking_id,))
        conn.commit()
        print("Booking canceled successfully.")
        return True

    def update_booking(self, booking_id, user_id, new_start_date, new_end_date):
        """
        Update a user's booking (change dates) if it is pending and no overlap occurs.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if booking belongs to this user and is pending
        cursor.execute("SELECT b.*, c.make, c.model, c.available, c.min_rent_period, c.max_rent_period, c.mileage FROM bookings b JOIN cars c ON b.car_id=c.car_id WHERE booking_id=%s AND user_id=%s AND status='pending'",
                    (booking_id, user_id))
        booking = cursor.fetchone()
        if not booking:
            print("You can only update pending bookings that belong to you.")
            return False

        rental_days = (new_end_date - new_start_date).days
        if rental_days < MIN_RENTAL_DAYS:
            print("End date must be after the start date.")
            return False

        # Check min/max rent period
        if rental_days < booking[MIN_RENT_PERIOD] or rental_days > booking[MAX_RENT_PERIOD]:
            print(
                f"Rental period must be between {booking[MIN_RENT_PERIOD]} and {booking[MAX_RENT_PERIOD]} days.")
            return False

        # Check for overlapping approved bookings again
        if self._is_overlapping_approved_booking(booking[CAR_ID], new_start_date, new_end_date, exclude_booking_id=booking_id):
            print("This car is already booked for the selected date range.")
            return False

        # Recalculate cost
        total_cost = self.calculate_rental_fee(booking[MILEAGE], rental_days, self._had_insurance(booking_id))

        # Update the booking
        cursor.execute("""
        UPDATE bookings SET start_date=%s, end_date=%s, total_cost=%s
        WHERE booking_id=%s
        """, (new_start_date, new_end_date, total_cost, booking_id))
        conn.commit()
        print(f"Booking updated successfully. New total cost: ${total_cost:.2f}")
        return True

    def _had_insurance(self, booking_id):
        """
        If you previously had a parameter for insurance, you might store it.
        If not, and you want to maintain that info, you'd need a column in the bookings table.
        For now, we'll assume the original logic doesn't store this. Returning False.
        """
        return False

    def _is_overlapping_approved_booking(self, car, start_date, end_date, exclude_booking_id=None):
        conn = self._get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 1 FROM bookings
        WHERE car_id = %s
          AND status = 'approved'
          AND NOT (end_date < %s OR start_date > %s)
        """
        params = [car.id, start_date, end_date]
        # If we are updating an existing booking, exclude it from overlap check
        if exclude_booking_id:
            query += " AND booking_id <> %s"
            params.append(exclude_booking_id)

        cursor.execute(query, tuple(params))
        result = cursor.fetchone()
        return result is not None

    def calculate_rental_fee(self, car_mileage, rental_days, include_insurance=False):
        mileage_surcharge_per_day = (car_mileage // 1000) * 0.05 * 100
        daily_rate = BASE_RATE + mileage_surcharge_per_day
        total_cost = daily_rate * rental_days
        if include_insurance:
            total_cost += INSURANCE_COST
        return round(total_cost, 2)