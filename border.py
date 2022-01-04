import cv2
import pathlib
import glob
import os

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

for photo_path in photo_files:
    img = cv2.imread(photo_path)

    img = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    filename = os.path.basename(photo_path)
    month_taken = month_mappings[filename[:2]]
    font = cv2.FONT_HERSHEY_TRIPLEX

    cv2.putText(img, month_taken, (400, 390), font,
                2, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imwrite(f"{OUTPUT_FOLDER}/{filename}", img)
