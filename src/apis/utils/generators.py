import random


def generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"
