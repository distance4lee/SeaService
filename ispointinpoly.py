# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".

def point_in_poly(pt,poly):

    x,y = pt
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


## Test
if __name__ == '__main__':
    pt = (5,5)
    poly = [(0,10),(10,10),(10,0),(0,0)]
    print point_in_poly(pt,poly)
    print point_in_poly((2,3),[[1,1],[1,4],[3,7],[4,4],[4,1]])