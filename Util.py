import hashlib


def append_array_to_array(array, array_to_append):
    for element in array_to_append:
        array.append(element)
    return array

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()