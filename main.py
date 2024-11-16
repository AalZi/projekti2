import json
import re
import random
import string
import os

# Caesar-salauksen salaus ja purku (esitoteutettu)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                while shifted > ord('z'):
                    shifted -= 26
                while shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                while shifted > ord('Z'):
                    shifted -= 26
                while shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Salasanan vahvuuden tarkistus
def is_strong_password(password):
    # Tarkistetaan pituus
    if len(password) < 8:
        return False
    
    # Tarkistetaan, että löytyy pieniä ja isoja kirjaimia, numeroita ja erikoismerkkejä
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"\W", password):
        return False
    
    # Tarkistetaan, että salasanassa ei ole toistuvia merkkejä (kommentoitu pois helpomman testauksen vuoksi)
    #if len(set(password)) < len(password):
        #return False

    return True

# Salasanan generointifunktio
def generate_password(length):

    # Varmistetaan toivottu salasanan pituus
    if length < 8:
        raise ValueError("Salasanan pituuden tulee olla vähintään 8 merkkiä.")

    # Generoidaan yksi merkki kustakin merkistötyypistä, jotta varmistetaan vähintään yksi kutakin
    characters = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Lisätään loput merkit salasanaan ja sekoitetaan, jonka jälkeen palautetaan merkkijonona
    characters += [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length - 4)]
    random.shuffle(characters)

    return ''.join(characters)


# Tyhjät listat
encrypted_passwords = []
websites = []
usernames = []

# Salasanan lisäystoiminto
def add_password():
    while True:
        website = input("Enter the website name (or type 'back' to return to the main menu): ")
        if website.lower() == 'back':
            print("Returning to the main menu.")
            return
        username = input("Enter the username (or type 'back' to return to the main menu): ")
        if username.lower() == 'back':
            print("Returning to the main menu.")
            return
        password = input("Enter the password (or 'generate' to create a random one, or type 'back' to return): ")
        if password.lower() == 'back':
            print("Returning to the main menu.")
            return
        while True:
            if password == "generate":
                password = generate_password(random.randint(8, 20))
                print(f"Generated password: {password}")
            if not is_strong_password(password):
                print("Password is not strong enough. Please try again.")
                password = input("Enter the password (or 'generate' to create a random one, or 'back' to return): ")
                if password.lower() == 'back':
                    print("Returning to the main menu.")
                    return
                continue
            shift = 5  # Siirtoarvo Caesar-salausfunktiolle
            encrypted_passwords.append(caesar_encrypt(password, shift))
            websites.append(website)
            usernames.append(username)
            print("Password added successfully.")
            return

# Salasanan hakutoiminto
def get_password():
    while True:
        website = input("Enter the website name (or type 'back' to return to the main menu): ")
        if website.lower() == 'back':
            print("Returning to the main menu.")
            return
        # Haetaan käyttäjätunnukset ja salasanat verkkosivun perusteella
        if website in websites:
            index = websites.index(website)
            username = usernames[index]
            encrypted_password = encrypted_passwords[index]
            # Puretaan salasanat ennen tulostusta
            decrypted_password = caesar_decrypt(encrypted_password, 5)
            print(f"Username: {username}")
            print(f"Password: {decrypted_password}")
            return
        else:
            print("Website not found in the vault.")
            return

# Funktio salasanojen tallentamiseen JSON-tiedostoon
def save_passwords():
    while True:
        filename = input("Enter the filename to save to (or type 'back' to return to the main menu): ")
        if filename.lower() == 'back':
            print("Returning to the main menu.")
            break
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'websites': websites,
                    'usernames': usernames,
                    'encrypted_passwords': encrypted_passwords
                }, f)
            print(f"Passwords saved successfully to {filename}.")
            break
        except Exception as e:
            print(f"An error occurred: {e}. Please try again or type 'back' to return to the main menu.")

# Funktio salasanojen lataamiseen tiedostosta
def load_passwords():
    global websites, usernames, encrypted_passwords  # Päivitetään globaalit listat tiedoston perusteella
    while True:
        filename = input("Enter the filename (or type 'back' to return to the main menu): ")
        if filename.lower() == 'back':
            print("Returning to the main menu.")
            break
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                websites = data['websites']
                usernames = data['usernames']
                encrypted_passwords = data['encrypted_passwords']
            print(f"Passwords loaded successfully from {filename}!")
            break
        except FileNotFoundError:
            print("Error: File not found. Please provide a valid filename or type 'back' to return to the main menu.")
        except json.JSONDecodeError:
            print("Error: File is not in the correct format. Please try again or type 'back' to return to the main menu.")

# Pääohjelma
def main():
    # Käyttöliittymä
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Save Passwords")
        print("4. Load Passwords")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            get_password()
        elif choice == "3":
            save_passwords()
        elif choice == "4":
            load_passwords()
        elif choice == "5":
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
