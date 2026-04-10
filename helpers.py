import random
import string

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_payload(email=None, password=None, name=None):
    return {
        "email": email or f"{generate_random_string(8)}@yandex.ru",
        "password": password or generate_random_string(8),
        "name": name or generate_random_string(8)
    }
