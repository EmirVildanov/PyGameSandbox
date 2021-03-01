# for more information look at
# https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/

# Define Infinite (Using INT_MAX
# caused overflow problems)
from typing import Tuple

import pygame

INT_MAX = 10000


def on_segment(p: tuple, q: tuple, r: tuple) -> bool:
    """
    Given three colinear points p, q, r,
    the function checks if point q lies
    on line segment 'pr'
    """
    if ((q[0] <= max(p[0], r[0])) &
            (q[0] >= min(p[0], r[0])) &
            (q[1] <= max(p[1], r[1])) &
            (q[1] >= min(p[1], r[1]))):
        return True

    return False


def orientation(p: tuple, q: tuple, r: tuple) -> int:
    """
    To find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (((q[1] - p[1]) *
            (r[0] - q[0])) -
           ((q[0] - p[0]) *
            (r[1] - q[1])))

    if val == 0:
        return 0
    if val > 0:
        return 1  # Collinear
    else:
        return 2  # Clock or counterclock


def do_intersect(p1, q1, p2, q2):
    """
    Function that returns true if
    the line segment 'p1q1' and 'p2q2' intersect.
    """
    # Find the four orientations needed for
    # general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases
    # p1, q1 and p2 are colinear and
    # p2 lies on segment p1q1
    if (o1 == 0) and (on_segment(p1, p2, q1)):
        return True

    # p1, q1 and p2 are colinear and
    # q2 lies on segment p1q1
    if (o2 == 0) and (on_segment(p1, q2, q1)):
        return True

    # p2, q2 and p1 are colinear and
    # p1 lies on segment p2q2
    if (o3 == 0) and (on_segment(p2, p1, q2)):
        return True

    # p2, q2 and q1 are colinear and
    # q1 lies on segment p2q2
    if (o4 == 0) and (on_segment(p2, q1, q2)):
        return True

    return False


def is_inside_polygon(points: list, p: tuple) -> bool:
    """
    Returns true if the point p lies
    inside the polygon[] with n vertices
    """
    n = len(points)

    # There must be at least 3 vertices
    # in polygon
    if n < 3:
        return False

    # Create a point for line segment
    # from p to infinite
    extreme = (INT_MAX, p[1])
    count = i = 0

    while True:
        next = (i + 1) % n

        # Check if the line segment from 'p' to
        # 'extreme' intersects with the line
        # segment from 'polygon[i]' to 'polygon[next]'
        if (do_intersect(points[i],
                         points[next],
                         p, extreme)):

            # If the point 'p' is colinear with line
            # segment 'i-next', then check if it lies
            # on segment. If it lies, return true, otherwise false
            if orientation(points[i], p,
                           points[next]) == 0:
                return on_segment(points[i], p,
                                  points[next])

            count += 1

        i = next

        if (i == 0):
            break

    # Return true if count is odd, false otherwise
    return (count % 2 == 1)


def is_segment_intersect_rect(point1, point2, rect: pygame.Rect):
    if do_intersect(point1, point2, rect.topleft, rect.topright):
        return True
    elif do_intersect(point1, point2, rect.topright, rect.bottomright):
        return True
    return False