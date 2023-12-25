from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image
from matplotlib import image
from matplotlib import pyplot as plt
import os

class PiCam(PiCamera):
    
    def __init__(self,results_dir):
        super().__init__()
        self.results_dir = results_dir

    def shot(self,filename:str='image.jpg'):
        if ".jpg" not in filename:
            raise Exception("File must be a .jpg")
        self.start_preview()
        sleep(2)
        self.capture(filename)
        self.stop_preview()
        self.close()

    def compress_image(self,image_path:str):
        if ".jpg" not in image_path:
            raise Exception("File specified is not a .jpg")
        img = Image.open(image_path)
        width, height = img.size
        scale_factor = 10
        img_compressed = img.resize((int(width / scale_factor), int(height / scale_factor)))
        img_compressed.save(compressed_image_path)
        img_size = os.path.getsize(image_path)
        img_compressed_size = os.path.getsize(compressed_image_path)
    
    def plot(self,image_path:str):
        if ".jpg" not in "image_path":
            raise Exception("File specified is not a .jpg")
        plt.figure(figsize=(15,12))

        plt.subplot(121)
        plt.imshow(img)

        plt.subplot(122)
        plt.imshow(img_compressed)

        plt.show()
        plt.savefig(self.results_dir)
