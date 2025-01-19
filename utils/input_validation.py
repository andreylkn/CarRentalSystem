import datetime

def input_int(prompt, min_val=None, max_val=None):
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            val = int(val)
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Please enter a value between {min_val} and {max_val}.")
                continue
            return val
        else:
            print("Invalid input. Please enter an integer.")

def input_str(prompt):
    val = input(prompt).strip()
    if not val:
        print("Input cannot be empty.")
        return input_str(prompt)
    return val

def input_date(prompt):
    while True:
        val = input(prompt).strip()
        try:
            date_obj = datetime.datetime.strptime(val, "%d/%m/%Y")
            return date_obj
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY.")

def yes_no(prompt):
    while True:
        val = input(prompt + " (y/n): ").strip().lower()
        if val in ['y', 'yes']:
            return True
        elif val in ['n', 'no']:
            return False
        else:
            print("Invalid choice. Enter 'y' or 'n'.")
