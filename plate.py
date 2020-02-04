from glob import glob
from PIL import Image, ImageOps

SIZE = 16
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

digits = ImageOps.grayscale(Image.open(open('img/digits.png', 'rb')))

for x in glob('img/5????.png'):
    print(x)
    img = ImageOps.grayscale(Image.open(open(x, 'rb')))
    for j in range(3):
        b_digit = img.crop((180+105 * j, 13, 284+105 * j, 187)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)
        rez = []
        for i in range(10):
            a_digit = digits.crop((62*i, 0, 62*(i+1), 82)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)
            d = compare(a_digit, b_digit)
            rez += [(i, d)]
        print(sorted(rez, key = lambda x : x[1])[0][0])
