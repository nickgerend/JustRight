# Written by: Nick Gerend, @dataoutsider
# Viz: "Just Right", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2, isinf
#pd.set_option('display.max_columns', None)

#region stack data
df = pd.read_csv(os.path.dirname(__file__) + '/exo2.csv')
df['o_mag_all'] = df['pl_orbsmax'] - (df['o_far']+df['o_close'])/2
meta_columns = ['pl_name','pl_rade','pl_bmasse','pl_insol','st_teff','st_rad','releasedate','Just_Right','sol_lum','gravity','conserv_mag','optimist_mag','o_mag_all']
df_list = []
df1 = df[meta_columns]
df1['Type'] = 'orbit'
df1['Value'] = df['pl_orbsmax']
df_list.append(df1)
df2 = df[meta_columns]
df2['Type'] = 'c_close'
df2['Value'] = df['c_close']
df_list.append(df2)
df3 = df[meta_columns]
df3['Type'] = 'c_far'
df3['Value'] = df['c_far']
df_list.append(df3)
df4 = df[meta_columns]
df4['Type'] = 'o_close'
df4['Value'] = df['o_close']
df_list.append(df4)
df5 = df[meta_columns]
df5['Type'] = 'o_far'
df5['Value'] = df['o_far']
df_list.append(df5)
df6 = df[meta_columns]
df6['Type'] = 'o_JR'
df6['Value'] = (df['o_far']+df['o_close'])/2
df_list.append(df6)
df7 = df[meta_columns]
df7['Type'] = 'c_JR'
df7['Value'] = (df['c_far']+df['c_close'])/2
df_list.append(df7)
#endregion

#region output
df_out = pd.concat(df_list, axis=0)
print(df.shape)
print(df_out.shape)
#endregion

df_out.to_csv(os.path.dirname(__file__) + '/exo3.csv', encoding='utf-8', index=False)