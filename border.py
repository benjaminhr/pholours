import cv2
import pathlib
import glob
import os
import numpy as np
from numpy.linalg import norm

OUTPUT_FOLDER = str(pathlib.Path("./output-border").resolve())
PHOTO_FOLDER = str(pathlib.Path("./output-colours").resolve())
photo_files = glob.glob(PHOTO_FOLDER + "/*")

color = [255, 255, 255]  # white
top, bottom, left, right = [200, 200, 100, 100]

month_mappings = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

images = []

for photo_path in photo_files:
    img = cv2.imread(photo_path)
    images.append({
        "path": photo_path,
        "image": img
    })

images.sort(key=lambda img: np.average(
    norm(img["image"], axis=2)) / np.sqrt(3))

print(len(images))
remove = 300
images = images[remove:]
print(len(images))

for imageObject in images:
    image = imageObject["image"]
    path = imageObject["path"]

    img = cv2.copyMakeBorder(
        image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    filename = os.path.basename(path)
    month_taken = month_mappings[filename[:2]]
    font = cv2.FONT_HERSHEY_TRIPLEX
    textsize = cv2.getTextSize(month_taken, font, 1, 2)[0]
    textX = ((img.shape[1] - textsize[0]) // 2) - 60

    cv2.putText(img, month_taken, (textX, 390), font,
                2, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imwrite(f"{OUTPUT_FOLDER}/{filename}", img)
