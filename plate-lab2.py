import numpy as np
from glob import glob
from PIL import Image, ImageOps
from digits.digits import digit_coordinates, plate_coordinates, digit_values
from json import dump, load

class Neuron(object):
    a =  0.02
    b = -0.4

    def __call__(self, X):
        s = b
        for i in range(len(X)):
            s += self.w[i] * X[i]
        return round(s)
    
    def __learn(self,D):
        w = self.w[:]
        f = self.__call__
        for x, y in D:
            for j in range(len(x)):
                self.w[j] += self.a * (y - f(x)) * x[j]
        return self.__diff__(w, self.w)
    
    def __diff__(self, w1, w2):
        s = 0
        for a, b in zip(w1, w2):
            s += abs(a-b)
        return s > 0.001
    
    def __init__(self, D, a = 0.02, b = -0.04):
        try:
            self.w = load(open('w.json'))
        except FileNotFoundError:
            self.w = [0]*len(D[0][0])
            self.a = a
            self.b = b
            self.c = 0
            while self.__learn(D):
                self.c += 1
                if self.c > 10000: break
            dump(self.w, open('w.json','w'), indent = 4)

SIZE = 16

digits = ImageOps.grayscale(Image.open(open('digits/digits.png', 'rb')))

D = []
y = 0
for a, b, c, d in digit_coordinates:
    a_digit = list(np.array(digits.crop((a, b, c, d)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)).reshape(1,SIZE * SIZE)[0] / 255)
    D += [[a_digit,y]]
    y += 1
 
dump(D, open('D.json','w'), indent = 4)

f = Neuron(D)
    
for x in glob('img/*.png'):
    print(x.split('/')[1].split('.')[0], end = ' ; ')
    img = ImageOps.grayscale(Image.open(open(x, 'rb')))
    for x1, y1, x2, y2 in plate_coordinates:
        b_digit = list(np.array(img.crop((x1, y1, x2, y2)).resize(size = (SIZE,SIZE), resample = Image.HAMMING)).reshape(1,SIZE * SIZE)[0] / 255)
        y = int(round(f(b_digit)))
        
        print(digit_values[y] if y < len(digit_values) else '*', end = '')
    print()
