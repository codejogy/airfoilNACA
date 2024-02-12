'''
BASED ON THIS ARTICLE
https://aerospaceweb.org/question/airfoils/q0041.shtml
'''

import os
import matplotlib.pyplot as plt
import argparse
import math
import csv

ROUND = 7 # GLOBAL CONST. The number of decimals to round the functions

def main():
    # PARSE FROM CLI
    parser = argparse.ArgumentParser(description='Make a NACA 4 digits airfoil')
    parser.add_argument('integers',metavar='XXXX',type=nacaParser,help='The 4 digits as #### PE. 2415')
    parser.add_argument('-s','--samples',dest='N',type=int,default=100,help='The number of samples from 0 to 1 to make the airfoil (default 100)')
    args = parser.parse_args()
    m = int(args.integers[0])
    p = int(args.integers[1])
    t = int(args.integers[2:])
    samples = args.N
    # MAKING ROUTE
    newPath = f'NACA{m}{p}{t:02d}/'
    mkdir(newPath)
    # GETTING THE AIRFOIL
    x = xValues(samples)
    yc = meanCamberLine(m,p,t,x)
    yt = thicknessDistribution(t,x)
    thetas = thetaValues(m,p,x)
    up = upperSurface(yc,yt,thetas,x)
    lo = lowerSurface(yc,yt,thetas,x)
    # SAVING THE AIRFOIL
    getImage(up,lo,x,yc,newPath)
    getCSV(up,lo,newPath)
    print('Success, check your new folder!')

def mkdir(path:str) -> bool:
    '''
    Check if the NACA####/ route exists, if not, makes a new dir to save the files
    :param path: String with the name of the directory to be checked or made
    '''
    if not os.path.isdir(path):
        os.mkdir(path)
        return True
    return False
        

def nacaParser(args):
    '''
    Parser function to check if the values are from 0 to 9999
    '''
    try:
        i = int(args)
    except ValueError:
        raise argparse.ArgumentTypeError('Add a number from 0001 to 9999')
    
    if not 0 < i <= 9999:
        raise argparse.ArgumentTypeError('Argument must be from 0001 to 9999')
    
    return f'{i:04d}'
    


def xValues(samples=100) -> tuple[int]:
    '''
    Get x values from a determined jump from 0 to 1 
    :param samples: That means, from 0 to 1, 100 divisions will be made
    '''
    xList = []
    for x in range(samples+1):
        xList.append(x/samples)

    return tuple(xList)




def meanCamberLine(m:int,p:int,t:int,xTuple:tuple[int]):
    '''
    Function to make the mean camber line
    :param m: Maximum camber
    :type m: int
    :param p: Position of the maximum camber
    :type p: int
    :param t: Maximum thickness, should be two numbers
    :type t: int
    :param xValues: A tuple of values of x
    :type xValues: tuple[int]
    :raise:
    :return: A tuple with the values yc from 0 to 1 in x
    :rtype: tuple
    '''
    c = 1 # Maximum chord value, from 0 to 1 in x
    # Get all the values from input to values the function need
    m:float=c*(m/100)
    p:float=c*(p/10)
    t:float=c*(t/100)
    # The jump should be 0.01 by default
    yc=[]
    for i in xTuple:
        if i >= p:
            # From x = p to x = c
            yc.append(m*((1-2*p)+2*p*i-i**2)/(1-p)**2)
            continue
        # From x = 0 to x = p
        yc.append(m*(2*p*i-i**2)/(p**2))
        
    return tuple(yc)


def thicknessDistribution(t:int,xTuple:tuple[int]) -> tuple[int]:
    '''
    Function to get the thickness distribution
    :param jump:
    :type jump: int
    :raise:
    :return: A tuple with the values yt from 0 to 1 in x
    :rtype: tuple
    '''
    c = 1
    t=c*(t/100)

    yt =[]
    # From x = 0 to x = c
    for i in xTuple:
        yt.append(t*(0.2969*(i)**(1/2)-0.126*i-0.3516*i**2+0.2843*i**3-0.1015*i**4)/0.2)

    return tuple(yt)
    
def thetaValues(m:int,p:int,xTuple:tuple[int]):
    '''
    Function to get the angle in each point of the camber line

    :param jump:
    :type jump: int 
    :return: A tuple with the values of theta from 0 to 1 in x
    :rtype: tuple
    '''
    c = 1
    m=c*(m/100)
    p=c*(p/10)
    # Theta = arctan(d(yc)/dx)
    # Derivative
    theta = []
    for x in xTuple:
        if x >= p:
            # yc has a function from x = p to x = c and c = 1
            dyc = 2*m*(p-x)/(1-p)**2
            theta.append(math.atan(dyc))
            continue
        # yc has a function from x = 0 to x = p
        dyc = 2*m*(p-x)/p**2
        theta.append(math.atan(dyc))
        
    return tuple(theta)

def upperSurface(yc:tuple[int],yt:tuple[int],theta:tuple[int],xTuple:tuple[int]) -> tuple[int,float]:
    '''
    Function that returns the upper surface of the selected airfoil
    :param yc:
    :type: tuple
    :param yt:
    :type: tuple
    :param theta:
    :type: tuple
    :param xTuple:
    :type:
    :return: Two tuples with the upper values, the first tuple has the values of x, the second has the values of y
    :rtype: tuple(tuple(upperX), tuple(upperY))
    '''
    # xu = x-yt*sin(theta)
    # This is the value of x that will have in the upper surface

    # yu = yc + yt*cos(theta)
    # This is the value of y from xu
    c = 1
    xu = []
    yu = []
    i=0
    for x in xTuple:
        xu.append(round(x-yt[i]*math.sin(theta[i]),ROUND))
        yu.append(round(yc[i]+yt[i]*math.cos(theta[i]),ROUND))
        i = i + 1 
    return tuple(xu),tuple(yu)


def lowerSurface(yc:tuple[int],yt:tuple[int],theta:tuple[int],xTuple:tuple[int]) -> tuple[int,float]:
    '''
    Function that returns the lower surface of the selected airfoil
    :param yc:
    :type: tuple
    :param yt:
    :type: tuple
    :param theta:
    :type: tuple
    :param jump:
    :type:
    :return: Two tuples with the lower values, the first tuple has the values of x, the second has the values of y
    :rtype: tuple(tuple(lowerX), tuple(lowerY))
    '''

    # xl = x + yt
    # Value of x in lower surface
    # yl = yc - yt*cos(theta)
    # Value of y in lower surface
    
    c = 1
    xl = []
    yl = []
    i = 0
    for x in xTuple:
        xl.append(round(x+yt[i]*math.sin(theta[i]),ROUND))
        yl.append(round(yc[i]-yt[i]*math.cos(theta[i]),ROUND))
        i = i + 1
    return tuple(xl), tuple(yl)

# Now that the values does exists, its necessary to print it in a graph with matplotlib help
def getImage(upperSurface:tuple[int,int],lowerSurface:tuple[int,int],xTuple:tuple[int],camberLine:tuple[int],path:str) -> bool:
    '''
    Function that returns the image in NACA####/NACA.png
    Replaces image if there's already one
    If there's something wrong will output False
    :param upperSurface:
    :type: tuple[int,int]
    :param lowerSurface:
    :type: tuple[int,int]
    :param path:
    :type path: str
    :raises:
    :return: Image of the airfoil in a folder with the same name
    :rtype: bool
    '''
    plt.plot(xTuple,camberLine)
    plt.plot(upperSurface[0],upperSurface[1])
    plt.plot(lowerSurface[0],lowerSurface[1])
    plt.axis('equal')
    plt.grid(True,linestyle='--')
    plt.savefig(os.path.join(path,'test.png'))
    return True

def getCSV(upperSurface:tuple[int,int],lowerSurface:tuple[int,int],path:str) -> None:
    '''
    Function that returns a CSV in NACA####/NACA.csv+
    Replaces the CSV if there's already one

    '''
    
    with open(os.path.join(path,'NACA.csv'),'w') as f:
        writer = csv.DictWriter(f,fieldnames=['x','y'])
        writer.writeheader()
        for valueX,valueY in zip(upperSurface[0],upperSurface[1]):
            writer.writerow({'x':valueX,'y':valueY})
        for valueX,valueY in zip(lowerSurface[0],lowerSurface[1]):
            writer.writerow({'x':valueX,'y':valueY})

if __name__ == '__main__':
    main()
    
    
