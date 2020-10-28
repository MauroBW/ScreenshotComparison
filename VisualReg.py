from PIL import Image, ImageDraw
from selenium import webdriver
from tkinter.filedialog import askopenfilename
from datetime import datetime
import os
import sys


class ScreenAnalysis:

    driver = None

    def __init__(self):
        self.analyze()

    def getTime(self):
        now = datetime.now()
        dt = now.strftime("%H%M%S")
        
        return (dt)

    def analyze(self):

        actual_screen = "Actual\Actual1.PNG"

        expected_screen = "Expected\Expected1.png"
        
        screenshot_actual = Image.open(actual_screen)
        screenshot_expected = Image.open(expected_screen)
        
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_actual.size

        print("Resolution of Actual screenshot:",screen_width, screen_height)
        print("Resolution of Expected screenshot", screenshot_expected.size)

        block_width = ((screen_width - 1) // columns) + 1 
        block_height = ((screen_height - 1) // rows) + 1

        print(block_width, block_height)

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_actual = self.process_region(screenshot_actual, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_expected, x, y, block_width, block_height)

                if region_actual is not None and region_production is not None and region_production != region_actual:
                    draw = ImageDraw.Draw(screenshot_actual)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")
                    

        screenshot_actual.save("result" + self.getTime() + ".png")
        raise Exception ("The screenshots doesn't  match")

    def process_region(self, image, x, y, width, height):
        region_total = 0

        factor = 500

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    
                    region_total += sum(pixel)/4
                except:
                    return
        print(region_total/factor)
        return region_total/factor

    
ScreenAnalysis()