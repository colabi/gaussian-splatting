
import time
import numpy as np
import torch
import glob
from PIL import Image


def convert_image(image_path):
    start = time.time()
    image = Image.open(image_path)
    resized_image = torch.from_numpy(np.array(image)) / 255.0
    resized_image = resized_image.permute(2, 0, 1)
    resized_image = resized_image[:3, ...]
    # print(resized_image.shape)
    original_image = resized_image.clamp(0.0, 1.0).to('cuda')
    end = time.time()
    print(end-start)
    torch.save(original_image, image_path.replace("undistorted_images", "undistorted_images_cache"))
    return original_image

def load_image(image_path):
    start = time.time()
    t = torch.load(image_path.replace("undistorted_images", "undistorted_images_cache"))
    end = time.time()
    print(end-start)
    
def process_images(path):
    images = glob.glob(path + "/*")
    for imagepath in images:
        # convert_image(imagepath)
        load_image(imagepath)

PATH = "/exp/myxed-gaussian-splatting/115886CF-AF45-4AEB-B1F4-DDF5CF588EF4/undistorted_images"
process_images(PATH)