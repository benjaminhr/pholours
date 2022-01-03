import glob
import imageio
import pathlib

PHOTO_FOLDER = str(pathlib.Path("./output-border").resolve())
photo_files = sorted(glob.glob(PHOTO_FOLDER + "/*"))

ANIMATION_FOLDER = str(pathlib.Path("./animations").resolve())

with imageio.get_writer(f'{ANIMATION_FOLDER}/movie.gif', mode='I', duration=0.05) as writer:
    for filename in photo_files:
        image = imageio.imread(filename)
        writer.append_data(image)
