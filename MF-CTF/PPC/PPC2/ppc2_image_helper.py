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
