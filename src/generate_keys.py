import secrets

def generate_secret_keys():
    # Generate a SECRET_KEY
    secret_key = secrets.token_hex(32)
    print(f'SECRET_KEY={secret_key}')

    # Generate a JWT_SECRET_KEY
    jwt_secret_key = secrets.token_hex(32)
    print(f'JWT_SECRET_KEY={jwt_secret_key}')

if __name__ == "__main__":
    generate_secret_keys()
