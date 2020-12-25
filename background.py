# Written by: Nick Gerend, @dataoutsider
# Viz: "Just Right", enjoy!

import pandas as pd
import os
from math import sin, cos, pi

#region Constants
# Ploygons:
# 1 (top)
# 2 (left)  5 (right)
# 3 (top)   6 (top)    8 (left) 9 (right)
# 4 (left)  7 (right)
# > across translation: 25.9807621135332,45
# v down translation: 25.9807621135332,-45
poly_list = []
# \ /
#  *
s_1 = [[0.,0.],[8.66025403784439,5.],[17.3205080756888,0.],[25.9807621135332,5.],[34.6410161513775,0.],[17.3205080756888,-10.]]
# \
# \
s_2 = [[0.,0.],[17.3205080756888,-10.],[17.3205080756888,-20.],[25.9807621135332,-25.],[25.9807621135332,-35.],[8.66025403784439,-25.],[8.66025403784439,-15.],[0.,-10.]]
# \
#  *
s_3 = [[0.,-30.],[8.66025403784439,-25.],[25.9807621135332,-35.],[17.3205080756888,-40.]]
# \
# |
s_4 = [[0.,-30.],[17.3205080756888,-40.],[17.3205080756888,-60.],[8.66025403784439,-55.],[8.66025403784439,-45.],[0.0,-40.]]
#  *
# /
s_5 = [[17.3205080756888,-10.],[34.6410161513775,0.0],[34.6410161513775,-10.],[17.3205080756888,-20.]]
#   /
# /
s_6 = [[17.3205080756888,-20.],[34.6410161513775,-10.0],[43.3012701892219,-15.],[51.9615242270663,-10.],[60.6217782649107,-15.],[43.3012701892219,-25.],[34.6410161513775,-20.],[25.9807621135332,-25.]]
#   |
# |
s_7 = [[17.3205080756888,-60.],[17.3205080756888,-40.],[25.9807621135332,-35.],[25.9807621135332,-25.],[34.6410161513775,-20.],[34.6410161513775,-40.],[25.9807621135332,-45.],[25.9807621135332,-55.]]
# |
# *
s_8 = [[34.6410161513775,-40.],[34.6410161513775,-20.],[43.3012701892219,-25.],[43.3012701892219,-45.]]
# /
# |
s_9 = [[43.3012701892219,-45.],[43.3012701892219,-25.],[60.6217782649107,-15.],[60.6217782649107,-25.],[51.9615242270663,-30.],[51.9615242270663,-40.]]

poly_list.append(s_1)
poly_list.append(s_2)
poly_list.append(s_3)
poly_list.append(s_4)
poly_list.append(s_5)
poly_list.append(s_6)
poly_list.append(s_7)
poly_list.append(s_8)
poly_list.append(s_9)
#endregion

class point:
    def __init__(self, index, side, poly, row, col, x, y, path = -1, value = ''): 
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

#region algorithm
list_xy = []

def polybuild(rc, list_xy, side):
    x_row_adj = 0.
    y_row_adj = 0.
    x_col_adj = 0.
    y_col_adj = 0.
    index = 0
    value = ''
    for col in range(rc):
        for row in range(rc):
            for poly in range(9):
                if poly == 1-1 or poly == 3-1 or poly == 6-1:
                    value = 'top'
                if poly == 2-1 or poly == 4-1 or poly == 8-1:
                    value = 'left'
                if poly == 5-1 or poly == 7-1 or poly == 9-1:
                    value = 'right'
                for xy in range(len(poly_list[poly])):
                    x = poly_list[poly][xy][0] + x_row_adj + x_col_adj
                    y = poly_list[poly][xy][1] + y_row_adj + y_col_adj
                    path = xy
                    list_xy.append(point(index, side, side+'_'+str(col)+'_'+str(row)+'_'+str(poly), row, col, x, y, path, value))
                # fully connected:
                x = poly_list[poly][0][0] + x_row_adj + x_col_adj
                y = poly_list[poly][0][1] + y_row_adj + y_col_adj            
                list_xy.append(point(index, side, side+'_'+str(col)+'_'+str(row)+'_'+str(poly), row, col, x, y, len(poly_list[poly]), value))
                # ^
                index += 1
            x_row_adj += 25.9807621135332
            y_row_adj += 45.
        x_col_adj += 25.9807621135332
        y_col_adj += -45.
        x_row_adj = 0.
        y_row_adj = 0.

polybuild(20, list_xy, 'all')
#endregion

#region output
df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
print(df_out)
#endregion

df_out.to_csv(os.path.dirname(__file__) + '/poly_back.csv', encoding='utf-8', index=False)