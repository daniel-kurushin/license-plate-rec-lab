from glob import glob
from PIL import Image, ImageOps
from digits.digits import digit_coordinates, plate_coordinates, digit_values
SIZE = 32
e = 2.78

def σ(x):
    return 1 / (1 + e**(-x))

def compare(img1, img2):
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            a = σ(img1.getpixel((x,y)) / 255)
            b = σ(img2.getpixel((x,y)) / 255)
            D += [(a-b)**2]
    return sum(D)**1/2

digits = ImageOps.grayscale(Image.open(open('digits/digits.png', 'rb')))

for x in glob('img/*.png'):
    print(x)
    img = ImageOps.grayscale(Image.open(open(x, 'rb')))
    j = 0
    for x1, y1, x2, y2 in plate_coordinates:
        b_digit = img.crop((x1, y1, x2, y2)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)
        rez = []
        i = 0
        for a, b, c, d in digit_coordinates:
            a_digit = digits.crop((a, b, c, d)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)
            d = compare(a_digit, b_digit)
            rez += [(digit_values[i], d)]
            i += 1
        j += 1
        print(sorted(rez, key = lambda x : x[1])[0][0])
