# %%
'''
# Example of analysis of the LHC lattice
## Importing a collider
First of all we need to load our collider. 
This is a json file that contains all the information on the collider.
Namely it contains the two lines `lhcb1` and `lhcb2` corresponding to the two beams.
'''

# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xpart as xp
import yaml

collider = xt.Multiline.from_json('../data/collider_thin.json')

# %%
'''
Let's look at attributes and methods of the collider
'''

# %%
print(dir(collider))

# %%
# We can see that we have two lines, lhcb1 and lhcb2, we look at the lhcb1 line
my_dict = collider.lhcb1.to_dict()
# We can look at the attributes and methods of the elements

# %%
# Let's look at the attributes and methods of the one element of the lhcb1 line
#collider.lhcb1.to_dict()['elements']['mqwa.a4r3.b1..1']
# %%
# We can se that this is a multipole and we can get, for example, the quadrupole strength
print('The quadrupole strength is', my_dict["elements"]["mqwa.a4r3.b1..1"]["knl"][1])

# %%
# In the dictionary we have also informations on the reference particle
my_dict['particle_ref']

# %%
# Now we want to see some optics quantities
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
# get a pandas dataframe with the twiss data

# %%
#First of all let's plot the beta functions!
fig, ax = plt.subplots(2,1)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
fig.suptitle('Beta functions',fontsize = fontsize )
ax[0].plot(twiss_b1['s'], twiss_b1['betx'], label = r'$\beta_{x}$')
ax[0].set_ylabel(r'$\beta_{x}$ [m]', fontsize = fontsize)
ax[0].grid()
ax[0].legend(fontsize = fontsize)

ax[1].plot(twiss_b1['s'], twiss_b1['bety'], label = r'$\beta_{y}$')
ax[1].set_ylabel(r'$\beta_{y}$ [m]', fontsize = fontsize)
ax[1].set_xlabel('s [m]', fontsize = fontsize)
ax[1].grid()


ax[1].legend(fontsize = fontsize)
#We plot the ip names on the plot to follow what is happening
for ii in collider['lhcb1'].element_names:
    if (ii.startswith('ip') and len(ii)==3):
        ax[0].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[1].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        #write the name of the ip on the plot as an upper label at the top of the plot
        ax[0].text(twiss_b1[['s'],ii], max(ax[0].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
        ax[1].text(twiss_b1[['s'],ii], max(ax[1].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')

plt.tight_layout()

# %%
#We can also have a look at the closed orbit
fig, ax = plt.subplots(2,1)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
fig.suptitle('Closed Orbit', fontsize = fontsize)
ax[0].plot(twiss_b1['s'], twiss_b1['x'], label = r'x')
ax[0].legend(fontsize = fontsize)
ax[0].set_ylabel(r'x [m]', fontsize = fontsize)
ax[0].grid()
ax[1].plot(twiss_b1['s'], twiss_b1['y'], label = r'y')
ax[1].set_ylabel(r'y [m]', fontsize = fontsize)
ax[1].set_xlabel('s [m]', fontsize = fontsize)
ax[1].grid()
ax[1].legend(fontsize = fontsize)
for ii in collider['lhcb1'].element_names:
    if (ii.startswith('ip') and len(ii)==3):
        ax[0].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[0].text(twiss_b1[['s'],ii], max(ax[0].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
        ax[1].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[1].text(twiss_b1[['s'],ii], max(ax[1].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')

plt.tight_layout()

# %%
#All the useful informations are stored in the twiss dataframe, for example the tune...
print('The horizontal tune is', twiss_b1["mux"][-1])
print('The vertical tune is', twiss_b1["muy"][-1])

# %%
# We want to change the optics of the line
# To do this we need to use the knobs, which control the lens of the line
# We can have a configuration file with the knob settings, or we can set them manually
# Let's start with the manual setting of a knob
# We change the (half) crossing angle at IP8 to 170 urad
collider.vars['on_x8v'] = 150
# We can check that the knob has been changed
print('The knob on_x1 is now',collider.vars["on_x8v"]._value)
# We can now perform the twiss again
twiss_b1 = collider['lhcb1'].twiss()
# And plot the closed orbit
fig, ax = plt.subplots(2,1)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
fig.suptitle('Closed Orbit', fontsize = fontsize)
ax[0].plot(twiss_b1['s'], twiss_b1['x'], label = r'x')
ax[0].legend(fontsize = fontsize)
ax[0].set_ylabel(r'x [m]', fontsize = fontsize)
ax[0].grid()

ax[1].plot(twiss_b1['s'], twiss_b1['y'], label = r'y')
ax[1].set_ylabel(r'y [m]', fontsize = fontsize)
ax[1].set_xlabel('s [m]', fontsize = fontsize)
ax[1].grid()
ax[1].legend(fontsize = fontsize)
for ii in collider['lhcb1'].element_names:
    if (ii.startswith('ip') and len(ii)==3):
        ax[0].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[0].text(twiss_b1[['s'],ii], max(ax[0].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
        ax[1].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[1].text(twiss_b1[['s'],ii], max(ax[1].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
plt.tight_layout()
#Is it what we expected?
max_y = np.max(twiss_b1['y'])
min_y = np.min(twiss_b1['y'])
s_max_y = twiss_b1['s'][np.argmax(twiss_b1['y'])]
s_min_y = twiss_b1['s'][np.argmin(twiss_b1['y'])]
theta_crossing_IP8 = (max_y-min_y)/(s_max_y-s_min_y)
print('The crossing angle at IP8 is', theta_crossing_IP8*1e6)
#We retrieve the knob value!

# %%
#Now let's change the knobs from a config file
with open('../data/config.yaml', "r") as fid:
        config = yaml.safe_load(fid)
    
def set_orbit_from_config(collider, config):
    print('Setting optics as from config')
    for ii in ['on_x1', 'on_sep1', 'on_x2', 'on_sep2', 'on_x5',
               'on_sep5', 'on_x8h', 'on_x8v', 'on_sep8h', 'on_sep8v',
               'on_a1', 'on_o1', 'on_a2', 'on_o2', 'on_a5', 'on_o5', 'on_a8', 
               'on_o8', 'on_disp', 'on_crab1', 'on_crab5', 'on_alice_normalized', 
               'on_lhcb_normalized', 'on_sol_atlas', 'on_sol_cms', 'on_sol_alice', 
               'vrf400', 'lagrf400.b1', 'lagrf400.b2']:
        collider.vars[ii] = config['config_collider']['config_knobs_and_tuning']['knob_settings'][ii]

set_orbit_from_config(collider, config)

twiss_b1 = collider['lhcb1'].twiss()
twiss_b2 = collider['lhcb2'].twiss().reverse()
# And plot the closed orbit
fig, ax = plt.subplots(2,1)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
fig.suptitle('Closed Orbit', fontsize = fontsize)
ax[0].plot(twiss_b1['s'], twiss_b1['x'], label = r'x')
ax[0].legend(fontsize = fontsize)
ax[0].set_ylabel(r'x [m]', fontsize = fontsize)
ax[0].grid()

ax[1].plot(twiss_b1['s'], twiss_b1['y'], label = r'y')
ax[1].set_ylabel(r'y [m]', fontsize = fontsize)
ax[1].set_xlabel('s [m]', fontsize = fontsize)
ax[1].grid()
ax[1].legend(fontsize = fontsize)
for ii in collider['lhcb1'].element_names:
    if (ii.startswith('ip') and len(ii)==3):
        ax[0].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[0].text(twiss_b1[['s'],ii], max(ax[0].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
        ax[1].axvline(twiss_b1[['s'],ii], color = 'red', linestyle = '--', alpha = 0.3)
        ax[1].text(twiss_b1[['s'],ii], max(ax[1].get_yticks()), ii, fontsize = fontsize, horizontalalignment='center')
plt.tight_layout()
#Now we activated different knobs!