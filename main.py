import os, requests, time;from datetime import date; import colorama; from colorama import Fore; from cryptography.fernet import Fernet

# Directory to store the password/logins in
directory = "your dir"

# Variable using datetime module to get current date
today = date.today()

# Fernet key to encrypt files
key = Fernet.generate_key()

# Common variable
fernet_key = Fernet(key)

# Check which os is being used to assign the appropriate terminal command to the variable
if os.name == 'nt':
    # Variable holding appropriate terminal command
    clear_command = "cls"
elif os.name == 'posix':
    clear_command = "clear"

# Menu function
def main_menu():
    option = input("[1] Add Login   [2] View Login  [3] Lock Files  [4] Unlock Files   [5] Load Key: ")
    if option == "1":
        os.system(clear_command)
        add_login()
    elif option == "2":
        os.system(clear_command)
        view_login()
    elif option == "3":
        os.system(clear_command)
        lock_files()
    elif option == "4":
        os.system(clear_command)
        unlock_files()
    elif option == "5":
        os.system(clear_command)
        load_key()

# Add login function that takes in arguments for the login information
def add_login():

    # Global variables for user input for login information
    global site, username, password, email, url
    
    site = input("Enter Site Domain: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    email = input("Enter Email: ")
    
    # Formatting for the get requests
    url = f"https://{site}/"
    add_login_function()

# The function that supports the functionality for the add_login() function, Essentially doing the work
def add_login_function():

    # Sending a get request to the domain to check if the url is valid then write it back into the file
    try:
        get_request_response = requests.get(url)
        if get_request_response.status_code == 200:
            print(f"{Fore.GREEN}[+] URL found{Fore.RESET}")

    except requests.ConnectionError:
        print(f"{Fore.RED}[-] URL not found{Fore.RESET}")

    # Creating file based on the user input for "site" variable as the file name
    file = open(f'creds/{site}.txt', 'x')

    # Format used for writing into the file created
    file.write(f'''Site: {site}\nUsername: {username}\nPassword: {password}\nURL: {url}\nEmail: {email}\nDate: {today}''')
    file.close()

    # After functionality is done to notify you that the login was added
    print(f"[+] Login Added for {site}")
    time.sleep(3)
    os.system(clear_command)
    main_menu()

# Function to view logins in the directory
def view_login():

    # List comprehension to hold file names after iterating over the directory set to "directory" variable
    file_names = [file for file in os.listdir(directory)]

    # Variable as counter to be increased by one for every iteration to serve as a place holder to display
    # file count of each iteration
    count_cursor = 0
    
    # For loop to iterate over elements in "file_names" list and add one to "count+cursor" and print output
    for file in file_names:
        count_cursor+=1
        print(f"File #{count_cursor}:  {file}")

    # Variable to hold user input for chosen file name to open
    choice = input("Which file?: ")

    # If statement to check if user input was found in the "file_names" list
    if choice in file_names:

        print(f"{Fore.GREEN}[+]File Found{Fore.RESET}")

        # Opening file that was used in "choice" and printing what content the file holds into terminal
        with open(f'creds/{file}', 'r+') as file:
            print(file.read())

            # Variable to decide to go back to "main_menu()"
            choice_2 = input("Home? (y/n): ")
            if choice_2 == "y":
                os.system(clear_command)
                main_menu()

    # Else statement for invalid input
    else:
        print(f"{Fore.RED}File doesnt exist{Fore.RESET}")
        time.sleep(3)
        os.system(clear_command)
        main_menu()

# Function to lock all files found in directory
def lock_files():    

    # Iterating through file in the "directory" variable
    for file in os.scandir(directory):

        # Openning each file and reading the concent within in it and encrypting it via fernet
        with open(file, 'rb') as file_content:
            content = file_content.read()
            encrypted_content = fernet_key.encrypt(content)

        # Opening the file again and writing back the encrypted content
        with open(file, 'wb') as file_encrypted:
            file_encrypted.write(encrypted_content)

        # Alert the files have been locked succesfully
        print(f"{Fore.GREEN}[+]Files locked succesfully{Fore.RESET}")
        time.sleep(3)
        os.system(clear_command)
        main_menu()
       

def unlock_files():

    # Iterating through all files in the "directory"
    for file in os.scandir(directory):
        try:    

            # Open every file in the iteration and reading the ecnrypted data and decrypting it
            with open(file, 'rb') as file_content:
                encrypted_content = file_content.read()
                decrypted_content = fernet_key.decrypt(encrypted_content)

            # Opening the file and writing back the decrypted data
            with open(file, 'wb') as file_decrypted_content:
                file_decrypted_content.write(decrypted_content)
                print(f"{Fore.GREEN}[+]Files Unlocked succesfully{Fore.RESET}")

        # Except statement for error checking
        except:
            print("Couldnt unlock file, unknown error")
        time.sleep(3)
        os.system(clear_command)
        main_menu()

# Function to load the generated key into the key file
def load_key():
    with open('config/key.key', 'wb+') as key_file:
        key_file.write(key)

    print("done")
    
        
main_menu()
