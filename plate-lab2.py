import numpy as np
from glob import glob
from PIL import Image, ImageOps
from digits.digits import digit_coordinates, plate_coordinates, digit_values
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork

SIZE = 10

def compare(img1, img2):
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            a = img1.getpixel((x,y)) / 255
            b = img2.getpixel((x,y)) / 255
            D += [(a-b)**2]
    return sum(D)**1/2

digits = ImageOps.grayscale(Image.open(open('digits/digits.png', 'rb')))
ds = SupervisedDataSet(SIZE * SIZE, len(digit_values))

i = 0
for a, b, c, d in digit_coordinates:
    a_digit = np.array(digits.crop((a, b, c, d)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)).reshape(1,100)[0]
    out = [0] * len(digit_values)
    out[1] = 1
    ds.addSample(a_digit, out)
    i += 1
    
net = buildNetwork(SIZE * SIZE, 50, len(digit_values))
trainer = BackpropTrainer(net, ds)
for x in range(300):
    trainer.trainEpochs(100)
    print(trainer.train())
    
for x in glob('img/*.png'):
    print(x.split('/')[1].split('.')[0], end = ' ; ')
    img = ImageOps.grayscale(Image.open(open(x, 'rb')))
    for x1, y1, x2, y2 in plate_coordinates:
        b_digit = np.array(img.crop((x1, y1, x2, y2)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)).reshape(1,100)[0]
        y = list(net.activate(b_digit))
        y_max = max(y)
        print(digit_values[y.index(y_max)], end = '')
    print()
#for x in glob('img/*.png'):
#    print(x.split('/')[1].split('.')[0], end = ' ; ')
#    img = ImageOps.grayscale(Image.open(open(x, 'rb')))
#    j = 0
#    for x1, y1, x2, y2 in plate_coordinates:
#        
#        rez = []
#        i = 0
#        for a, b, c, d in digit_coordinates:
#            a_digit = digits.crop((a, b, c, d)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)
#            d = compare(a_digit, b_digit)
#            rez += [(digit_values[i], d)]
#            i += 1
#        j += 1
#        print(sorted(rez, key = lambda x : x[1])[0][0], end = '')
#    print()
