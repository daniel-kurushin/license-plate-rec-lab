from json import load
import matplotlib.pyplot as plt

D = load(open('D.json'))
w = load(open('w.json'))

SIZE = 16

d0 = w
img = []
i = 0
for x in range(SIZE):
    col = []
    for y in range(SIZE):
        col += [d0[i]]
        i += 1
    img += [col]
    
plt.imshow(img)
plt.show()