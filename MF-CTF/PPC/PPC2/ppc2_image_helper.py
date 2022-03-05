import base64
import hashlib


def find_base64_image(data: list) -> str:
    ppc2_image = ""
    for item in data:
        if item:
            if item[0] == 'b':
                ppc2_image = item
    return ppc2_image[2:-1]


def get_b64image_from_raw_data(data: bytes) -> str:
    data = data.decode('utf-8').split("\n")
    return find_base64_image(data)


def get_correct_answer(data: str) -> str:
    """

    :rtype: object
    """
    data = data.split(":")
    return data[1].strip()


def is_correct_image(data: str, check_header="PNG") -> bool:
    if check_header in str(base64.urlsafe_b64decode(data)):
        return True
    return False


def is_correct_answer(answer, check_pattern='&') -> bool:
    if check_pattern in answer:
        return True
    return False


def append_image_length(b64image: str, length=2048) -> str:
    if len(b64image) < length:
        while len(b64image) != length:
            b64image += '0'
    return b64image


def calculate_b64img_hash(b64image: str, length=2048) -> str:
    if len(b64image) < length:
        b64image = append_image_length(b64image)
    b64image = b64image[0:length]
    img_hash = hashlib.md5(b64image.encode('utf-8')).hexdigest()
    return img_hash
