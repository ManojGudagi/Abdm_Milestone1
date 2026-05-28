import base64


def encrypt_data(data: str):
    return base64.b64encode(data.encode()).decode()


def decrypt_data(encoded_data: str):
    return base64.b64decode(encoded_data.encode()).decode()