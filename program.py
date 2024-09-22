from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from getpass import getpass
from datetime import date

###########################################################################################################################################################################
############################################################## MY DATABASE SETUP ########################################################################################
Base = declarative_base()
engine = create_engine('sqlite:///hotel_reservation.db')
Session = sessionmaker(bind=engine)
session = Session()

#############################################################  MODELS  ################################################################################################
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False,unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False,unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False, unique=True)
    room_type = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    customer = relationship("Customer")
    room = relationship("Room")

Base.metadata.create_all(engine)

##########################################################################################################################################################################
############################################################### MY HELPER FUNCTIONS #######################################################################################
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input
        print("Input cannot be empty.")

def get_non_empty_password(prompt):
    while True:
        password = getpass(prompt)
        if password.strip():
            return password
        print("Password cannot be empty.")

def get_phone_number(prompt):
    while True:
        phone_number=get_non_empty_input(prompt)
        if phone_number.isdigit() and len(phone_number)==10:
            return phone_number
        print("Invalid phone number it must be exactly 10 digits")

######this function prompts the hotel manager to create an account when the program runs and there are no managers in my database .
#firstly i query into the db to check if there are any managers if there are zero number of managers i create a manger 
def create_super_manager():
    if session.query(Manager).count() == 0:
        print("\n--- Super Manager Creation ---")
        first_name = get_non_empty_input("Enter Super Manager's first name: ")
        last_name = get_non_empty_input("Enter Super Manager's last name: ")
        phone = get_phone_number("Enter your phone number it must be 10 digits: ")
        email = get_non_empty_input("Enter Super Manager's email: ")
        password = get_non_empty_password("Enter Super Manager's password: ")

        super_manager = Manager(first_name=first_name, last_name=last_name,phone_number=phone,email=email, password=password)
        session.add(super_manager)
        session.commit()
        print("Super Manager created successfully!")

# Customer and Manager login/register functions
def customer_registration():
    print("\n--- Customer Registration ---")
    first_name = get_non_empty_input("Enter your first name: ")
    last_name = get_non_empty_input("Enter your last name: ")
    phone = get_phone_number("Enter your phone number it must be 10 digits: ")
    email = get_non_empty_input("Enter your email: ")
    password = get_non_empty_password("Create a password: ")

    new_customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone, email=email, password=password)
    try:
        session.add(new_customer)
        session.commit()
        print("Customer registration successful!")
    except:
        session.rollback()
        print("A customer with this phone number or email already exists. Please try again with different details.")
    
    

def customer_login():
    print("\n--- Customer Login ---")
    phone_number=get_phone_number("Enter your phone number:")
    password = get_non_empty_password("Enter your password: ")

    customer = session.query(Customer).filter_by(phone_number=phone_number, password=password).first()
    if customer:
        print(f"Welcome, {customer.first_name}!")
        return customer
    else:
        print("Invalid login credentials.")
        return None

def manager_registration():
    print("\n--- Manager Registration ---")
    first_name = get_non_empty_input("Enter your first name: ")
    last_name = get_non_empty_input("Enter your last name: ")
    phone = get_phone_number("Enter your phone number it must be 10 digits: ")
    email = get_non_empty_input("Enter your email: ")
    password = get_non_empty_password("Create a password: ")

    new_manager = Manager(first_name=first_name, last_name=last_name,phone_number=phone, email=email, password=password)
    try:
        session.add(new_manager)
        session.commit()
        print("Manager registration successful!")
    except:
        session.rollback()
        print("A manager with this phone number or email already exists. Please try again with different details.")

def add_manager():
    print("\n--- Manager Registration ---")
    first_name = get_non_empty_input("Enter Manager first name: ")
    last_name = get_non_empty_input("Enter Manager last name: ")
    phone = get_phone_number("Enter Manager phone number it must be 10 digits: ")
    email = get_non_empty_input("Enter Manager email: ")
    password = get_non_empty_password("Create a password: ")

    new_manager = Manager(first_name=first_name, last_name=last_name,phone_number=phone, email=email, password=password)
    try:
        session.add(new_manager)
        session.commit()
        print("Manager registration successful!")
    except:
        session.rollback()
        print("A manager with this phone number or email already exists. Please try again with different details.")

def manager_login():
    print("\n--- Manager Login ---")
    phone_number=get_phone_number("Enter your phone number:")
    password = get_non_empty_password("Enter your password: ")

    manager = session.query(Manager).filter_by(phone_number=phone_number, password=password).first()
    if manager:
        print(f"Welcome, {manager.first_name}!")
        return manager
    else:
        print("Invalid login credentials.")
        return None

# Room and Reservation functions
def add_room():
    room_number = get_non_empty_input("Enter the room number: ")
    room_type = get_non_empty_input("Enter the room type (e.g., single, double): ")
    price_per_night = float(get_non_empty_input("Enter the price per night: "))

    new_room = Room(room_number=room_number, room_type=room_type, price_per_night=price_per_night, is_available=True)
    session.add(new_room)
    session.commit()
    print(f"Room {room_number} added successfully!")

def view_all_rooms():
    rooms = session.query(Room).all()
    if not rooms:
        print("No rooms found.")
    else:
        for room in rooms:
            status = "Available" if room.is_available else "Booked"
            print(f"Room {room.room_number} - {room.room_type} - KSH.{room.price_per_night}/night - {status}")

def view_available_rooms():
    print("\n--- Available Rooms ---")
    available_rooms = session.query(Room).filter_by(is_available=True).all()
    if not available_rooms:
        print("No rooms are available at the moment.")
    else:
        for room in available_rooms:
            print(f"Room {room.room_number} - {room.room_type} - KSH.{room.price_per_night}/night")
    return available_rooms

def view_all_reservations():
    reservations = session.query(Reservation).all()
    if not reservations:
        print("No reservations found.")
    else:
        for res in reservations:
            customer = session.query(Customer).filter_by(id=res.customer_id).first()
            room = session.query(Room).filter_by(id=res.room_id).first()
            print(f"Reservation id: {res.id} :Reservation for {customer.first_name} {customer.last_name}: Room {room.room_number}, "
                  f"Check-in: {res.check_in_date}, Check-out: {res.check_out_date}, Total Price: KSH.{res.total_price:.2f}")

def cancel_reservation():
    view_all_reservations()
    reservation_id=input("Enter the reservation ID to cancel: ")
    reservation=session.query(Reservation).filter_by(id=reservation_id).first()
    if not reservation:
        print("Reservation not found.")
        return
    room = session.query(Room).filter_by(id=reservation.room_id).first()
    
    if room:
        room.is_available = True
    
    session.delete(reservation)
    session.commit()
    
    print(f"Reservation ID:{reservation_id} has been canceled and room {room.room_number} is now available.")
    
def view_all_customers():
    customers=session.query(Customer).all()
    
    if not customers:
        print("No customers found")
    
    else:
        print("\n -- OUR CUSTOMERS --")
        for customer in customers:
            print(f"ID: {customer.id} - {customer.first_name} {customer.last_name} - Phone: {customer.phone_number} - Email: {customer.email}")
            
def delete_customer():
    view_all_customers()
    customer_id=input("Enter the customer Id to delete : ")
    customer=session.query(Customer).filter_by(id=customer_id).first()
    
    if not customer:
        print("Customer not found.")
        return
    
    session.delete(customer)
    session.commit()
        

def book_room(customer):
    available_rooms = view_available_rooms()

    if not available_rooms:
        print("No rooms available for booking.")
        return

    room_number = get_non_empty_input("Enter the room number you'd like to book: ")
    selected_room = next((room for room in available_rooms if room.room_number == room_number), None)

    if not selected_room:
        print(f"Room {room_number} is not available.")
        return

    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

    try:
        check_in_date_obj = date.fromisoformat(check_in_date)
        check_out_date_obj = date.fromisoformat(check_out_date)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    total_days = (check_out_date_obj - check_in_date_obj).days
    if total_days <= 0:
        print("Invalid check-in/check-out dates.")
        return

    total_price = total_days * selected_room.price_per_night
    new_reservation = Reservation(room_id=selected_room.id, customer_id=customer.id,
                                  check_in_date=check_in_date_obj, check_out_date=check_out_date_obj, total_price=total_price)

    selected_room.is_available = False
    session.add(new_reservation)
    session.commit()

    print(f"Room {room_number} successfully booked!")
    print(f"Total price: KSH.{total_price:.2f}")

def make_reservation_for_customer():
    print("\n--- Make Reservation for Customer ---")

    email = get_non_empty_input("Enter the customer's email: ")
    customer = session.query(Customer).filter_by(email=email).first()

    if not customer:
        print("Customer not found. Creating a new customer.")
        first_name = get_non_empty_input("Enter customer's first name: ")
        last_name = get_non_empty_input("Enter customer's last name: ")
        phone = get_non_empty_input("Enter customer's phone number: ")
        password = get_non_empty_password("Enter a password for the customer: ")

        customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone, email=email, password=password)
        session.add(customer)
        session.commit()
        print(f"Customer {first_name} {last_name} created successfully!")

    available_rooms = view_available_rooms()

    if not available_rooms:
        print("No rooms are available for booking.")
        return

    room_number = get_non_empty_input("Enter the room number you'd like to book: ")

    selected_room = next((room for room in available_rooms if room.room_number == room_number), None)

    if not selected_room:
        print(f"Room {room_number} is not available.")
        return

    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

    try:
        check_in_date_obj = date.fromisoformat(check_in_date)
        check_out_date_obj = date.fromisoformat(check_out_date)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    total_days = (check_out_date_obj - check_in_date_obj).days
    if total_days <= 0:
        print("Invalid check-in/check-out dates.")
        return

    total_price = total_days * selected_room.price_per_night
    new_reservation = Reservation(room_id=selected_room.id, customer_id=customer.id,
                                  check_in_date=check_in_date_obj, check_out_date=check_out_date_obj, total_price=total_price)

    selected_room.is_available = False
    session.add(new_reservation)
    session.commit()

    print(f"Room {room_number} has been successfully booked for {customer.first_name} {customer.last_name}!")
    print(f"Total price: KSH.{total_price:.2f}")

def manager_menu(manager):
    while True:
        print("\n--- Manager Menu ---")
        print("1. Add Room")
        print("2. View All Rooms")
        print("3. View All Reservations")
        print("4. Create Reservation for Customer")
        print("5. Add Manager")
        print("6. Cancel Reservation")
        print("7. Delete Customer")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_room()
        elif choice == "2":
            view_all_rooms()
        elif choice == "3":
            view_all_reservations()
        elif choice == "4":
            make_reservation_for_customer()
        elif choice=="5":
            add_manager()
        elif choice=="6":
            cancel_reservation()
        elif choice=="7":
            delete_customer()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    #i would like when the program runs for the first time it checks whether there is a manager in the db,if there is no manager ,we are prompted to create a manager
    create_super_manager()  

    while True:
        print("\n--- Hotel Reservation System ---")
        print("1. Customer Login")
        print("2. Customer sign up")
        print("3. Manager Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer = customer_login()
            if customer:
                while True:
                    print("\n--- Customer Menu ---")
                    print("1. View Available Rooms")
                    print("2. Book a Room")
                    print("3. Logout")

                    customer_choice = input("Enter your choice: ")

                    if customer_choice == "1":
                        view_available_rooms()
                    elif customer_choice == "2":
                        book_room(customer)
                    elif customer_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice=="2":
            customer_registration()
        elif choice == "3":
            manager = manager_login()
            if manager:
                manager_menu(manager)
        elif choice == "4":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
