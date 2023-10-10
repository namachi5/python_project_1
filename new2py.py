import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import filedialog
import os

# Create or connect to the SQLite database
conn = sqlite3.connect('bus_reservation.db')
cursor = conn.cursor()

# Create the necessary tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY,
        bus_number TEXT NOT NULL,
        capacity INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        bus_id INTEGER NOT NULL,
        passenger_name TEXT NOT NULL,
        seat_number INTEGER NOT NULL
    )
''')

conn.commit()

# Function to add a bus
def add_bus():
    bus_number = bus_number_entry.get()
    capacity = capacity_entry.get()
    if bus_number and capacity:
        cursor.execute('INSERT INTO buses (bus_number, capacity) VALUES (?, ?)', (bus_number, capacity))
        conn.commit()
        clear_bus_entries()
        refresh_bus_list()

# Function to add a reservation
def add_reservation():
    bus_id = bus_combobox.get()
    passenger_name = passenger_name_entry.get()
    seat_number = seat_number_entry.get()
    if bus_id and passenger_name and seat_number:
        cursor.execute('INSERT INTO reservations (bus_id, passenger_name, seat_number) VALUES (?, ?, ?)', (bus_id, passenger_name, seat_number))
        conn.commit()
        clear_reservation_entries()
        refresh_reservation_list()

# Function to delete a reservation
def delete_reservation():
    selected_reservation = reservation_listbox.curselection()
    if selected_reservation:
        reservation_id = reservation_listbox.get(selected_reservation[0]).split("-")[0].strip()
        cursor.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
        conn.commit()
        refresh_reservation_list()

# Function to clear bus entry fields
def clear_bus_entries():
    bus_number_entry.delete(0, tk.END)
    capacity_entry.delete(0, tk.END)

# Function to clear reservation entry fields
def clear_reservation_entries():
    passenger_name_entry.delete(0, tk.END)
    seat_number_entry.delete(0, tk.END)

# Function to refresh the bus list
def refresh_bus_list():
    cursor.execute('SELECT * FROM buses')
    buses = cursor.fetchall()
    bus_listbox.delete(0, tk.END)
    for bus in buses:
        bus_listbox.insert(tk.END, f"{bus[1]} - Capacity: {bus[2]}")

# Function to refresh the reservation list
def refresh_reservation_list():
    cursor.execute('SELECT reservations.id, buses.bus_number, reservations.passenger_name, reservations.seat_number FROM reservations INNER JOIN buses ON reservations.bus_id = buses.id')
    reservations = cursor.fetchall()
    reservation_listbox.delete(0, tk.END)
    for reservation in reservations:
        reservation_listbox.insert(tk.END, f"{reservation[0]} - Bus: {reservation[1]} - Passenger: {reservation[2]} - Seat: {reservation[3]}")
def edit_capacity():
    selected_bus = bus_listbox.curselection()
    new_capacity = capacity_entry_edit.get()
    if selected_bus and new_capacity:
        bus_id = bus_listbox.get(selected_bus[0]).split("-")[0].strip()
        cursor.execute('UPDATE buses SET capacity=? WHERE id=?', (new_capacity, bus_id))
        conn.commit()
        refresh_bus_list()
def print_reservation():
    selected_reservation = reservation_listbox.curselection()
    if selected_reservation:
        reservation_id = reservation_listbox.get(selected_reservation[0]).split("-")[0].strip()
        cursor.execute('SELECT * FROM reservations WHERE id=?', (reservation_id,))
        reservation_data = cursor.fetchone()
        if reservation_data:
            # Create a temporary text file to store reservation details
            temp_file_path = "temp_reservation.txt"
            with open(temp_file_path, "w") as temp_file:
                temp_file.write("Bus Reservation System \n\n")
                temp_file.write(f"Reservation ID: {reservation_data[0]}\n")
                temp_file.write(f"Bus ID: {reservation_data[1]}\n")
                temp_file.write(f"Passenger Id: {reservation_data[2]}\n")
                temp_file.write(f"Seat Number: {reservation_data[3]}\n")

            # Open the standard print dialog
            os.system(f"notepad /p {temp_file_path}")

            # Clean up the temporary file
            os.remove(temp_file_path)

# Create the main tkinter window
root = tk.Tk()
root.title("Bus Reservation System")

# Create a frame for bus input fields
bus_frame = ttk.Frame(root)
bus_frame.pack(padx=10, pady=10)

bus_number_label = ttk.Label(bus_frame, text="Bus Number:")
bus_number_label.grid(row=0, column=0, padx=5, pady=5)

bus_number_entry = ttk.Entry(bus_frame)
bus_number_entry.grid(row=0, column=1, padx=5, pady=5)

capacity_label = ttk.Label(bus_frame, text="Capacity:")
capacity_label.grid(row=1, column=0, padx=5, pady=5)

capacity_entry = ttk.Entry(bus_frame)
capacity_entry.grid(row=1, column=1, padx=5, pady=5)

add_bus_button = ttk.Button(bus_frame, text="Add Bus", command=add_bus)
add_bus_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

bus_listbox = tk.Listbox(bus_frame, width=50)
bus_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create a frame for reservation input fields
reservation_frame = ttk.Frame(root)
reservation_frame.pack(padx=10, pady=10)

bus_label = ttk.Label(reservation_frame, text="Select Bus:")
bus_label.grid(row=0, column=0, padx=5, pady=5)

cursor.execute('SELECT * FROM buses')
buses = cursor.fetchall()
bus_combobox = ttk.Combobox(reservation_frame, values=[bus[0] for bus in buses])
bus_combobox.grid(row=0, column=1, padx=5, pady=5)

passenger_name_label = ttk.Label(reservation_frame, text="Passenger Id:")
passenger_name_label.grid(row=1, column=0, padx=5, pady=5)

passenger_name_entry = ttk.Entry(reservation_frame)
passenger_name_entry.grid(row=1, column=1, padx=5, pady=5)

seat_number_label = ttk.Label(reservation_frame, text="Seat Number:")
seat_number_label.grid(row=2, column=0, padx=5, pady=5)

seat_number_entry = ttk.Entry(reservation_frame)
seat_number_entry.grid(row=2, column=1, padx=5, pady=5)

add_reservation_button = ttk.Button(reservation_frame, text="Add Reservation", command=add_reservation)
add_reservation_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

reservation_listbox = tk.Listbox(reservation_frame, width=50)
reservation_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Create a frame for reservation deletion
delete_frame = ttk.Frame(root)
delete_frame.pack(padx=10, pady=10)

delete_reservation_button = ttk.Button(delete_frame, text="Delete Reservation", command=delete_reservation)
delete_reservation_button.grid(row=0, column=0, padx=5, pady=5)

# Add a "Print Reservation" button
print_reservation_button = ttk.Button(delete_frame, text="Print Reservation", command=print_reservation)
print_reservation_button.grid(row=0, column=1, padx=5, pady=5)

# Refresh the lists
refresh_bus_list()
refresh_reservation_list()

root.mainloop()
