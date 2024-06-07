from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Test password and hash
password = "hiba"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
print(f"Hashed password: {hashed_password}")

# Verify password
password_check = bcrypt.check_password_hash(hashed_password, password)
print(f"Password check: {password_check}")
