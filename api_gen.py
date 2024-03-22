import secrets

# Generate a random 32-character API key
API_KEY = secrets.token_hex(16)
print("Generated API Key:", API_KEY)