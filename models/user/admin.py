from models.user.user import User
from services.database import MODEL, MAKE, YEAR, MILEAGE, MIN_RENT_PERIOD, MAX_RENT_PERIOD, BOOKING_ID, START_DATE, \
    END_DATE, TOTAL_COST, CAR_ID, USERNAME, USER_ID, STATUS
from utils.input_validation import input_int, input_str

class Admin(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username)

    def view_cars(self):
        cars = self._car_service.get_all_cars()
        print("================ List Of Cars ================")
        for car in cars:
            car.print_full_details()
        print("==============================================")

    def add_car(self):
        make = input_str("Make: ")
        model = input_str("Model: ")
        year = input_int("Year: ", 1900, 2100)
        mileage = input_int("Mileage: ", 0)
        min_period = input_int("Min rent period (days): ", 1)
        max_period = input_int("Max rent period (days): ", min_period)
        self._car_service.add_car(make, model, year, mileage, min_period, max_period)

    def update_car(self):
        car_id = input_int("Car ID to update: ", 1)

        print("\nWhich field would you like to update?")
        print("1. Make")
        print("2. Model")
        print("3. Year")
        print("4. Mileage")
        print("5. Minimum Rent Period")
        print("6. Maximum Rent Period")
        choice = input_int("Choose an option (1-6): ", 1, 6)

        field_map = {
            1: MAKE,
            2: MODEL,
            3: YEAR,
            4: MILEAGE,
            5: MIN_RENT_PERIOD,
            6: MAX_RENT_PERIOD
        }

        field_name = field_map[choice]

        # Prompt for new value, with type checks
        if field_name in [YEAR, MILEAGE, MIN_RENT_PERIOD, MAX_RENT_PERIOD]:
            new_value = input_int(f"Enter new {field_name.replace('_', ' ')}: ")
        else:
            new_value = input_str(f"Enter new {field_name}: ")

        self._car_service.update_car(car_id, **{field_name: new_value})

    def delete_car(self):
        car_id = input_int("Car ID to delete: ", 1)
        self._car_service.delete_car(car_id)

    def manage_bookings(self):
        # Enhanced details: Display car make/model and username of customer
        pending_bookings = self._booking_service.get_pending_bookings()
        if not pending_bookings:
            print("No pending bookings.")
            return
        for b in pending_bookings:
            print("-------------------------------------------------")
            print(f"Booking ID: {b[BOOKING_ID]}")
            print(f"Car: {b[MAKE]} {b[MODEL]} (ID: {b[CAR_ID]})")
            print(f"Customer: {b[USERNAME]} (User ID: {b[USER_ID]})")
            print(f"Period: {b[START_DATE]} to {b[END_DATE]}")
            print(f"Total Cost: ${b[TOTAL_COST]:.2f}")
            print("Current Status: pending")
            decision = input("Approve (A) or Reject (R)? ").strip().lower()
            if decision == 'a':
                self._booking_service.update_booking_status(b[BOOKING_ID], 'approved')
            elif decision == 'r':
                self._booking_service.update_booking_status(b[BOOKING_ID], 'rejected')
            else:
                print("Invalid choice. Skipping this booking.")

    def show_all_bookings(self):
        # Displays all bookings (approved, pending, rejected) with details
        all_bookings = self._booking_service.get_all_bookings()
        if not all_bookings:
            print("No bookings found.")
            return
        for bk in all_bookings:
            print("-------------------------------------------------")
            print(f"Booking ID: {bk[BOOKING_ID]}")
            print(f"Car: {bk[MAKE]} {bk[MODEL]} (Car ID: {bk[CAR_ID]})")
            print(f"Customer: {bk[USERNAME]} (User ID: {bk[USER_ID]})")
            print(f"Period: {bk[START_DATE]} to {bk[END_DATE]}")
            print(f"Total Cost: ${bk[TOTAL_COST]:.2f}")
            print(f"Status: {bk[STATUS]}")

    def manage_car_availability(self):
        # Allows admin to toggle a car's availability
        car_id = input_int("Enter the Car ID to update availability: ", 1)
        car = self._car_service.get_car_by_id(car_id)
        if not car:
            print("Car not found.")
            return

        print(f"Car {car.id}: {car.make} {car.model} | Currently Available: {car.available}")
        choice = input("Set availability to available (A) or unavailable (U)? ").strip().lower()
        if choice == 'a':
            self._car_service.update_car(car_id, available=True)
            print("Car is now available.")
        elif choice == 'u':
            self._car_service.update_car(car_id, available=False)
            print("Car is now unavailable.")
        else:
            print("Invalid choice. No changes made.")