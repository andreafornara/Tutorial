# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xpart as xp
import useful_functions as useful_functions
# %%
# First of all we need to load our collider
# In the collider 2 lines are defined: lhcb1 and lhcb2
collider = xt.Multiline.from_json('collider.json')
# %%
# To simplify the analysis we can remove the BB lenses from the lines
collider = useful_functions.set_BB(collider, beam = 'lhcb1', bb_lr = False, HO_1 = False, HO_2 = False, HO_5 = False, HO_8 = False)
collider = useful_functions.set_BB(collider, beam = 'lhcb2', bb_lr = False, HO_1 = False, HO_2 = False, HO_5 = False, HO_8 = False)

# %%
# In Xsuite a Twiss is performed by tracking a particle with a given initial condition (0,0,0,0,0,0 by default) 
# We need to build the trackers for each line
# WARNING: elements CANNOT be removed/added after the tracker is built
# you need to deprecate the tracker before modifying the line and build it again
collider.build_trackers()
# %%
# Now we can perform the Twiss of both lines
# We will concentrate on the lhcb1 line but the same procedure can be applied to the lhcb2 line
twiss_b1 = collider['lhcb1'].twiss()
twiss_b2 = collider['lhcb2'].twiss().reverse()
# %%
# The twiss is a dataframe with the following columns:
print(twiss_b1.cols)
#get a pandas dataframe with the twiss data
# %%
#First of all let's plot the beta functions!
fig, ax = plt.subplots(2,1)
fig.set_size_inches(18.5, 10.5)
fig.suptitle('Beta functions')
fontsize = 15
ax[0].plot(twiss_b1['s'], twiss_b1['betx'], label = r'$\beta_{x}$')
ax[1].plot(twiss_b1['s'], twiss_b1['bety'], label = r'$\beta_{y}$')
ax[0].set_ylabel(r'$\beta_{x}$ [m]', fontsize = fontsize)
ax[0].grid()
ax[1].set_ylabel(r'$\beta_{y}$ [m]', fontsize = fontsize)
ax[1].set_xlabel('s [m]', fontsize = fontsize)
ax[1].grid()
ax[0].legend(fontsize = fontsize)
ax[1].legend(fontsize = fontsize)
plt.tight_layout()


# %%
#All the useful informations are stored in the twiss dataframe, for example the tune...
print(f'The horizontal tune is {twiss_b1["mux"][-1]}')
print(f'The vertical tune is {twiss_b1["muy"][-1]}')

# %%
