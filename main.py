from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
import shutil
import numpy as np

if os.path.exists("./AMC/"):
    shutil.rmtree("./AMC/")
os.mkdir("./AMC/")
os.mkdir("./AMC/10/")

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(executable_path = "./chromedriver", options = options)

for year in range(2002, 2021):
    year_path = "./AMC/10/%d/" % year
    os.mkdir(year_path)
    for exam in 'AB':
        exam_path = year_path + exam + '/'
        os.mkdir(exam_path)
        for problem in range(1, 26):
            url = "https://artofproblemsolving.com/wiki/index.php/%d_AMC_10%s_Problems/Problem_%d" % (year, exam, problem)
            browser.get(url)
            try:
                div = browser.find_element_by_class_name("mw-parser-output")
                elements = (element for element in div.find_elements_by_xpath("*"))

                while next(elements).tag_name != "h2":
                    pass

                ims = []
                while True:
                    element = next(elements)
                    if element.tag_name == "h2":
                        break
                    location = element.location
                    size = element.size
                    png = browser.get_screenshot_as_png()
                    im = Image.open(BytesIO(png))
                    left = location['x']
                    top = location['y']
                    right = location['x'] + size['width']
                    bottom = location['y'] + size['height']
                    im = im.crop((left, top, right, bottom))
                    ims.append(im)
                image = np.vstack([np.asarray(im) for im in ims])
                image = Image.fromarray(image)
                image.save(exam_path + str(problem) + ".png")
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print ("ERROR:", str(e))
                continue

browser.close()
