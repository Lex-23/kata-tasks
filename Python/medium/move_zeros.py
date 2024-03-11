"""Write an algorithm that takes an array and moves all of the zeros to the end, preserving the order of the other elements."""

def move_zeros(lst):
    return list(filter(lambda i: i != 0, lst)) + [0] * lst.count(0)
