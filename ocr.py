import matplotlib.pyplot as plt
import cv2
import pytesseract as pt
import numpy as np
from deskew import determine_skew
import skimage.transform as sit
from skimage.util import img_as_ubyte
import re 
import spacy
#load_model = spacy.load("en_core_web_sm")

pt.pytesseract.tesseract_cmd = r'C:/Program Files\Tesseract-OCR\tesseract.exe'

red = '\033[91m'
green = '\u001b[32m'
blue = '\u001b[34m'
yellow = '\033[93m'
black = '\033[90m'

number_tokens = r"\d+,*\/*-*\d*"
quantity_tokens = "(?:kilo|kilogram|kilograms|grams|gram|litre|litres|liters|litr)"
structure_tokens = "hours ingredients method time portion fiber".split()


plt.figure(figsize = (15,15))
for i in range(1,6):
    path = 'photos/t'+str(i)+'.jpg'
    img = cv2.imread(path)
    plt.subplot(3,4,i)
    plt.imshow(img, cmap='gray')
def optimal_resize(img):
    boxes = pt.image_to_data(img, config='--psm 1', output_type = "data.frame")
    median_height = np.median(boxes["height"])
    target_height = 32
    scale_factor = target_height / median_height
    skip_percentage = 0.07
    if(scale_factor > 1 - skip_percentage and scale_factor < 1 + skip_percentage):
        return img
    if(scale_factor > 1.0):
        interpolation = cv2.INTER_CUBIC
    else:
        interpolation = cv2.INTER_AREA
    return cv2.resize(img, None, fx = scale_factor, fy = scale_factor, interpolation = interpolation)
    """Resize image based on the median height of the text in it. The idea is to keep the aspect ratio of the text blocks, but make sure they are roughly of a similar height, for better OCR performance."""
def preprocess(image):
    # This function preprocesses the image to make it suitable for OCR

    img = optimal_resize(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1,1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    angle = determine_skew(img)
    img = sit.rotate(img, angle, resize=True, cval = 1)
    img = img_as_ubyte(img)
    cv2.imshow('CLOSE ME',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img
def split_words_from_text(txt):
    glued_words = []
    words = txt.split()
    remainder = ""
    for word in words:
        word = word.strip(r" ,./\\*\(\):;?!\'\"\[\]_”„=<>")
        word = " "+word+" "
        number = re.findall(number_tokens, word)
        word = re.sub(number_tokens, "", word)
        quantity = re.findall(quantity_tokens, word)
        other = re.sub(quantity_tokens, "", word)
        other = other.strip()
        if len(remainder) > 0:
            glued_words.append((remainder+other).strip(r"- ,./\\*\(\):;?!\'\"\[\]_”„=<>"))
            remainder = ""
            other = ""
        if len(number) > 0:
            glued_words.append(number[0])
        if len(quantity) > 0:
            glued_words.append(quantity[0].strip())
        if len(other) > 0:
            if other[-1] == "-":
                remainder = other[0:-1]
                continue
            glued_words.append(other.strip(r"- ,./\\*\(\):;?!\'\"\[\]_”„=<>”"))
    return glued_words
for i in range(1,6):
    path = 'photos/t'+str(i)+'.jpg'
    example_image =  cv2.imread(path)
    processed = preprocess(example_image)
    text = pt.image_to_string(processed, lang = "eng", config='--psm 1')
    #print(text)
    split_text = split_words_from_text(text)
    print("")
    for word in split_text:
        print(word, end = " ")
