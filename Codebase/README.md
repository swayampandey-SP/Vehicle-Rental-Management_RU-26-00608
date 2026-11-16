# Vehicle Rental Management System

A simple command-line application, written in Python, for managing a small vehicle rental business. It lets you add vehicles, rent them out to customers, process returns, and view the fleet. All data is saved automatically to a local file, so nothing is lost between runs.

## Features

- **Add vehicles** with a type, model and daily rate. IDs are generated automatically (`V1`, `V2`, `V3`, ...).
- **Rent a vehicle** to a customer for a number of days, with the bill calculated automatically.
- **Automatic discount:** 10% off for rentals of 7 days or more.
- **Return a vehicle** and mark it available again.
- **View all vehicles** with their current status (Available / Rented).
- **Persistent storage:** data is saved to `vehicles.txt` in JSON format after every change.
- **Input validation:** empty fields, non-numeric values, non-positive rates, invalid day counts, unknown IDs and double rentals or returns are all handled with clear messages.

## Requirements

- Python 3.6 or higher
- No external libraries needed (uses only the built-in `json` and `os` modules)

## Getting Started

1. Save the script as `vehicle_rental.py`.
2. Open a terminal in the folder containing the file.
3. Run:

   ```bash
   python vehicle_rental.py
   ```

The first run creates `vehicles.txt` automatically once you add your first vehicle.

## Usage

The program shows a menu:

```
================================
   VEHICLE RENTAL MANAGEMENT
================================
1. Add Vehicle
2. Rent Vehicle
3. Return Vehicle
4. View Vehicles
5. Exit
```

### 1. Add Vehicle
Enter the vehicle type (e.g. `Car`, `Bike`), model and rate per day. A unique ID is assigned.

```
Type: Car
Model: Swift
Rate per day: 1500
Vehicle added. ID: V1 | Car | Swift | Rs. 1500/day | Available
```

### 2. Rent Vehicle
Enter the vehicle ID, customer name and number of days.

```
Vehicle ID: V1
Customer: Rahul
Days: 7
V1 rented to Rahul for 7 days. 10% discount applied. Bill: Rs. 9450
```

### 3. Return Vehicle
Enter the vehicle ID. The rental record is removed and the vehicle becomes available again.

### 4. View Vehicles
Lists every vehicle:

```
V1 | Car | Swift | Rs. 1500/day | Available
V2 | Bike | Splendor | Rs. 500/day | Rented
```

### 5. Exit
Closes the program. Data has already been saved after each operation.

## Billing Rules

| Rental length | Bill |
|---------------|------|
| 1-6 days      | `rate x days` |
| 7+ days       | `rate x days`, minus 10% |

## Data Storage

All data is stored in `vehicles.txt` (in the folder where you run the program) as JSON:

```json
{
    "vehicles": [
        {
            "vehicle_id": "V1",
            "vehicle_type": "Car",
            "model": "Swift",
            "rate": 1500.0,
            "available": false
        }
    ],
    "rentals": {
        "V1": {
            "customer": "Rahul",
            "days": 7,
            "bill": 9450.0
        }
    }
}
```

If the file is corrupted or has an unexpected structure, the program prints a warning and starts with an empty fleet.

## Project Structure

```
.
├── vehicle_rental.py   # Main program
└── vehicles.txt        # Auto-generated data file
```

### Code Overview

| Class / Method | Purpose |
|----------------|---------|
| `Vehicle` | Represents a single vehicle (ID, type, model, rate, availability). Includes `display()` and `to_dict()`. |
| `RentalSystem` | Core logic and menu handling. |
| `save_data()` / `load_data()` | Write to and read from `vehicles.txt`. |
| `generate_id()` | Creates the next unique vehicle ID. |
| `add_vehicle()`, `rent_vehicle()`, `return_vehicle()`, `view_vehicles()` | Menu actions. |
| `find_vehicle()` | Looks up a vehicle by ID. |

## Possible Improvements

- Search and filter vehicles by type or availability
- Rental history and revenue reports
- Remove or edit vehicles
- Case-insensitive vehicle ID entry
- Late-return fees and rental dates
- A GUI or web interface

## License

This project is free to use and modify for learning and personal projects.
