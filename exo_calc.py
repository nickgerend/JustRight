# Written by: Nick Gerend, @dataoutsider
# Viz: "Just Right", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2, isinf
#pd.set_option('display.max_columns', None)

#region input
df = pd.read_csv(os.path.dirname(__file__) + '/JustRight2.csv')
earth_temp_K = 5778
df['sol_lum'] = (df['st_rad'])**2*(df['st_teff']/earth_temp_K)**4
#endregion

def effective_solar_flux(teff):
    
    if teff < 2600 or teff > 7200:
        return 0, 0, 0, 0

    # credit: arXiv:1404.5292
    # Coeffcients to be used in the analytical expression to calculate habitable zone flux boundaries

    seff = [0,0,0,0,0,0]
    seffsun  = [1.776,1.107, 0.356, 0.320, 1.188, 0.99] 
    a = [2.136e-4, 1.332e-4, 6.171e-5, 5.547e-5, 1.433e-4, 1.209e-4]
    b = [2.533e-8, 1.580e-8, 1.698e-9, 1.526e-9, 1.707e-8, 1.404e-8]
    c = [-1.332e-11, -8.308e-12, -3.198e-12, -2.874e-12, -8.968e-12, -7.418e-12]
    d = [-3.097e-15, -1.931e-15, -5.575e-16, -5.011e-16, -2.084e-15, -1.713e-15]

    tstar = teff - 5780.0
    for i in range(len(a)):
        seff[i] = seffsun[i] + a[i]*tstar + b[i]*tstar**2 + c[i]*tstar**3 + d[i]*tstar**4
    
    recentVenus = seff[0] # optimistic too close
    runawayGreenhouse = seff[1] # conservative too close
    maxGreenhouse = seff[2] # conservative too far
    earlyMars = seff[3] # optimistic too far
    #fivemeRunaway = seff[4] # earth close limit
    #tenthmeRunaway = seff[5] # closer limit 

    #c_close, c_far, o_close, o_far
    return runawayGreenhouse, maxGreenhouse, recentVenus, earlyMars

def orb_type(orb, close_limit, far_limit):
    if orb < close_limit:
        return 'too close'
    elif orb > far_limit:
        return 'too far'
    else:
        return 'just right'

def orb_mag(orb, close_limit, far_limit):
    if orb < close_limit:
        return orb - close_limit
    elif orb > far_limit:
        return orb - far_limit
    else:
        return orb - (far_limit+close_limit)/2

def gravity(e_rad, e_mass):
    e_m = 5.96e24
    e_r = 6.37e6
    G = 6.673e-11
    return G*(e_mass*e_m)/((e_rad*e_r)**2)

#region prepare data
output = list(map(lambda x: effective_solar_flux(x), df['st_teff']))
df['c_close'] = [x[0]**0.5 for x in output]
df['c_close'] = (df['sol_lum']/df['c_close'])**0.5
df['c_far'] = [x[1] for x in output]
df['c_far'] = (df['sol_lum']/df['c_far'])**0.5
df['o_close'] = [x[2] for x in output]
df['o_close'] = (df['sol_lum']/df['o_close'])**0.5
df['o_far'] = [x[3] for x in output]
df['o_far'] = (df['sol_lum']/df['o_far'])**0.5

df['conserv'] = [1 if x > y and x < z else 0 for x, y, z in zip(df['pl_orbsmax'], df['c_close'], df['c_far'])]
df['conserv_type'] = [orb_type(x, y, z) for x, y, z in zip(df['pl_orbsmax'], df['c_close'], df['c_far'])]
df['optimist'] = [1 if x > y and x < z else 0 for x, y, z in zip(df['pl_orbsmax'], df['o_close'], df['o_far'])]
df['optimist_type'] = [orb_type(x, y, z) for x, y, z in zip(df['pl_orbsmax'], df['o_close'], df['o_far'])]
df['c_type'] = ['just right' if x == 1 else y for x, y in zip(df['Just_Right'], df['conserv_type'])]
df['o_type'] = ['just right' if x == 1 else y for x, y in zip(df['Just_Right'], df['optimist_type'])]
df = df.loc[df['c_close'].astype(str) != 'inf']

df['gravity'] = [gravity(x, y) for x, y in zip(df['pl_rade'], df['pl_bmasse'])]
df['conserv_mag'] = [orb_mag(x, y, z) for x, y, z in zip(df['pl_orbsmax'], df['c_close'], df['c_far'])]
df['optimist_mag'] = [orb_mag(x, y, z) for x, y, z in zip(df['pl_orbsmax'], df['o_close'], df['o_far'])]
#endregion

print(df)
df.to_csv(os.path.dirname(__file__) + '/exo2.csv', encoding='utf-8', index=False)