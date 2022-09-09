import os, requests, time;from datetime import date; import colorama; from colorama import Fore; from cryptography.fernet import Fernet

directory = "C:\\Users\\crese\\Downloads\\Important\\Coding\\Coding\\python\\PW manager\\creds\\"
today = date.today()
key = Fernet.generate_key()

with open('config/key.key', 'wb') as kf:
    kf.write(key)
with open('config/key.key', 'rb') as fk:
    key = fk.read()

if os.name == 'nt':
    cmd = "cls"
elif os.name == 'posix':
    cmd = "clear"

def main_menu():
    option = input("[1] Add Login   [2] View Login  [3] Lock Files  [4] Unlock Files: ")
    if option == "1":
        os.system(cmd)
        add_login()
    elif option == "2":
        os.system(cmd)
        view_login()
    elif option == "3":
        os.system(cmd)
        lock_files()
    elif option == "4":
        os.system(cmd)
        unlock_files()

def add_login():
    site = input("Enter Site Domain: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    email = input("Enter Email: ")
    url = f"https://{site}/"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(f"{Fore.GREEN}[+] URL found{Fore.RESET}")

    except requests.ConnectionError:
        print(f"{Fore.RED}[-] URL not found{Fore.RESET}")

    file = open(f'creds/{site}.txt', 'x')
    file.write(f'''
Site: {site}
Username: {username}
Password: {password}
URL: {url}
Email: {email}
Date: {today}''')
    file.close()
    print(f"[+] Login Added for {site}")
    time.sleep(3)
    os.system(cmd)
    main_menu()

def view_login():
    file_names = []
    for file in os.listdir(directory):
        file_names.append(file)
        count = 0
        print(f"File #{count+1}:  {file}")

    choice = input("Which file?: ")
    if choice in file_names:
        print(f"{Fore.GREEN}[+]File Found{Fore.RESET}")
        with open(f'creds/{file}', 'r+') as f:
            print(f.read())
            choice_2 = input("Home? (y/n): ")
            if choice_2 == "y":
                os.system(cmd)
                main_menu()
    else:
        print(f"{Fore.RED}File doesnt exist{Fore.RESET}")
        time.sleep(3)
        os.system(cmd)
        main_menu()

def lock_files():
    fk = Fernet(key)
    for file in os.scandir(directory):
        with open(file, 'rb') as file_c:
            content = file_c.read()
            e_data = fk.encrypt(content)
        with open(file, 'wb') as file_e:
            file_e.write(e_data)
        print(f"{Fore.GREEN}[+]Files locked succesfully{Fore.RESET}")
        time.sleep(3)
        os.system(cmd)
        main_menu()

def unlock_files():
    fk = Fernet(key)
    for file in os.scandir(directory):
        with open(file, 'rb') as file_c:
            e_data = file_c.read()
            d_data = fk.decrypt(e_data)
        with open(file, 'wb') as file_e:
            file_e.write(d_data)
        print(f"{Fore.GREEN}[+]Files Unlocked succesfully{Fore.RESET}")
        time.sleep(3)
        os.system(cmd)
        main_menu()

main_menu()