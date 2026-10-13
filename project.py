#Name: Josef Gonzalez
#Student ID:Removed for security purposes
#Course: CTS-153 – Programming for IT
#Assignment: Final Programming Project
#Instructor: Micheal Penta
#This program is a simple user account system that lets people create accounts,
#login, update their password, and keep a log of everything that happens.


def load_user_data(filename):
    user_data = {}
    with open(filename, "r") as file:
        for line in file:
            clean_line = line.strip()

            if clean_line == "":
                continue
            username, password = clean_line.split(":")

            user_data[username] = password

    return user_data

def save_user_data(filename, user_data):

    with open(filename, "w") as file:
        for username, password in user_data.items():
            file.write(username + ":" + password + "\n")

def write_to_log(username, status):
    with open("log.txt", "a") as file:
        line = f"{username} :: [{status}] \n"
        file.write(line)

import random

def create_username(first_name, last_name):
    first_letter = first_name[0].lower()
    last_name = last_name.lower()
    digits = ""
    for i in range(4):
        numbers = random.randint(0,9)
        digit = str(numbers)
        digits = digits + digit
    username = first_letter + last_name + digits
    return username

def get_username():

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    username = create_username(first_name, last_name)
    return username

def test_valid_password(password):
#
   if len(password) < 7:
        return False
   forbidden = "!@:?"
   for ch in password:
       if ch in forbidden:
        return False
   return True

def encrypt_password(password):

    first = password[0]
    middle = password[1:-1]
    last = password[-1]
    new_password = last + middle + first
    new_password = new_password.replace("a","@")
    new_password = new_password.replace("s","$")
    return new_password

def get_password(user_data):

    attempts = 0
    while attempts < 5:
        password1 = input("Enter your Password: ")
        password2 = input("Enter your Password again: ")

        if password1 != password2:
            print("Passwords do not macth!")
            attempts += 1
            continue
        if not test_valid_password(password1):
            print("Password must be at least 7 characters and not contain !, @, $, ?.")
            attempts += 1
            continue
        return password1

    return None

def update_password(user_data, username):
    new_password = get_password(user_data)
    if new_password is None:
        print("Password not updated.")
        return
    new_encrypted = encrypt_password(new_password)
    user_data[username] = new_encrypted
    save_user_data("user_data.txt", user_data)
    write_to_log(username, "UPDATE")

    print("Password updated successfully.")

def add_user(user_data):
    username = get_username()

    if username in user_data:
        print("Username is already taken. Try again.")
        return
    new_password = get_password(user_data)
    if new_password is None:
        print("User not created to many invalid password attempts.")
        return
    new_encrypted = encrypt_password(new_password)

    user_data[username] = new_encrypted

    save_user_data("user_data.txt", user_data)
    write_to_log(username, "NEW USER")
    print("User created successfully. Your new username is: ", username)

def check_user(user_data):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    encrypted = encrypt_password(password)

    if username not in user_data:
       print("User not Found")
       return False, username

    if user_data[username] == encrypted:
        return True, username
    else:
        return False, username

def print_log():

    with open("log.txt", "r") as file:
        for line in file:
            print(line.strip())


def display_main_menu():
    print("\nMain Menu")
    print("1. Login")
    print("2. Create New User")
    print("3. Quit")

    choice = input("Enter your choice (1-3):")
    choice = choice.strip().strip('"').strip("'")
    return choice

def display_user_menu():
    print("\nUser Menu")
    print("1. Print Log")
    print("2. Update Password")
    print("3. Logout")

    choice = input("Enter your choice (1-3):")
    choice = choice.strip().strip('"').strip("'")
    return choice


def main():

    user_data = load_user_data("user_data.txt")

    running = True
    while running:
        choice = display_main_menu()


        if choice == "1":
            success, username = check_user(user_data)

            if success:
                print("Login successful.")
                write_to_log(username, "OK")


                logged_in = True
                while logged_in:
                    user_choice = display_user_menu()

                    if user_choice == "1":
                        print_log()

                    elif user_choice == "2":
                        update_password(user_data, username)

                        user_data = load_user_data("user_data.txt")

                    elif user_choice == "3":
                        print("Logging out.")
                        logged_in = False

                    else:
                        print("Invalid choice. Enter 1-3.")
            else:
                print("Login failed.")
                write_to_log(username, "BAD PASS")


        elif choice == "2":
            add_user(user_data)

            user_data = load_user_data("user_data.txt")


        elif choice == "3":
            print("Goodbye! Have a good day!")
            save_user_data("user_data.txt", user_data)
            running = False

        else:
            print("Invalid choice. Enter 1-3.")

main()






