# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xpart as xp
import xobjects as xo
import useful_functions as useful_functions
import yaml
# %%
# Now we want to start tracking particles!
# First of all let's load the collider and build the trackers
collider = xt.Multiline.from_json('collider.json')
collider.build_trackers()
# %%
# Then we want to set the optics from a config file
# We will use the optics from the HL-LHC config
with open('config.yaml', "r") as fid:
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
# %%
# First of all we define a context
ctx = xo.ContextCpu()
# Then we can define a single particle 
my_particle = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9, x = 1e-6)
# Let's look at it
my_particle.show()
# We can also access the particle attributes directly
# IMPORTANT: it is better to use the context to access the attributes 
# to avoid conflicts when using GPU contexts
print(f'The particle energy is {ctx.nparray_from_context_array(my_particle.energy0)} eV')
print(f'The particle x position is {ctx.nparray_from_context_array(my_particle.x)} m')
# %%
# Now we want to track the particle, we can do it with the tracker method
# IMPORTANT: each element of the collider can track particles separately!
# For example let's take a crab cavity and track the particle through it
# We can access the crab cavity with the following command
my_crab = collider["lhcb1"].element_dict['acfgah.4bl1.b1']
print(my_crab)
# %%
# And we can track the particle with the following command
my_particle = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9, zeta = 0.075)
print('---------Particle before tracking------')
my_particle.show()
my_crab.track(my_particle)
print('---------Particle after tracking------')
my_particle.show()
# The particle px has changed! This is because the particle is at zeta!=0
# What if we want to track the particle at zeta=0?
# We can do it with the following command
my_particle = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9, zeta = 0)    
my_crab.track(my_particle)
print('---------Particle after tracking at zeta=0------')
my_particle.show()

#Now for something more complicated we can track the particle through the whole line
#We can do it with the following command
my_particle = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9)
collider['lhcb1'].track(my_particle)
print('---------Particle after tracking through the whole line------')
my_particle.show()
# %%
# Now for a more realistic example we want to track a gaussian bunch of particles
# Matched to the RF bucket
N_particles = 10000
bunch_intensity = 2.2e11
normal_emitt_x = 2.5e-6 #m*rad
normal_emitt_y = 2.5e-6 #m*rad
sigma_z = 7.5e-2
particle_ref = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9)
gaussian_bunch = xp.generate_matched_gaussian_bunch(
        num_particles=N_particles, total_intensity_particles=bunch_intensity,
        nemitt_x=normal_emitt_x, nemitt_y=normal_emitt_y, sigma_z=sigma_z,
        particle_ref=particle_ref,
        tracker=collider['lhcb1'].tracker)
# %%
#We can plot histograms of the particles
fig, ax = plt.subplots(1,3)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
starting_x = ctx.nparray_from_context_array(gaussian_bunch.x).copy()
starting_y = ctx.nparray_from_context_array(gaussian_bunch.y).copy()
starting_zeta = ctx.nparray_from_context_array(gaussian_bunch.zeta).copy()

fig.suptitle('Bunch histograms', fontsize = fontsize)
ax[0].hist(starting_x, bins = 100)
ax[0].set_xlabel('x [m]', fontsize = fontsize)
ax[0].grid()
ax[1].hist(starting_y, bins = 100)
ax[1].set_xlabel('y [m]', fontsize = fontsize)
ax[1].grid()
ax[2].hist(starting_zeta, bins = 100)
ax[2].set_xlabel('zeta [m]', fontsize = fontsize)
ax[2].grid()
plt.tight_layout()
# %%
# We can also plot the bunch in the transverse plane
fig, ax = plt.subplots(1,1)
fig.set_size_inches(7.5, 7.5)
fontsize = 20
fig.suptitle('Bunch in the transverse plane', fontsize = fontsize)
ax.scatter(starting_x, starting_y)
ax.set_xlabel('x [m]', fontsize = fontsize)
ax.set_ylabel('y [m]', fontsize = fontsize)
ax.grid()
plt.tight_layout()
# %%
# We can also track the bunch through the whole line
# Now we perform more turns
N_turns = 10
collider['lhcb1'].track(gaussian_bunch, num_turns=N_turns)
# %%
# We can plot histograms of the particles
ending_x = ctx.nparray_from_context_array(gaussian_bunch.x).copy()
fig, ax = plt.subplots(1,1)
fig.set_size_inches(18.5, 10.5)
fontsize = 20
fig.suptitle('Comparison between starting and ending distribution', fontsize = fontsize)
ax.hist(starting_x, bins = 100, label = 'starting distribution')
ax.hist(ending_x, bins = 100, label = 'ending distribution', alpha = 0.5)
ax.set_xlabel('x [m]', fontsize = fontsize)
ax.grid()
ax.legend()
plt.tight_layout()
# The distribution changed, as expected










