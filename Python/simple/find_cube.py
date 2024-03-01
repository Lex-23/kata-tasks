"""
Build a pile of Cubes
"""

def find_(m):
    i = 0
    temp = m
    while True:
        i += 1
        temp = temp - i ** 3
        if temp == 0:
            return i
        elif temp < 0:
            return -1
