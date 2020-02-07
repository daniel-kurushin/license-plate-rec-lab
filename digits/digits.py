plate_coordinates = [
    ( 50, 53, 159, 191), 
    (176, 16, 281, 191), 
    (285, 16, 390, 191), 
    (395, 16, 500, 191), 
    (509, 53, 618, 191), 
    (618, 53, 727, 191), 
    (747, 19, 807, 133), 
    (806, 19, 874, 133), 
    (884, 19, 952, 133),
]

digit_coordinates = []

D = 35
for x in range(0, 736, D):
    digit_coordinates += [(x, 0, x + D, 44)]

digit_values = "0123456789ABCEHKMOPTXY"