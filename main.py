import os
import pathlib
import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime

PICS_PATH = str(pathlib.Path("./input-images").resolve())
TEST_PICS_PATH = str(pathlib.Path("./test_pics").resolve())

# get all input files and sort by modification time
photo_files = sorted(pathlib.Path(PICS_PATH).iterdir(), key=os.path.getmtime)
# to string
photo_files = [str(path) for path in photo_files]

OUTPUT_FOLDER = str(pathlib.Path("./output-colours").resolve())


def visualize_colors(cluster, centroids):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((70, 1000, 3), dtype=np.uint8)
    colors = sorted([(percent, color)
                    for (percent, color) in zip(hist, centroids)])
    start = 0
    for (percent, color) in colors:
        print(color, "{:0.2f}%".format(percent * 100))
        end = start + (percent * 1000)
        cv2.rectangle(rect, (int(start), 0), (int(end), 70),
                      color.astype("uint8").tolist(), -1)
        start = end
    return rect


def show_colours(image_path):
    # Load image and convert to a list of pixels
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))

    # Find and display most dominant colors
    cluster = KMeans(n_clusters=7).fit(reshape)
    visualize = visualize_colors(cluster, cluster.cluster_centers_)
    visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
    return visualize


for path in photo_files:
    if not (path.endswith(".jpg") or path.endswith(".png")):
        continue

    last_modified_timestamp = int(os.path.getmtime(path))
    timestamp = datetime.utcfromtimestamp(
        last_modified_timestamp).strftime('%m-%d--%H:%M:%S')

    colour_img = show_colours(path)
    cv2.imwrite(f"./{OUTPUT_FOLDER}/{timestamp}.jpg", colour_img)
