import base64


def find_base64_image(data: list) -> str:
    ppc2_image = ""
    for item in data:
        if item:
            if item[0] == 'b':
                ppc2_image = item
    return ppc2_image[2:-1]


def get_image_from_raw_data(data: bytes) -> str:
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
