#!/usr/bin/env python

import sys
import os
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *


def write_gcode(data):
    f = open(sys.argv[2], 'a')
    f.write("%s\n" % data)
    f.close()

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

    if os.path.exists(sys.argv[1]):
        tree = ET.parse(sys.argv[1])
    else:
        print "Error: Could not open file '%s'" % sys.argv[1]
    if os.path.exists(sys.argv[2]):
        os.unlink(sys.argv[2])
    root = tree.getroot()

    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        print "Error: Unable to get width and height for the svg"
        sys.exit(1)
    else:
        width = float(width.rstrip('mm'))
        height = float(height.rstrip('mm'))

    viewbox = root.get('viewBox')
    if viewbox:
        _, _, ww, hh = viewbox.split()
        print "ViewBox w=%s h=%s" % (ww, hh)
        ww = float(ww)
        hh = float(hh)
    else:
        print "Error: Unable to get viewbox for the svg"
        sys.exit(1)
    
    # Inkscape scale: http://wiki.inkscape.org/wiki/index.php/Units_In_Inkscape
    dpi = 96.0
    scale_x = width / ww
    scale_y = height / hh
    if scale_x != scale_y:
        print "Warning: width and height scale factors are not equal!"

    print "Info: Document scale factor is %0.1f %0.1f" % (scale_x, scale_y)
    if width > bed_max_x or height > bed_max_y:
        print "Info: Document area larger than print bed, extra scaling needed!"
        scale_x = (bed_max_x / max(width, height)) * scale_x
        scale_y = (bed_max_y / max(width, height)) * scale_y
        print "Info: New scale factor is %0.1f %0.1f" % (scale_x, scale_y)

    write_gcode(preamble)
    first = True

    maxX = None
    minX = None
    maxY = None
    minY = None

    for elem in root.iter():
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                write_gcode(shape_preamble)
                p = point_generator(d, m, smoothness)
                for x,y in p:
                    xs = scale_x*x
                    ys = scale_y*y
                    if flipX:
                        xs = -xs + bed_max_x
                    if flipY:
                        ys = -ys + bed_max_y
                    xs += offset_x
                    ys += offset_y
                    if not maxX:
                        maxX = xs
                    elif xs > maxX:
                        maxX = xs
                    if not minX:
                        minX = xs
                    elif xs < minX:
                        minX = xs
                    if not maxY:
                        maxY = ys
                    elif ys > maxY:
                        maxY = ys
                    if not minY:
                        minY = ys
                    elif ys < minY:
                        minY = ys

                    if xs > bed_min_x and xs < bed_max_x and ys > bed_min_y and ys < bed_max_y:
                        if first:
                            write_gcode("G1 X%0.1f Y%0.1f" % (xs, ys))
                            write_gcode(after_move)
                            first = False
                        write_gcode("G1 X%0.1f Y%0.1f" % (xs, ys))
                    else:
                        print "Error: out of bounds! (X%0.1f Y%0.1f)" % (xs, ys)
                first = True
                write_gcode(before_move)
                #print shape_postamble
    write_gcode(postamble)

    print "Min X = %0.1fmm" % minX
    print "Max X = %0.1fmm" % maxX
    print "Min Y = %0.1fmm" % minY
    print "Max Y = %0.1fmm" % maxY
    print "DeltaX = %0.1fmm" % (maxX - minX)
    print "DeltaY = %0.1fmm" % (maxY - minY)

if __name__ == "__main__":
    generate_gcode()
