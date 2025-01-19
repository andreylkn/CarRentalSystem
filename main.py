from models.user.admin import Admin
from models.user.customer import Customer
from services.authorization_service import AuthorizationService
from utils.menu import show_guest_menu, show_admin_menu, show_customer_menu

def main():
    auth_service = AuthorizationService()
    current_user = None

    while True:
        if current_user is None:
            show_guest_menu()
            choice = input("Choose an option: ").strip()
            if choice == '1':
                auth_service.register_user()
            elif choice == '2':
                current_user = auth_service.authenticate()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if type(current_user) is Admin:
                show_admin_menu()
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    current_user.view_cars()
                elif choice == '2':
                    current_user.add_car()
                elif choice == '3':
                    current_user.update_car()
                elif choice == '4':
                    current_user.delete_car()
                elif choice == '5':
                    current_user.manage_bookings()
                elif choice == '6':
                    current_user.show_all_bookings()
                elif choice == '7':
                    current_user.manage_car_availability()
                elif choice == '8':
                    current_user = None
                else:
                    print("Invalid choice. Please try again.")
            elif type(current_user) is Customer:
                show_customer_menu()
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    current_user.view_cars()
                elif choice == '2':
                    current_user.create_booking()
                elif choice == '3':
                    current_user.show_my_bookings()
                elif choice == '4':
                    current_user.cancel_booking()
                elif choice == '5':
                    current_user.update_booking()
                elif choice == '6':
                    current_user = None
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
