import pandas as pd
import scipy.integrate as spi
import scipy.optimize as sop

X=[0,1,2,3,4,5,6,7,8,9,10]
Y=[10,8,3,4,6,8,25,9,4,2,1]


def ode_creator(X,Y):
    ode_func=sop.curve_fit(X,Y)
    return ode_func


print(ode_creator(X,Y))