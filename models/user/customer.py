from models.user.user import User
from services.base_service import BaseService
from services.database import CAR_ID, START_DATE, END_DATE, TOTAL_COST, STATUS, MAKE, MODEL, BOOKING_ID
from utils.input_validation import input_int, input_date, yes_no

class Customer(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username)

    def view_cars(self):
        cars = self._car_service.get_available_cars()
        print("================ List Of Cars ================")
        for car in cars:
            car.print_short_details()
        print("==============================================")

    def create_booking(self):
        print("================== Booking ==================")
        car_id = input_int("Car ID: ", 1)

        car = self._car_service.get_available_car_by_id(car_id)
        if not car:
            print("Car not available or not found.")
            return None

        print("Enter rental period:")
        start_date = input_date("Start date (DD/MM/YYYY): ")
        end_date = input_date("End date (DD/MM/YYYY): ")
        insurance = yes_no("Add insurance for a flat $20 fee?")

        booking_id = self._booking_service.create_booking(self.user_id, car, start_date, end_date, insurance)

        if booking_id:
            print(f"Booking request created with ID: {booking_id}. Waiting for approval.")
        else:
            print("Failed to create booking. Please check dates and availability.")
        print("============================================")

    def show_bookings(self):
        bookings = self._booking_service.get_user_bookings(self.user_id)
        if not bookings:
            print("You have no bookings.")
            return
        for b in bookings:
            print("-------------------------------------------------")
            print(f"Booking ID: {b[BOOKING_ID]}")
            print(f"Car: {b[MAKE]} {b[MODEL]} (Car ID: {b[CAR_ID]})")
            print(f"Period: {b[START_DATE]} to {b[END_DATE]}")
            print(f"Total Cost: ${b[TOTAL_COST]:.2f}")
            print(f"Status: {self._booking_service.convert_booking_status_to_string(b[STATUS])}")

    def cancel_booking(self):
        booking_id = input_int("Enter the Booking ID to cancel: ", 1)
        self._booking_service.cancel_booking(booking_id, self.user_id)

    def update_booking(self):
        booking_id = input_int("Enter the Booking ID to update: ", 1)
        new_start_date = input_date("New start date (DD/MM/YYYY): ")
        new_end_date = input_date("New end date (DD/MM/YYYY): ")
        self._booking_service.update_booking(booking_id, self.user_id, new_start_date, new_end_date)