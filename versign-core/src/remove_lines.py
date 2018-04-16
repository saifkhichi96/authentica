import cv2
import numpy as np

def remove_xlines(im):
    lines = []

    h, w = im.shape
    columns = range(w)
    rows = range(h)

    for r in rows:                      # For each horizontal scan line
        mean = np.mean(im[r, columns])      # calculate pixel density (i.e.
        pxdt = mean / 255.0                 # percentage of white pixels)

        if pxdt > 0.25:                     # For >25% white pixels, we make the
            lines.append(r)                 # whole scan line (FIXME: Should be
            im[r, columns] = 0              # the actual line only) black.
            try:
                im[r-2, columns] = 0
                im[r-1, columns] = 0
                im[r+1, columns] = 0
                im[r+2, columns] = 0
            except:
                pass

    return im, lines

def remove_ylines(im):
    lines = []

    h, w = im.shape
    columns = range(w)
    rows = range(h)

    for c in columns:                   # For each vertical scan line
        mean = np.mean(im[rows, c])         # calculate pixel density (i.e.
        pxdt = mean / 255.0                 # percentage of white pixels)

        if pxdt > 0.25:                     # For >25% white pixels, we make the
            lines.append(c)                 # whole scan line (FIXME: Should be
            im[rows, c] = 0                 # the actual line only) black.
            try:
                im[rows, c-2] = 0
                im[rows, c-1] = 0
                im[rows, c+1] = 0
                im[rows, c+2] = 0
            except:
                pass
    return lines

def x_filling(im, x_lines):
    print "x-lines:", len(x_lines)
    h, w = im.shape
    for r in x_lines:
        for c in range(w):
            try:
                tpPx = im[r + 1, c]
                crPx = im[r, c]
                btPx = im[r - 2, c]

                if crPx == 0 and tpPx != 0 and btPx != 0:
                    for i in range(-5, 5):
                        im[r + i, c] = 255
            except:
                # Ignore index out of bounds errors
                pass

    return im

def y_filling(im, y_lines):
    print "y-lines:", len(y_lines)
    h, w = im.shape
    for c in y_lines:
        for r in range(h):
            try:
                rtPx = im[r, c + 5]
                crPx = im[r, c]
                ltPx = im[r, c - 5]

                if crPx == 0 and ltPx != 0 and rtPx != 0:
                    for i in range(-3, 4):
                        im[c + i, r] = 255
            except:
                # Ignore index out of bounds errors
                pass

    return im

def remove(image, kernel=(25, 25), fill=False):
    # Make a copy (original image will be needed later)
    copy = np.copy(image)

    # Remove all lines (horizontal and vertical)
    print 'Removing horizontal lines'
    x_lines = remove_xlines(copy)

    print 'Removing vertical lines'
    y_lines = remove_ylines(copy)

    # Remove noise (removes any parts of lines not removed)
    print 'Removing residual noise'
    filter = cv2.GaussianBlur(copy, kernel, 0)
    ret3, copy = cv2.threshold(filter, 0, 255, \
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Fill in any holes left by line removal
    if fill is True:
        print 'Filling holes'
        copy = x_filling(copy, x_lines)
        copy = y_filling(copy, y_lines)
    else:
        print 'Filling disabled'

    # Guassian filtering for noise removal thickens all strokes
    # and filling can sometimes color pixels which were unfilled
    # in original image. These side effects are reversed by
    # taking an intersection of the processed image with the
    # original image
    print 'Unfilling false positives'
    return cv2.bitwise_and(copy, image)