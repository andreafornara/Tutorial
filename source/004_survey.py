# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
import xpart as xp
import yaml
import matplotlib.patches as patches

# %%
collider = xt.Multiline.from_json('../data/collider.json')
collider.build_trackers()

# %%
twiss_b1 = collider['lhcb1'].twiss()
twiss_b2 = collider['lhcb2'].twiss().reverse()
my_dict = collider.lhcb1.to_dict()
# %%
survey_b1 = collider['lhcb1'].survey()
survey_b2 = collider['lhcb2'].survey().reverse()
# %%
#plot the surver x vs z
fig, ax = plt.subplots(1,1)
fig.set_size_inches(8.5, 8.5)
fontsize = 20
fig.suptitle('Survey of the LHC lattice for Beam 1 and Beam 2',fontsize = fontsize )
ax.plot(survey_b1['X'], survey_b1['Z'])  
#ax.plot(survey_b2['X'], survey_b2['Z'])
ip_links = ['12','23','34','45','56','67','78','81']
for ii in ip_links:
    ax.plot(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'],
            survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'],
            color='green')
    #write the 'ARC'+ii beside the arc
    ax.text(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'].mean(),
            survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'].mean(),
            'ARC'+ii, fontsize=fontsize, color='green')
    
r_ip = ['r1','r2','r3','r4','r5','r6','r7','r8']
l_ip = ['l1','l2','l3','l4','l5','l6','l7','l8']
for ii in r_ip:
    ax.plot(survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['X'],
            survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['Z'],
            color='purple')

for ii in l_ip:
    ax.plot(survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['X'],
            survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['Z'],
            color='purple')


ax.plot(survey_b1.rows['ip1']['X'], survey_b1.rows['ip1']['Z'], '*', markersize=20, color='red')
ax.text(survey_b1.rows['ip1']['X'], survey_b1.rows['ip1']['Z']-380,
        'IP1', fontsize=fontsize, color='red')
ax.plot(survey_b1.rows['ip2']['X'], survey_b1.rows['ip2']['Z'], '*', markersize=20, color='red')
ax.text(survey_b1.rows['ip2']['X']+300, survey_b1.rows['ip2']['Z'],
        'IP2', fontsize=fontsize, color='red')
ax.plot(survey_b1.rows['ip5']['X'], survey_b1.rows['ip5']['Z'], '*', markersize=20, color='red')
ax.text(survey_b1.rows['ip5']['X'], survey_b1.rows['ip5']['Z']+120,
        'IP5', fontsize=fontsize, color='red')
ax.plot(survey_b1.rows['ip8']['X'], survey_b1.rows['ip8']['Z'], '*', markersize=20, color='red')
ax.text(survey_b1.rows['ip8']['X']-800, survey_b1.rows['ip8']['Z'],
        'IP8', fontsize=fontsize, color='red')
#same for ip3,4,6,7 but in black
ax.plot(survey_b1.rows['ip3']['X'], survey_b1.rows['ip3']['Z'], '*', markersize=20, color='black')
ax.text(survey_b1.rows['ip3']['X'], survey_b1.rows['ip3']['Z']+120,
        'IP3', fontsize=fontsize, color='black')
ax.plot(survey_b1.rows['ip4']['X'], survey_b1.rows['ip4']['Z'], '*', markersize=20, color='black')
ax.text(survey_b1.rows['ip4']['X'], survey_b1.rows['ip4']['Z']+120,
        'IP4', fontsize=fontsize, color='black')
ax.plot(survey_b1.rows['ip6']['X'], survey_b1.rows['ip6']['Z'], '*', markersize=20, color='black')
ax.text(survey_b1.rows['ip6']['X'], survey_b1.rows['ip6']['Z']+120,
        'IP6', fontsize=fontsize, color='black')
ax.plot(survey_b1.rows['ip7']['X'], survey_b1.rows['ip7']['Z'], '*', markersize=20, color='black')
ax.text(survey_b1.rows['ip7']['X'], survey_b1.rows['ip7']['Z']+120,
        'IP7', fontsize=fontsize, color='black')    
ax.set_xlabel('x [m]', fontsize = fontsize)
ax.set_ylabel('z [m]', fontsize = fontsize)
ax.grid()
ax.legend(fontsize = fontsize)
plt.tight_layout()

# %%
#zoom in on IP3
fig, ax = plt.subplots(1,1)
fig.set_size_inches(8.5, 8.5)
fontsize = 20

ii = '23'
ax.plot(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'],
            survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'],
            color='green')
# ax.text(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'].mean(),
#         survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'].mean(),
#         'ARC'+ii, fontsize=fontsize, color='green')

ii = '34'
ax.plot(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'],
            survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'],
            color='green')
# ax.text(survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['X'].mean(),
#         survey_b1.rows['s.arc.'+ii+'.b1':'e.arc.'+ii+'.b1', ]['Z'].mean(),
#         'ARC'+ii, fontsize=fontsize, color='green')

ii = 'r3'
ax.plot(survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['X'],
        survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['Z'],
        color='purple')
ii = 'l3'
ax.plot(survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['X'],
        survey_b1.rows['s.ds.'+ii+'.b1':'e.ds.'+ii+'.b1', ]['Z'],
        color='purple')

#straight section
ax.plot(survey_b1.rows['ip3':'s.ds.'+'r3'+'.b1', ]['X'],
        survey_b1.rows['ip3':'s.ds.'+'r3'+'.b1', ]['Z'],
        color='red')
ax.plot(survey_b1.rows['e.ds.'+'l3'+'.b1':, ]['X'],
        survey_b1.rows['e.ds.'+'l3'+'.b1':, ]['Z'],
        color='red')


# survey_b1.rows['s.ds.'+'r3'+'.b1':'e.ds.'+'r3'+'.b1', ]['Z']



ax.plot(survey_b1.rows['ip3']['X'], survey_b1.rows['ip3']['Z'], '*', markersize=20, color='black')
plt.xlim(-100,10)
plt.ylim(-800,800)
plt.grid()

# %%
fig, ax = plt.subplots(1,1)
fig.set_size_inches(8.5, 8.5)
fontsize = 20
fig.suptitle('Survey of the LHC lattice for Beam 1 and Beam 2',fontsize = fontsize )
ax.plot(survey_b1.rows[:, 'ip4%%-10': 'ip4%%+10']['X'], survey_b1.rows[:, 'ip4%%-10': 'ip4%%+10']['Z'])
ax.plot(survey_b2.rows[:, 'ip4%%-25': 'ip4%%+25']['X'], survey_b2.rows[:, 'ip4%%-25': 'ip4%%+25']['Z'])




# %%
fig, ax = plt.subplots(1,1)
fig.set_size_inches(8.5, 8.5)
fontsize = 20
fig.suptitle('Survey of the LHC lattice for Beam 1 and Beam 2',fontsize = fontsize )
ax.plot(survey_b1.rows[:, 'ip5%%-100': 'ip5%%+100']['X'], survey_b1.rows[:, 'ip5%%-100': 'ip5%%+100']['Z'])
ax.plot(survey_b2.rows[:, 'ip5%%-100': 'ip5%%+100']['X'], survey_b2.rows[:, 'ip5%%-100': 'ip5%%+100']['Z'])



#%%



# %%
fig, ax = plt.subplots(1,1)
fig.set_size_inches(20, 8.5)
fontsize = 20
#ax.plot(survey_b1['Z'],survey_b1['X']-survey_b2['X']) 
ax.plot(survey_b1.rows['ip1']['Z'],survey_b1.rows['ip1']['X']-survey_b2.rows['ip1']['X'], '*', markersize=20, color='red')
ax.plot(survey_b1.rows['ip2']['Z'],survey_b1.rows['ip2']['X']-survey_b2.rows['ip2']['X'], '*', markersize=20, color='red')
ax.plot(survey_b1.rows['ip5']['Z'],survey_b1.rows['ip5']['X']-survey_b2.rows['ip5']['X'], '*', markersize=20, color='red')
ax.plot(survey_b1.rows['ip8']['Z'],survey_b1.rows['ip8']['X']-survey_b2.rows['ip8']['X'], '*', markersize=20, color='red')

ax.plot(survey_b1.rows['ip3']['Z'],survey_b1.rows['ip3']['X']-survey_b2.rows['ip3']['X'], '*', markersize=20, color='k')
ax.plot(survey_b1.rows['ip4']['Z'],survey_b1.rows['ip4']['X']-survey_b2.rows['ip4']['X'], '*', markersize=20, color='k')
ax.plot(survey_b1.rows['ip6']['Z'],survey_b1.rows['ip6']['X']-survey_b2.rows['ip6']['X'], '*', markersize=20, color='k')
ax.plot(survey_b1.rows['ip7']['Z'],survey_b1.rows['ip7']['X']-survey_b2.rows['ip7']['X'], '*', markersize=20, color='k')

print('ip1 difference =',survey_b1.rows['ip1']['X']-survey_b2.rows['ip1']['X'])
print('ip2 difference =',survey_b1.rows['ip2']['X']-survey_b2.rows['ip2']['X'])
print('ip5 difference =',survey_b1.rows['ip5']['X']-survey_b2.rows['ip5']['X'])
print('ip8 difference =',survey_b1.rows['ip8']['X']-survey_b2.rows['ip8']['X'])

print('ip3 difference =',survey_b1.rows['ip3']['X']-survey_b2.rows['ip3']['X'])
print('ip4 difference =',survey_b1.rows['ip4']['X']-survey_b2.rows['ip4']['X'])
print('ip6 difference =',survey_b1.rows['ip6']['X']-survey_b2.rows['ip6']['X'])
print('ip7 difference =',survey_b1.rows['ip7']['X']-survey_b2.rows['ip7']['X'])


ax.set_xlabel('z [m]', fontsize = fontsize)
ax.set_ylabel('x [m]', fontsize = fontsize)
ax.grid()
ax.legend(fontsize = fontsize)
plt.tight_layout()
# %%
