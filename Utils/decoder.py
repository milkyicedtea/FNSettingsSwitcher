import base64


def decode(string):
    string_bytes = string.encode('UTF-8')
    decoded_string = base64.b64decode(string_bytes).decode('UTF-8')

    return decoded_string
