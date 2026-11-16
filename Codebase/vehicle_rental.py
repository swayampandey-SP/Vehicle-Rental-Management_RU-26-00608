
import json
import os

# -------------------------------
# VEHICLE CLASS
# -------------------------------

class Vehicle:

    def __init__(self, vehicle_id, vehicle_type, model, rate, available=True):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.model = model
        self.rate = rate
        self.available = available

    def display(self):
        status = "Available" if self.available else "Rented"

        print(
            f"{self.vehicle_id} | {self.vehicle_type} | "
            f"{self.model} | Rs. {self.rate:g}/day | {status}"
        )

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type,
            "model": self.model,
            "rate": self.rate,
            "available": self.available
        }

# -------------------------------
# RENTAL SYSTEM CLASS
# -------------------------------

class RentalSystem:

    def __init__(self):
        self.vehicles = []
        self.rentals = {}

        self.filename = "vehicles.txt"

        self.load_data()

    # ---------------------------
    # SAVE DATA INTO FILE
    # ---------------------------

    def save_data(self):

        data = {
            "vehicles": [v.to_dict() for v in self.vehicles],
            "rentals": self.rentals
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    # ---------------------------
    # LOAD DATA FROM FILE
    # ---------------------------

    def load_data(self):

        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            for item in data.get("vehicles", []):
                vehicle = Vehicle(
                    item["vehicle_id"],
                    item["vehicle_type"],
                    item["model"],
                    item["rate"],
                    item["available"]
                )

                self.vehicles.append(vehicle)

            self.rentals = data.get("rentals", {})

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: Could not load saved data.")

    # ---------------------------
    # GENERATE VEHICLE ID
    # ---------------------------

    def generate_id(self):

        numbers = []

        for vehicle in self.vehicles:
            try:
                numbers.append(int(vehicle.vehicle_id[1:]))
            except ValueError:
                continue

        next_number = max(numbers, default=0) + 1

        return "V" + str(next_number)

    # ---------------------------
    # ADD VEHICLE
    # ---------------------------

    def add_vehicle(self):

        vehicle_type = input("Type: ").strip()
        model = input("Model: ").strip()

        if not vehicle_type or not model:
            print("Vehicle type and model cannot be empty.")
            return

        try:
            rate = float(input("Rate per day: "))

            if rate <= 0:
                print("Rate must be greater than zero.")
                return

        except ValueError:
            print("Please enter a valid rate.")
            return

        vehicle_id = self.generate_id()

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

            if vehicle.vehicle_id == vehicle_id:
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

        vehicle = self.find_vehicle(vehicle_id)

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

        self.save_data()

        print(f"{vehicle_id} returned. Status: Available")

    # ---------------------------
    # VIEW AVAILABLE VEHICLES
    # ---------------------------

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

if __name__ == "__main__":

    system = RentalSystem()

    system.menu()
