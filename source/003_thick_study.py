# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xpart as xp
import yaml

# %%
collider = xt.Multiline.from_json('../data/collider.json')
collider.build_trackers()

# %%
twiss_b1 = collider['lhcb1'].twiss()
twiss_b2 = collider['lhcb2'].twiss().reverse()

# %%
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
plt.tight_layout()

# %%
import matplotlib.patches as patches

def plotLatticeSeries(ax, twiss, element_name, series, height=1., v_offset=0., color='r',alpha=0.5):
    aux=series
    ax.add_patch(
    patches.Rectangle(
        (twiss_b1['s', element_name]-aux['length']*0, v_offset-height/2.),   # (x,y)
        aux['length'],          # width
        height,          # height
        color=color, alpha=alpha
    )
    )
    return;


# %%
# twiss_b1[:, ['s.arc.34.b1', 'e.arc.34.b1']]
fig = plt.figure(figsize=(20,10))

# set up subplot grid
#gridspec.GridSpec(3,3)
fontsize = 10
ax1 = plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)
plt.plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'][0:300],0*twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'][0:300],'k')
plt.plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'][0:300],twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['x'][0:300]*1e4,'green',label='x')

my_dict = collider.lhcb1.to_dict()
for ii in (twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['name']):
    if((ii.startswith('mq.')) and ii.endswith('b1')):
        print(ii)
        aux =my_dict['elements'][ii]
        k1l = my_dict['elements'][ii]['k1']*my_dict['elements'][ii]['length']
        plotLatticeSeries(plt.gca(),twiss_b1, ii, aux, height=k1l, v_offset=k1l/2, color='red')
        if(ii == 'mq.14r3.b1'):
            break
ax1.set_ylabel(r'$K1L$ [1/m]', color='red')  # we already handled the x-label with ax1
ax1.tick_params(axis='y', labelcolor='red')




#ax1.set_xlim(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'][0],600)


for ii in (twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['name']):
    if((ii.startswith('mb.')) and ii.endswith('b1')):
        print(ii)
        aux =my_dict['elements'][ii]
        kl = my_dict['elements'][ii]['k0']*my_dict['elements'][ii]['length']
        plotLatticeSeries(plt.gca(),twiss_b1, ii, aux, height=kl, v_offset=kl/2, color='blue')
        if(ii == 'mb.c15r3.b1'):
            break
 # instantiate a second axes that shares the same x-axis
color = 'blue'
# ax2.set_ylabel(r'$\theta$=K0L [rad]', color=color)  # we already handled the x-label with ax1
# ax2.tick_params(axis='y', labelcolor=color)
plt.title('LHC lattice in the arc 34', fontsize = fontsize)
plt.xlabel('s [m]', fontsize = fontsize)
plt.axvline(twiss_b1['s', 'mq.12r3.b1' ], color = 'b', label = 'mq.12r3.b1')
plt.axvline(twiss_b1['s', 'mq.12r3.b1_exit' ], color = 'r', label = 'mq.12r3.b1_exit')
plt.legend(fontsize = fontsize)

plt.grid()

# %%
def set_orbit_from_config(collider, config):
    print('Setting optics as from config')
    for ii in ['on_x1', 'on_sep1', 'on_x2', 'on_sep2', 'on_x5',
               'on_sep5', 'on_x8h', 'on_x8v', 'on_sep8h', 'on_sep8v',
               'on_a1', 'on_o1', 'on_a2', 'on_o2', 'on_a5', 'on_o5', 'on_a8', 
               'on_o8', 'on_disp', 'on_crab1', 'on_crab5', 'on_alice_normalized', 
               'on_lhcb_normalized', 'on_sol_atlas', 'on_sol_cms', 'on_sol_alice', 
               'vrf400', 'lagrf400.b1', 'lagrf400.b2']:
        collider.vars[ii] = config['config_collider']['config_knobs_and_tuning']['knob_settings'][ii]

with open('../data/config.yaml', "r") as fid:
        config = yaml.safe_load(fid)
set_orbit_from_config(collider, config)
twiss_b1 = collider['lhcb1'].twiss()
twiss_b2 = collider['lhcb2'].twiss().reverse()
plt.plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'][0:300],twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['x'][0:300],'k')







# fig = plt.figure(figsize=(13,8))
# ax1=plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)
# plt.plot(twiss_b1['s'],0*twiss_b1['s'],'k')


# DF=twiss_b1[(twiss_b1['keyword']=='quadrupole')]
# for i in range(len(DF)):
#     aux=DF.iloc[i]
#     plotLatticeSeries(plt.gca(),aux, height=aux.k1l, v_offset=aux.k1l/2, color='r')
# %%
