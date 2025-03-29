import os
from random import choice


import base64

folder_path = ".\\images"

file_collections = []
for root, _, files in os.walk(folder_path):
    for file in files:
        file_collections.append(os.path.join(root, file))


def random_file():
    global file_collections
    return choice(file_collections)


def b64_img(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

