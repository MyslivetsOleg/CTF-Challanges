def calculate_stego(text):
    resulting_stego = ""
    for symbol in text:
        if symbol == " ":
            resulting_stego += '0'
        if symbol == '\xa0':
            resulting_stego += '1'
    return resulting_stego

file_content = []
FILE_DIR = "/home/fakalor/Downloads/Stego/text_stego/stego_poeli_w.txt"
with open(FILE_DIR, 'r', encoding='utf-8') as file:
    file_content = file.readlines()
file_content = "".join(file_content)
# print(file_content)
stego_txt = calculate_stego(file_content)
print(stego_txt)
