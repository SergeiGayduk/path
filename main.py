# Error: when it calls input_3 or input_4 the program runs, but doesn't finish the process
# Same with the try, except 

import sys
import re
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

# Reading and saving the data in the variables
def read(file_name):
    """ File Structure: 
        Xs, Ys, Xf, Yf 
        Total of obstacles
        Coordinate of the first obstacle
        Coordinate of the second obstacle
        And so on
    """
    file = open(file_name, "r")

    with file as f:
        Xs, Ys, Xf, Yf = [int(x) for x in next(f).split()] # Starting Points (Xs, Ys) and Finishing points (Xf, Yf)
        t = file.readline().split()                   
        number_of_obstacles = int(t[0])                    # Total of obstacles in the path

        Ax, Ay = [], []
        Bx, By = [], []
        Cx, Cy = [], []
        for line in f:
            values = [int(s) for s in line.split()]
            Ax.append(values[0])
            Ay.append(values[1])
            Bx.append(values[2])
            By.append(values[3])
            Cx.append(values[4])
            Cy.append(values[5])
        # Saves the coordinates of the first and second columns in variables ax and ay, respectively
        # np.array() allows to compute a bunch of data 
        ax = np.array([Ax])
        ay = np.array([Ay])

        bx = np.array([Bx])
        by = np.array([By])

        cx = np.array([Cx])
        cy = np.array([Cy])
        
        return Xs, Ys, Xf, Yf, number_of_obstacles, ax, ay, bx, by, cx, cy


# Details about the algorithm below:
# Move diagonally or along an axis: x += 1 if x1 > x0, x -= 1 if x1 < x0
# Move along 45 degree lines: x += 1 if dx > dy / 2 etc.
# x += dx / 10 ... while it's not taking constant steps, 
# it makes for a pretty cool display if you have a bunch of 
# randomly scattered bots chasing each other.
def line(x0, y0, x1, y1):
    """ Algoritmn used to create circular or elliptical arcs, oblique line (i.e. one that come at the 
    target at a slight angle), perpendicular paths, or even just running straight away from the target
    """
    try:
        # Number of steps x and y
        mx = abs(x1 - x0)
        my = abs(y1 - y0)

        # The greater number of steps 
        steps = max(mx, my)
        sx = 0
        sy = 0

        x = x0
        y = y0
        path = [(x0, y0)]

        while x != x1 or y != y1:
            sx += mx
            sy += my

            if sx >= steps:
                sx -= steps
                x += 1 # Only one direction for now
        
            if sy >= steps:
                sy -= steps
                y += 1 # Only one direction for now
        
            path.append((x,y))

    except ValueError:
        print("IMPOSSIBLE!")
    
    return path

# Returns the coordinate of each obstacles' coordinate
def obstacles(ax, ay, bx, by, cx, cy):
    """Given the coordinates of the three vertices of a triangle ABC,
    the centroid O coordinates are given by Ox = Ax + Bx + Cx / 3 and
    Oy = Ay + By + Cy / 3, where Ax and Ay are the x and y coordinates of the point A etc..
    """   

    ox = np.array([(ax + bx + cx)], dtype=np.float) / 3    
    oy = np.array([(ay + by + cy)], dtype=np.float) / 3


    return ox, oy


# Uses the string and the dictionary to write the data in the file in the right way
def replace_words(s, words):
    for k, v in words.items():
        s = s.replace(k, v)
    return s

def main():
    input_file = "input/input_3.txt"
    Xs, Ys, Xf, Yf, number_of_obstacles, ax, ay, bx, by, cx, cy = read(input_file)

    path = line(Xs, Ys, Xf, Yf)

    ox, oy = obstacles(ax, ay, bx, by, cx, cy)

    ox = np.reshape(ox, (number_of_obstacles), 1)
    oy = np.reshape(oy, (number_of_obstacles), 1)

    dat = np.array([ox, oy])
    dat = dat.T

    np.savetxt('output/data_3.txt', dat, delimiter = ',')

    total = len(path) - 1
    with open('output/output_3.txt', mode='w', encoding='utf-8') as output_file:
        output_file.write(str(total) + '\n')
        for element in path:
            coord = str(element)
            dictionary = {"(" : "", "," : "", ")" : ""}
            output_file.write(replace_words(coord, dictionary) + '\n')

if __name__ == "__main__":
    main() 
