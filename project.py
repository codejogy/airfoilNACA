'''
BASED ON THIS ARTICLE
https://aerospaceweb.org/question/airfoils/q0041.shtml
'''

import os
import matplotlib.pyplot as plt
import argparse

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# Check if the folder exists, if not, make it
# plt.savefig('/NACA/plot.png')

def main():
    ...
def meanCamberLine(m:int,p:int,t:int,jump:int=0.01):
    '''
    Function to make the mean camber line
    :param m: Maximum camber
    :type m: int
    :param p: Position of the maximum camber
    :type p: int
    :param t: Maximum thickness, should be two numbers
    :type t: int
    :param jump: The jump is by default 0.01
    :raise:
    :return: A tuple with the values yc from 0 to 1 in x
    :rtype: tuple
    '''
    c = 1 # Maximum chord value, from 0 to 1 in x
    # Get all the values from input to values the function need
    m=c*(m/100)
    p=c*(p/10)
    t=c*(t/100)
    # The jump should be 0.01 by default
    # From x = 0 to x = p
    yc=[]
    for i in range(0,p,jump):
        yc.append(m*(2*p*i-i**2)/(p**2))

    # From x = p to x = c
        # c+1 because the end is not inclusive
    for i in range(p,c+1,jump):
        yc.append(m*((1-2*p)+2*p*i-i**2)/(1-p)**2)

    return tuple(yc)
def thicknessDistribution(t:int,jump:int = 0.01):
    '''
    Function to get the thickness distribution
    :param jump:
    :raise:
    :return: A tuple with the values yt from 0 to 1 in x
    '''
    c = 1
    t=c*(t/100)

    yt =[]
    # From x = 0 to x = c
    for i in range(0,c+1,jump):
        
        yt.append(t*(0.2969*(i)**(1/2)-0.126*i-0.3516*i**2+0.2843*i**3-0.1015*i**4)/0.2)

    
def fun3():
    ...