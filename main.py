import json
import re
import random
import string
import os

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# salasanan vahvuuden tarkistus
def is_strong_password(password):
    # Pituuden tarkistus
    if len(password) < 8:
        return False
    
    # Tarkistetaan, etta loytyy pienia ja isoja kirjaimia, numeroita ja erikoismerkkeja
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"\W", password):
        return False
    
    # Tarkistetaan, etta salasanassa on kaytetty kutakin kirjainta vain kerran (tama kommentoitu pois testaamisen helpottamiseksi) 
    #if len(set(password)) < len(password):
        #return False

    return True

# Salasanan generointi funktio
def generate_password(length):

    # varmistetaan toivottu salasanan pituus
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    # generoidaan yksi merkki kustakin kirjaisintyypista, jotta voidaan varmistua etta salasanassa on vahintaan yksi kutakin
    characters = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # lisataan loput merkit salasanaan ja sekoitetaan, jonka jalkeen palautetaan merkkijonona
    characters += [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length - 4)]
    random.shuffle(characters)

    return ''.join(characters)


# Tyhjat listat
encrypted_passwords = []
websites = []
usernames = []

# Salasanan lisays funktio 
def add_password(website, username, password):

    while True:

        #mikali salasanaksi annettu "generate", syotetaan salasanan generointi toimintoon randomisoitu pituus
        if password == "generate":
            password = generate_password(random.randint(8, 20))
        
        #mikali annettu salasana ei ole riittavan vahva, pyydetaan salasana uudestaan
        if not is_strong_password(password):
            print("Password is not strong enough. Please try again.")
            password = input("Enter the password (or 'generate' to create a random one, or 'back' to return to the main menu): ")
            if password.lower() == 'back':
                return
            continue
        
        shift = int(5)  #Cesar_cryptaus funktiolle syotettava shift-arvo 

        #cryptattujen salasanojen, nettisivujen ja kayttajien lisays listoihin
        encrypted_passwords.append(caesar_encrypt(password, shift))
        websites.append(website)
        usernames.append(username)
        break
# salasanojen haku
def get_password(website):
    # nettisivun perusteella kayttajatunnusten ja salasanojen haku
    if website in websites:
        index = websites.index(website)
        username = usernames[index]
        encrypted_password = encrypted_passwords[index]
        #salasanojen decryptaus ennen tulostusta
        decrypted_password = caesar_decrypt(encrypted_password, 5)
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}")
    else:
        print("Website not found in the vault.")

# Funktio jolla salasanat tallennetaan json tiedostoon
def save_passwords(filename):
    #listojen tallennus tiedostoon, salasanat cryptatussa muodossa
    with open(filename, 'w') as f:
        json.dump({
            'websites': websites,
            'usernames': usernames,
            'encrypted_passwords': encrypted_passwords
        }, f)
    print(f"Passwords saved successfully to {filename}.")

# Salasanojen haku tiedostosta
def load_passwords(filename):
   

    global websites, usernames, encrypted_passwords  # muutetaan globaaleja listoja tiedoston mukaisiksi
    while True:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                websites = data['websites']
                usernames = data['usernames']
                encrypted_passwords = data['encrypted_passwords']
            print(f"Passwords loaded successfully from {filename}!")
            break
        # jos tiedostonimi on vaara, annetaan error ja pyydetaan oikeaa tiedostonimea
        except FileNotFoundError:
            print("Error: File not found. Please provide a valid filename.")
            filename = input("Enter the filename (or 'back' to return to the main menu): ")
            if filename.lower() == 'back':
                return
            continue

  # Main method
def main():
# kayttoliittyma annetun mukainen

  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")
    
    choice = input("Enter your choice: ")
    
    #lisattu kentat tietojen antamista varten tanne kayttoliittymaan
    if choice == "1":
        website = input("Enter the website (or 'back' to return to the main menu): ")
        if website.lower() == 'back':
            continue
        username = input("Enter the username (or 'back' to return to the main menu): ")
        if username.lower() == 'back':
            continue
        password = input("Enter the password (or 'generate' to create a random one, or 'back' to return to the main menu): ")
        if password.lower() == 'back':
            continue
        add_password(website,username,password)
    elif choice == "2":
        website = input("Enter the website (or 'back' to return to the main menu): ")
        if website.lower() == 'back':
            continue
        get_password(website)
    elif choice == "3":
        filename = input("Enter the filename (or 'back' to return to the main menu): ")
        if filename.lower() == 'back':
            continue
        save_passwords(filename)
    elif choice == "4":
        filename = input("Enter the filename (or 'back' to return to the main menu): ")
        if filename.lower() == 'back':
            continue
        load_passwords(filename)

    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
