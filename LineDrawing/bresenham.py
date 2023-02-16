from typing import List, Tuple

def bresenham(
    p1: Tuple[int,int],
    p2: Tuple[int,int],
    I: List[List[int]],
    c: int = 1
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
    assert(
        p1[1] < len(I) and 
        p1[0] < len(I[0]) and
        p2[1] < len(I) and
        p2[0] < len(I[0]) and
        p1 != p2
    ), "The point must be distinct coordinates (x,y) inside the matrix I."


    if(p1[0] > p2[0]): p1,p2=p2,p1
    elif(p1[0] > p2[0]): p1,p2=p2,p1
    x0,y0 = p1
    x1,y1 = p2

    x = x0
    y = y0
    
    I[y][x] = c

    dx = x1 - x0
    dy = y1 - y0

    p0 = 2*dy - dx
    pk = p0
    while x < x1 and y < y1:
        x += 1
        if pk < 0: 
            pk += 2*dy
        else: 
            y += 1
            pk += 2*dy - 2*dx
        I[y][x] = c
    
    return I