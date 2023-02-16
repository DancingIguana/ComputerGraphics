from typing import List, Tuple

def digital_differential_analyzer(
    p1: Tuple[int,int],
    p2: Tuple[int,int],
    I: List[List[int]],
    c: int = 1
) -> List[List[int]]:
    """
    Given a matrix of integer values and two points,
    draw a line with the Digital Diferential Analyzer
    algorithm.
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

    I = [row[:] for row in I]
    if(p1[0] > p2[0]): p1,p2 = p2,p1

    x_0,y_0 = p1
    x_1,y_1 = p2

    m_x = x_1 - x_0
    m_y = y_1 - y_0

    s = max(abs(m_x), abs(m_y))

    dx = m_x/s
    dy = m_y/s

    x = x_0 
    y = y_0
    I[round(y)][round(x)] = c

    for i in range(s):
        x = x + dx
        y = y + dy
        I[round(y)][round(x)] = c

    return I