
import json      # json is a built-in Python module. It is used to store retrieve and store data. Use JSON to save data in vehicles.txt.
import os        #os is a built-in Python module. It allows Python to interact with the operating system. Use to check whether data file exist.

# -------------------------------
# VEHICLE CLASS
# -------------------------------

class Vehicle:          # Vehicle is the class that defines the information every vehicle should congtain.

    def __init__(self, vehicle_id, vehicle_type, model, rate, available=True):    # These statements assign values to the object's attributes.
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.model = model
        self.rate = rate
        self.available = available

    def display(self):     # Displays the details of a vehicle.
        status = "Available" if self.available else "Rented"

        print(
            f"{self.vehicle_id} | {self.vehicle_type} | "
            f"{self.model} | Rs. {self.rate:g}/day | {status}"
        )

    def to_dict(self):  # Converts a Vehicle object into a dictionary. 
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type,
            "model": self.model,
            "rate": self.rate,
            "available": self.available
        }         # JSON cannot directly serialize your custom Vehicle objects.
# -------------------------------
# RENTAL SYSTEM CLASS    
# -------------------------------

class RentalSystem:      # This class controls the complete rental management system.

    def __init__(self):  # Constructor of the RentalSystem class. It runs automatically when an object is created.
        self.vehicles = []  # Creates an empty list to store vehicle objects.
        self.rentals = {}   # Creates an empty dictionary to store rental details.

        self.filename = "vehicles.txt"  # Stores the name of the file where project data is saved.

        self.load_data()  # Calls the load_data() method to retrieve previously saved information when the system starts.

    # ---------------------------
    # SAVE DATA INTO FILE
    # ---------------------------
 # Purpose: Saves all vehicle and rental information into vehicles.txt
    
    def save_data(self):  # Defines a method named save_data().

        data = {
            "vehicles": [v.to_dict() for v in self.vehicles],  # This is a list comprehension.
            "rentals": self.rentals  # Stores the rental dictionary inside the main data dictionary.
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    # ---------------------------
    # LOAD DATA FROM FILE
    # ---------------------------
    
# Purpose: Loads previously saved vehicle and rental information when the program starts.
    
    def load_data(self):  

        if not os.path.exists(self.filename):         # This checks whether vehicles.txt exist.
            return

        try:  # It allows the program to handle certain errors without immediately crashing.
            with open(self.filename, "r") as file:
                data = json.load(file)

            for item in data.get("vehicles", []):  # It retrieves the value associated with the "vehicles" key.
                vehicle = Vehicle(
                    item["vehicle_id"],
                    item["vehicle_type"],
                    item["model"],
                    item["rate"],
                    item["available"]
                )

                self.vehicles.append(vehicle)  # Adds newly created vehicle object to the vehicles list.

            self.rentals = data.get("rentals", {})   

        except (json.JSONDecodeError, KeyError, TypeError):  # Handles this type of error.
            print("Warning: Could not load saved data.")  # Dispaly error when one of these errors occurs.

    # ---------------------------
    # GENERATE VEHICLE ID
    # ---------------------------
    
# Purpose: Automatically generates a unique vehicle ID.
    
    def generate_id(self): # generate vehicle IDs.

        numbers = []

        for vehicle in self.vehicles:
            try:
                numbers.append(int(vehicle.vehicle_id[1:]))
            except ValueError:
                continue

        next_number = max(numbers, default=0) + 1

        return "V" + str(next_number) # Converts the number into a string and adds "V" before it.

    # ---------------------------
    # ADD VEHICLE
    # ---------------------------

# Purpose: Adds a new vehicle to the rental system.
    def add_vehicle(self):

        vehicle_type = input("Type: ").strip()  # strip removes unnecessary spaces. 
        model = input("Model: ").strip()

        if not vehicle_type or not model:
            print("Vehicle type and model cannot be empty.")
            return

        try:  # Starts an exception-handling block.
            rate = float(input("Rate per day: "))

            if rate <= 0:
                print("Rate must be greater than zero.")
                return

        except ValueError:
            print("Please enter a valid rate.")
            return

        vehicle_id = self.generate_id()  # generate_id() is func to generate a new vehicle id.

        vehicle = Vehicle(
            vehicle_id,
            vehicle_type,
            model,
            rate
        )

        self.vehicles.append(vehicle)

        self.save_data()

        print(
            f"Vehicle added. ID: {vehicle_id} | "
            f"{vehicle_type} | {model} | "
            f"Rs. {rate:g}/day | Available"
        )

    # ---------------------------
    # FIND VEHICLE BY ID
    # ---------------------------

    def find_vehicle(self, vehicle_id):

        for vehicle in self.vehicles:

            if vehicle.vehicle_id == vehicle_id: # compares the ID of current and ID of enter by user.
                return vehicle

        return None

    # ---------------------------
    # RENT VEHICLE
    # ---------------------------

    def rent_vehicle(self):

        vehicle_id = input("Vehicle ID: ").strip()
        customer = input("Customer: ").strip()

        if not customer:
            print("Customer name cannot be empty.")
            return

        try:
            days = int(input("Days: "))

            if days < 1:
                print("Days must be 1 or more.")
                return

        except ValueError:
            print("Please enter a valid number of days.")
            return

        vehicle = self.find_vehicle(vehicle_id) # method to search for the requested vehicle.

        if vehicle is None:
            print("Vehicle ID not found.")
            return

        if not vehicle.available:
            print(f"Vehicle {vehicle_id} is not available.")
            return

        # Calculate original bill
        bill = vehicle.rate * days

        # Apply 10% discount for 7 or more days
        discount = 0

        if days >= 7:
            discount = bill * 0.10
            bill = bill - discount

        # Update vehicle status
        vehicle.available = False

        # Store rental details in dictionary
        self.rentals[vehicle_id] = {
            "customer": customer,
            "days": days,
            "bill": bill
        }

        self.save_data()

        if discount > 0:
            print(
                f"{vehicle_id} rented to {customer} for {days} days. "
                f"10% discount applied. Bill: Rs. {bill:g}"
            )
        else:
            print(
                f"{vehicle_id} rented to {customer} for {days} days. "
                f"Bill: Rs. {bill:g}"
            )

    # ---------------------------
    # RETURN VEHICLE
    # ---------------------------

    def return_vehicle(self):

        vehicle_id = input("Vehicle ID: ").strip()

        vehicle = self.find_vehicle(vehicle_id)

        if vehicle is None:
            print("Vehicle ID not found.")
            return

        if vehicle.available:
            print(f"Vehicle {vehicle_id} is already available.")
            return

        # Remove rental details
        self.rentals.pop(vehicle_id, None)

        # Update vehicle status
        vehicle.available = True

        self.save_data() # Saves the updated rental information and vehicle availability.

        print(f"{vehicle_id} returned. Status: Available")

    # ---------------------------
    # VIEW AVAILABLE VEHICLES
    # ---------------------------

 # Purpose: Displays all vehicles stored in the system.

    def view_vehicles(self):

        print("\n---------- VEHICLE LIST ----------")

        if not self.vehicles:
            print("No vehicles found.")
            return

        for vehicle in self.vehicles:
            vehicle.display()

    # ---------------------------
    # MAIN MENU
    # ---------------------------

 # Purpose: Provides the main interface through which users operate the system.
    def menu(self): 

        while True:

            print("\n================================")
            print("   VEHICLE RENTAL MANAGEMENT")
            print("================================")
            print("1. Add Vehicle")
            print("2. Rent Vehicle")
            print("3. Return Vehicle")
            print("4. View Vehicles")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_vehicle()

            elif choice == "2":
                self.rent_vehicle()

            elif choice == "3":
                self.return_vehicle()

            elif choice == "4":
                self.view_vehicles()

            elif choice == "5":
                print("Thank you for using Vehicle Rental System!")
                break

            else:
                print("Invalid choice. Please try again.")


# -------------------------------
# MAIN PROGRAM
# -------------------------------

if __name__ == "__main__":  # Main guard 

    system = RentalSystem()  # Creates an object named system of the RentalSystem class.

    system.menu()  # This displays the main menu and allows the user to operate the project.

