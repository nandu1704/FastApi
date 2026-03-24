import hashlib
 # 16 bytes random salt
password = "MySecret123"

# Hash password + salt using SHA-256
hash_object = hashlib.sha256(password.encode())
hashed_password = hash_object.hexdigest()

print("Hash:", hashed_password)