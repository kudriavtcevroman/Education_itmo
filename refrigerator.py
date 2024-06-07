from random import uniform
def temperature(a, b):
    temp = uniform(a, b)
    temp = "{:.2f}".format(temp)
    return temp