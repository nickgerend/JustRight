# Written by: Nick Gerend, @dataoutsider
# Viz: "Just Right", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2, isinf
#pd.set_option('display.max_columns', None)

#region Blend Data
df_exo = pd.read_csv(os.path.dirname(__file__) + '/exo2.csv')
df_poly = pd.read_csv(os.path.dirname(__file__) + '/poly.csv')
df_exo['abs_c_mag'] = abs(df_exo['optimist_mag'])

exo_group = df_exo.groupby('optimist_type', as_index=False)
group_list = []
for name, group in exo_group:
    group_sort = group.sort_values(by=['abs_c_mag'], ascending=True)
    group_filter = group_sort.head(96)
    group_shuffle = group_filter.sample(frac=1)
    group_shuffle['index'] = range(96)
    group_final = group_shuffle.reset_index(drop = True)
    group_list.append(group_final)

df_exo_filter = pd.concat(group_list, axis=0)
#print(df_final)

def toside(orb):
    if orb == 'too close':
        return 'right'
    if orb == 'too far':
        return 'left'
    return 'top'

df_exo_filter['side'] = [toside(x) for x in df_exo_filter['optimist_type']]
df_out = pd.merge(df_poly, df_exo_filter, on=['index', 'side'], how='inner')
#endregion

print(df_poly.shape)
print(df_out.shape)
df_out.to_csv(os.path.dirname(__file__) + '/poly.csv', encoding='utf-8', index=False)