from typing import List, Tuple
# Reference: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def plot_line_low(
    x0:int,
    y0:int,
    x1:int,
    y1:int,
    I: List[List[int]],
    c: int = 1
) -> List[List[int]]:

    dx = x1 - x0
    dy = y1 - y0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    pk=(2*dy)-dx
    y = y0

    for x in range(x0,x1+1):
        I[y][x] = c
        if pk > 0: 
            y += yi
            pk += 2*(dy-dx)
        else:
            pk += 2*dy
    
    return I


def plot_line_high(
    x0:int,
    y0:int,
    x1:int,
    y1:int,
    I:List[List[int]],
    c:int = 1
) -> List[List[int]]:
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    pk = (2*dx) - dy
    x = x0
    for y in range(y0,y1+1):
        I[y][x] = c
        if pk > 0:
            x += xi
            pk += 2*(dx-dy)
        else:
            pk += 2*dx

    return I

def bresenham(
    p1:Tuple[int,int],
    p2:Tuple[int,int],
    I:List[List[int]],
    c:int = 1
) -> List[List[int]]:
    """
    Given a matrix of integer values and two points,
    draw a line with the Bresenham algorithm.

    Args:
    ------------
    p1: (x0,y0) coordinate inside the matrix I
    p2: (x1,y1) coordinate inside the matrix I
    I: the matrix where the line will be drawn
    c: the integer value of the line's color

    Returns:
    ------------
    The matrix with the colored line
    """
    #assert(
    #    p1[1] < len(I) and 
    ##    p1[0] < len(I[0]) and
    #    p2[1] < len(I) and
    #    p2[0] < len(I[0]) and
    #    p1 != p2
    #), "The point must be distinct coordinates (x,y) inside the matrix I."

    x0,y0 = p1
    x1,y1 = p2
    I = [row[:] for row in I]
    if abs(y1-y0) < abs(x1-x0):
        if x0 > x1:
            I = plot_line_low(x1,y1,x0,y0,I,c)
        else:
            I = plot_line_low(x0,y0,x1,y1,I,c)
    else:
        if y0 > y1:
            I = plot_line_high(x1,y1,x0,y0,I,c)
        else:
            I = plot_line_high(x0,y0,x1,y1,I,c)
    
    return I 
