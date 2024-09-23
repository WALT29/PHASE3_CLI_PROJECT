# Hotel Reservation System  13th/Sept/2024

**BY Walter David Irungu**

This project is a CLI hotel reservation system built with Python and SQLite. It allows customers to register, log in, and book rooms, while managers can add a room ,add a reservation for a customer ,view all reservations,uncheck a reservation and remove a customer from the sytem

## Problem statement
Managing hotel reservations efficiently is crucial for both customers and hotel staff. However, manual processes and outdated systems can lead to double bookings, unavailability of real-time room information, and delays in handling customer queries.

## Solution statement
The project will involve building a command-line interface (CLI) hotel reservation system using Python and SQLite. The system will allow users to book rooms, cancel reservations, check room availability, and view booking details. The system will store hotel room information, customer details, and reservation data in an SQLite database. 

## Mvp features
    1.ROOM MANAGEMENT
        Customers can view available rooms
        Manager can add a new room (type,price)
        When a room is booked the status will be indicated (Update room status)
    
    2.CUSTOMER MANAGEMENT
        Adding a new customer to the db with their customer view customer info
    
    3.BOOKING MANAGEMENT
        Make a reservation by selecting a room or Table
    
    4.ROOM AVAILABILITY
        Check if a room is available
    
    5.LOGIN AND AUTHENTICATION
        Customers and managers can login into their different account based on their credentials on the database
    
    6.DB MANAGEMENT
        sql to store manager,customer and room info and booking info CRUD operations


## Installation

1. **Clone the reposistory in your local directory:**
   - git clone git@github.com:WALT29/PHASE3_CLI_PROJECT.git

2. **On your terminal, cd into your directory**

3. **pipenv**
    - to install pipenv ,just write `pipenv install` on your terminal
    - make sure you change the python version in the `pipfile` to match your machine python version
    - after the installation type `pipenv shell` 
    - if you dont have the `sqlalchemy` type , `pip install sqlalchemy` while you are in the pipenv virtual environment

4. **running the program**
    - To run the program in the terminal type `python program.py` while still you are in the virtual environment
   https://github.com/user-attachments/assets/bb6af83a-923d-4935-97b8-cf5d794463b6
