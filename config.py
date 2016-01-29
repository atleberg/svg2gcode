''' G-code emitted at the start of processing the SVG file '''
preamble = "G21\nG28\nG90\nG1 Z15.0"

'''
G21 ; set units to millimeters
G28 ; home all axes
G90 ; use absolute coordinates
M204 S9000 ; set default acceleration to this
'''

''' G-code emitted at the end of processing the SVG file '''
postamble = "G28"

''' G-code emitted before processing a SVG shape '''
shape_preamble = "G4 P200"

''' G-code emitted after processing a SVG shape '''
shape_postamble = "G4 P200"

''' Print bed width in mm '''
bed_max_x = 120.0
bed_min_x = 0.0

''' Print bed height in mm '''
bed_max_y = 120.0
bed_min_y = 20.0

''' Offset '''
offset_x = 0.0
offset_y = 0.0

''' Post and pre actions '''
before_move = "G1 Z12.0"
after_move = "G1 Z10.0"

''' Flip Axis '''
flipX = False
flipY = True

'''
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
'''
smoothness = 0.2
