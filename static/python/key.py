from cryptography.fernet import Fernet

def main():
    # Generate the two keys
    # KEY is used to crypt the name of the articles
    KEY = Fernet.generate_key()
    # APP_KEY is used by the Flask app to encode the session cookies
    APP_KEY = Fernet.generate_key()

    # Writing the two keys in a .env file
    dotenvFile = open(".env", "w", encoding='utf8')
    dotenvFile.write("KEY = '" + str(KEY.decode()) + "'\nAPP_KEY = '" + str(APP_KEY.decode()) + "'")
    dotenvFile.close()

if __name__ == "__main__":
    main()