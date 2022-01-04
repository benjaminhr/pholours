import cv2
import glob
import pathlib
import numpy as np
from numpy.linalg import norm

PHOTO_FOLDER = str(pathlib.Path("./output-colours").resolve())
photo_files = glob.glob(PHOTO_FOLDER + "/*")

images = []

for photo_path in photo_files:
    img = cv2.imread(photo_path)
    images.append(img)

color = [255, 255, 255]  # white
top, bottom, left, right = [200, 200, 100, 100]

# sort images by lightness (dark => light)
images.sort(key=lambda img: np.average(
    norm(img, axis=2)) / np.sqrt(3))

# create one large image of light strips
full_image = cv2.vconcat(images)
# full_image = cv2.resize(full_image, (4000,  1000))
# full_image = cv2.copyMakeBorder(
#     full_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite(f"test.jpg", full_image)
