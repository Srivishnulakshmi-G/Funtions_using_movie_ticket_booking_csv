import csv
import os

LOGIN_FILE = "login.csv"
MOVIE_FILE = "seats.csv"
BOOKING_FILE = "bookings.csv"
 #hgjhg
def load_login():
    with open(LOGIN_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            return int(row["login_id"]), int(row["password"])

def login():
    stored_id, stored_pass = load_login()

    loginId = int(input("Enter your Login ID: "))
    password = int(input("Enter your Password: "))

    if loginId == stored_id and password == stored_pass:
        print("Login Successful")
        return True
    else:
        print("Invalid Login")
        return False

def change_credentials():
    new_id = int(input("Enter new Login ID: "))
    new_pass = int(input("Enter new Password: "))

    with open(LOGIN_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["login_id", "password"])
        writer.writerow([new_id, new_pass])

    print("Login credentials updated successfully")

def load_movies():
    tamil_seats = {}
    english_seats = {}

    with open(MOVIE_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["category"] == "Tamil":
                tamil_seats[int(row["movie_id"])] = int(row["seats"])
            else:
                english_seats[int(row["movie_id"])] = int(row["seats"])

    return tamil_seats, english_seats


def update_movie_seats(category, movie_id, new_seats):
    rows = []

    with open(MOVIE_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["category"] == category and int(row["movie_id"]) == movie_id:
                row["seats"] = str(new_seats)
            rows.append(row)

    with open(MOVIE_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def save_booking(movie, category, seats, amount):
    file_exists = os.path.isfile(BOOKING_FILE)

    with open(BOOKING_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["movie", "category", "seats", "amount"])
        writer.writerow([movie, category, seats, amount])


def check_availability(tamil_seats, english_seats, tamil_movies, english_movies):
    print("\n1. Tamil Movies")
    print("2. English Movies")
    cat = int(input("Select category: "))

    if cat == 1:
        movies = tamil_movies
        seats = tamil_seats
    elif cat == 2:
        movies = english_movies
        seats = english_seats
    else:
        print("Invalid category")
        return

    for k, v in movies.items():
        print(k, "-", v)

    choice = int(input("Choose movie to check availability: "))

    if choice in seats:
        print(f"Available seats for {movies[choice]}: {seats[choice]}")
    else:
        print("Invalid movie selection")


def get_seat_count():
    while True:
        seats = int(input("Enter number of seats: "))
        if seats <= 0:
            print("Seats must be greater than zero")
        else:
            return seats


def payment(seats):
    choice = int(input("Payment Method [1-GPay / 2-PhonePe]: "))

    if choice == 1:
        amount = seats * 120
    elif choice == 2:
        amount = seats * 125
    else:
        print("Invalid payment option")
        return False, 0

    print("Total Amount:", amount)
    confirm = int(input("Confirm payment? YES-1 / NO-2: "))

    if confirm == 1:
        print("Payment Successful")
        return True, amount
    else:
        print("Payment Cancelled")
        return False, 0


def book_movie(movie_seats, movie_names, category):
    print("\nMovies List:")
    for k, v in movie_names.items():
        print(k, "-", v)

    choice = int(input("Choose movie: "))

    if choice not in movie_seats:
        print("Invalid movie selection")
        return movie_seats

    seats = get_seat_count()

    if seats > movie_seats[choice]:
        print("Not enough seats available")
        return movie_seats

    success, amount = payment(seats)

    if success:
        movie_seats[choice] -= seats
        update_movie_seats(category, choice, movie_seats[choice])
        save_booking(movie_names[choice], category, seats, amount)
        print("Booking successful for", movie_names[choice])
    else:
        print("Booking failed")

    return movie_seats

def main():
    tamil_movies = {
        1: "RRR", 2: "LEO", 3: "JOE", 4: "PADAYAPPA", 5: "LYK"
    }
    english_movies = {
        1: "Jaws", 2: "Dune", 3: "Heat", 4: "Reds", 5: "Babe"
    }

    tamil_seats, english_seats = load_movies()

    while True:
        if not login():
            continue

        while True:
            print("\n1. Tamil Movies")
            print("2. English Movies")
            print("3. Change Login")
            print("4. Logout")
            print("5. Exit")
            print("6. Check Seat Availability")

            ch = int(input("Enter choice: "))

            if ch == 1:
                tamil_seats = book_movie(tamil_seats, tamil_movies, "Tamil")

            elif ch == 2:
                english_seats = book_movie(english_seats, english_movies, "English")

            elif ch == 3:
                change_credentials()
                break

            elif ch == 4:
                print("Logged out successfully")
                break

            elif ch == 5:
                print("Thank you for using Movie Booking System")
                return

            elif ch == 6:
                check_availability(
                    tamil_seats, english_seats,
                    tamil_movies, english_movies
                )

            else:
                print("Invalid choice")
main()
