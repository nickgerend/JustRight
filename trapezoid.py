# Written by: Nick Gerend, @dataoutsider
# Viz: "Just Right", enjoy!

import pandas as pd
import os
from math import sin, cos, pi

#region Constants
# Geometry:
#           2
#     1
#              3
#  4
#           5
#     6
# > across translation: 25.9807621135332,15
# v down translation: 0,-30

# Ploygons:
poly_list = []
# \  \
#  \
s_1 = [[0.,0.],[8.66025403784439,5.],[17.3205080756888,0.],[17.3205080756888,-10.]]
#  /
# / /
s_2 = [[8.66025403784439,5.],[25.9807621135332,15.],[25.9807621135332,5.],[17.3205080756888,0.]]
# . |
#   |
s_3 = [[25.9807621135332,-15.],[17.3205080756888,-10.],[17.3205080756888,0.],[25.9807621135332,5.]]
#   \
# \  \
s_4 = [[0.,0.],[17.3205080756888,-10.],[8.66025403784439,-15.],[0.,-10.]]
# /  /
#   /
s_5 = [[8.66025403784439,-25.],[8.66025403784439,-15.],[17.3205080756888,-10.],[25.9807621135332,-15.]]
# | .
# |
s_6 = [[0.,-10.],[8.66025403784439,-15.],[8.66025403784439,-25.],[0.,-30.]]

poly_list.append(s_1)
poly_list.append(s_2)
poly_list.append(s_3)
poly_list.append(s_4)
poly_list.append(s_5)
poly_list.append(s_6)
#endregion

class point:
    def __init__(self, index, side, poly, row, col, x, y, path = -1, value = -1): 
        self.index = index
        self.side = side
        self.poly = poly
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.path = path
        self.value = value       
    def to_dict(self):
        return {
            'index' : self.index,
            'side' : self.side,
            'poly' : self.poly,
            'row' : self.row,
            'col' : self.col,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value }

def polybuild(rc, list_xy, side, cutoff):

    angle = 0.
    if side == 'left':
        angle = 120.
    if side == 'top':
        angle = 240.

    x_row_adj = 0.
    y_row_adj = 0.
    x_col_adj = 0.
    y_col_adj = 0.
    index = 0
    value = 1
    for col in range(rc):
        for row in range(rc):
            for poly in range(6):
                for xy in range(4):
                    x = poly_list[poly][xy][0] + x_row_adj + x_col_adj
                    y = poly_list[poly][xy][1] + y_row_adj + y_col_adj
                    x_t = x*cos(angle*pi/180.) + y*sin(angle*pi/180.)
                    y_t = -x*sin(angle*pi/180.) + y*cos(angle*pi/180.)
                    path = xy
                    if index > cutoff:
                        value = 0
                    list_xy.append(point(index, side, side+'_'+str(col)+'_'+str(row)+'_'+str(poly), row, col, x_t, y_t, path, value))
                # fully connected:
                x = poly_list[poly][0][0] + x_row_adj + x_col_adj
                y = poly_list[poly][0][1] + y_row_adj + y_col_adj
                x_t = x*cos(angle*pi/180.) + y*sin(angle*pi/180.)
                y_t = -x*sin(angle*pi/180.) + y*cos(angle*pi/180.)             
                if index > cutoff:
                        value = 0
                list_xy.append(point(index, side, side+'_'+str(col)+'_'+str(row)+'_'+str(poly), row, col, x_t, y_t, 4, value))
                # ^
                index += 1
            x_row_adj += 25.9807621135332
            y_row_adj += 15.
        x_col_adj += 0.
        y_col_adj += -30.
        x_row_adj = 0.
        y_row_adj = 0.

#region output
list_xy = []
polybuild(4, list_xy, 'right', 54)
polybuild(4, list_xy, 'left', 10)
polybuild(4, list_xy, 'top', 4)

df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
print(df_out)
#endregion

df_out.to_csv(os.path.dirname(__file__) + '/poly.csv', encoding='utf-8', index=False)