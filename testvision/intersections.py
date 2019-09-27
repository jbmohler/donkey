import os
import argparse
import math
import cv2
import numpy as np
import poly_point_isect as bot

def analyze_sudoku_image(imagefile):
    img = cv2.imread(imagefile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('image size:  ', gray.shape)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    # algorithm --
    # 1. find lines
    # 2. bucket angles to figure out primary axes (by statistical grouping)
    # 3. group lines by intersection with vertical and horizontal axis
    # 4. ....

    print('lines\n\tcount: {}\n\tfirst: {}'.format(len(lines), lines[0]))
    points = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    def angle(line):
        assert len(line) == 1
        x1, y1, x2, y2 = line[0]
        yd = x2 - x1
        xd = y2 - y1

        # cross product
        dotprod = xd**2+xd*yd
        absprod = math.sqrt((xd**2+yd**2)*(xd+yd)**2)
        return math.acos(dotprod/absprod)

    def length(line):
        assert len(line) == 1
        x1, y1, x2, y2 = line[0]
        yd = x2 - x1
        xd = y2 - y1
        return math.sqrt(xd**2+yd**2)

    lengths = [length(line) for line in lines]
    maxlen = max(lengths)
    scale = maxlen / 10.

    angles = [angle(line) for line in lines]
    #print(angles[:23])

    scaled_angles = []
    for xlength, xangle in zip(lengths, angles):
        scale_count = int(xlength / scale) + 1
        scaled_angles += [xangle]*scale_count

    class Bucket:
        def __init__(self, r1, r2):
            self._r1 = r1
            self._r2 = r2

        def __contains__(self, value):
            return self._r1 < value < self._r2

        def __repr__(self):
            return 'Int({:.2f}, {:.2f})'.format(self._r1, self._r2)

        def overlaps(self, other):
            return self._r2 > other._r1

        def outer(self, other):
            return Bucket(self._r1, other._r2)

        def inner(self, other):
            assert self._r2 > other._r1
            return Bucket(other._r1, self._r2)

    buckets = [Bucket(math.pi/20.*(index-1), math.pi/20.*(index+1)) for index in range(40)]

    # run a bi-polar distribution on these angles to get the orientation
    bucket_counts = {i: 0 for i in range(20)}
    for sangle in scaled_angles:
        for index, bucket in enumerate(buckets):
            if sangle in bucket:
                bucket_counts[index%20] += 1

    print(bucket_counts)
    minb = min(bucket_counts.values())
    maxb = max(bucket_counts.values())
    quartiles = (maxb - minb)/4
    cutoff = minb + 3*quartiles
    magics = [(index, count) for index, count in bucket_counts.items() if count > cutoff]
    if len(magics) == 2:
        if magics[1][0] - magics[0][0] == 10:
            print('square!! got it')
        else:
            print('got it')
        print(magics)
    else:
        raise RuntimeError('cannot find parallel family')

    def line_intersect(perp, line):
        assert len(line) == 1
        x1, y1, x2, y2 = line[0]

        x0, y0 = perp

        if y0 == None:
            if x0 == x1:
                return y1
            if x0 == x2:
                return y2
            return (x0-x1)*(y2-y1)/(x2-x1)+y1

        if x0 == None:
            if y0 == y1:
                return x1
            if y0 == y2:
                return x2
            return (y0-y1)*(x2-x1)/(y2-y1)+x1

        raise RuntimeError('cannot find intersection')

    # note that lines and image shape feel like they are in the opposite order to me.
    xmed = gray.shape[1] // 2
    ymed = gray.shape[0] // 2
    b1, b2 = magics[1][0], magics[0][0]

    yintersections = []
    xintersections = []

    for xline, xlength, xangle in zip(lines, lengths, angles):
        scale_count = int(xlength / scale) + 1
        if xangle in buckets[b1] or xangle in buckets[b1+20]:
            v = line_intersect((xmed, None), xline)
            #assert 0 <= v <= gray.shape[0], 'v-y='+str(v)
            yintersections += [v]*scale_count
        if xangle in buckets[b2] or xangle in buckets[b2+20]:
            v = line_intersect((None, ymed), xline)
            #assert 0 <= v <= gray.shape[1], 'v-x='+str(v)
            xintersections += [v]*scale_count

    #print(xintersections[:7])
    #print(yintersections[:7])

    def bucket_values(values, rlow, rhigh, count_buckets):
        basewidth = (rhigh - rlow)/100
        buckets = [Bucket(basewidth*(index-1), basewidth*(index+1)) for index in range(count_buckets+1)]

        bucket_counts = {index: 0 for index, _ in enumerate(buckets)}
        for v1 in values:
            for index, bucket in enumerate(buckets):
                if v1 in bucket:
                    bucket_counts[index] += 1

        minb = min(bucket_counts.values())
        maxb = max(bucket_counts.values())
        quartiles = (maxb - minb)/12

        for i in range(11, 2, -1):
            cutoff = minb + i*quartiles
            magics = [(buckets[index], count) for index, count in sorted(bucket_counts.items()) if count > cutoff]

            refined = []
            swallowed = False
            for mag1, mag2 in zip(magics[:-1], magics[1:]):
                if swallowed:
                    swallowed = False
                    continue
                # If the magics are adjacent see if they are capturing the same
                # elements in the overlapping space.
                if mag1[0].overlaps(mag2[0]):
                    outerbucket = mag1[0].outer(mag2[0])
                    innerbucket = mag1[0].inner(mag2[0])

                    outers = 0
                    inners = 0
                    for v1 in values:
                        if v1 in outerbucket:
                            outers += 1
                        if v1 in innerbucket:
                            inners += 1

                    if inners >= .8*outers:
                        refined.append((innerbucket, inners))
                        swallowed = True
                    else:
                        refined.append(mag1)
                else:
                    refined.append(mag1)
            magics = refined

            if len(magics) >= 10:
                break

        return magics

    # look for a 10-polar distribution of lines in both directions
    yclusters = bucket_values(yintersections, 0, gray.shape[1], 100)
    print(yclusters)
    xclusters = bucket_values(xintersections, 0, gray.shape[0], 100)
    print(xclusters)

    line_image = np.copy(img) * 0  # creating a blank to draw lines on
    for xline, xlength, xangle in zip(lines, lengths, angles):
        scale_count = int(xlength / scale) + 1
        if xangle in buckets[b1] or xangle in buckets[b1+20]:
            v = line_intersect((xmed, None), xline)
            for bucket, _ in yclusters:
                if v in bucket:
                    v0 = line_intersect((0, None), xline)
                    v1 = line_intersect((xmed*2, None), xline)
                    cv2.line(line_image, (0, int(v0)), (xmed*2, int(v1)), (255, 0, 0), 5)
            #assert 0 <= v <= gray.shape[0], 'v-y='+str(v)
        if xangle in buckets[b2] or xangle in buckets[b2+20]:
            v = line_intersect((None, ymed), xline)
            for bucket, _ in xclusters:
                if v in bucket:
                    v0 = line_intersect((None, 0), xline)
                    v1 = line_intersect((None, ymed*2), xline)
                    cv2.line(line_image, (int(v0), 0), (int(v1), ymed*2), (255, 0, 0), 5)
            #assert 0 <= v <= gray.shape[1], 'v-x='+str(v)
        
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    cv2.imwrite('output-lines-extended.png', lines_edges)
    #os.system('gwenview output-lines-extended.png')

    """
    import pytesseract

    boxfun = pytesseract.image_to_boxes(img)
    for b in boxfun.splitlines():
        print(b)
    print(boxfun)

    asdf()
    """

    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    print(lines_edges.shape)
    #cv2.imwrite('line_parking.png', lines_edges)

    print('points\n\tcount: {}\n\tfirst: {}'.format(len(points), points[0]))
    intersections = bot.isect_segments(points)
    print('intersections:  {}'.format(len(intersections)))

    for inter in intersections:
        a, b = inter
        for i in range(3):
            for j in range(3):
                lines_edges[int(b) + i, int(a) + j] = [0, 255, 0]

    cv2.imwrite('output-lines-intersections.png', lines_edges)

    os.system('gwenview output-lines-intersections.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('sudoku image reader')
    parser.add_argument("image", help="image file to analyzze")
    args = parser.parse_args()

    analyze_sudoku_image(args.image)
