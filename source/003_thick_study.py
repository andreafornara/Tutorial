# %%
import xtrack as xt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
import xpart as xp
import yaml
import matplotlib.patches as patches
import xobjects as xo
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
ctx = xo.ContextCpu()

# %%
'''
In this snippet we will look at the optics quantities of the `ARC`.

The big difference with respect to the previous snippet is that we will use the `twiss` method: in this case the reference system is the one of the beam.
This is the reference system that is used in the vast majority of the cases.

Our task is to understand how the twiss quantities can be retrieved and to see how the LHC arc works.

We start by loading the collider from the json file, as always. Then we call the twiss method on the lhcb1 line.
'''

# %%
collider = xt.Multiline.from_json('../data/collider.json')
collider.build_trackers()
my_dict = collider.lhcb1.to_dict()

# %%
twiss_b1 = collider['lhcb1'].twiss()

# %%
'''
We can see, for example, the columns of the twiss dataframe, which contain several important quantities.
'''

# %%
print(twiss_b1.cols)
print('The beta functions are', twiss_b1['betx'], twiss_b1['bety'])
print('The names of the elements are ', twiss_b1['name'])

# %%
'''
Now we can plot the beta functions in the ARC together with dipole and quadrupole magnets.
The convention is the following:
- The `dipole` magnets are in `blue`;
- The `quadrupole` magnets are in `red`;
The height of the each element is proportional to the integrated strength of the element.
We are now going to look at `ARC34` .

'''

# %%
fig = plt.figure(figsize=(30,25))
fontsize = 20
ax1 = plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)
plt.plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'],
         0*twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'],'k')
for ii in (twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['name']):
    if((ii.startswith('mq.')) and ii.endswith('b1')):
        aux =my_dict['elements'][ii]
        k1l = my_dict['elements'][ii]['k1']*my_dict['elements'][ii]['length']
        #print(ii, k1l)
        plotLatticeSeries(plt.gca(),twiss_b1, ii, aux, height=k1l, v_offset=k1l/2, color='red')
        # add a label for each quadrupole on top of it with its name
        name = ' '+ii.split('.')[1]+' '
        plt.gca().text(twiss_b1['s', ii], np.abs(k1l)/12, 
                       name, fontsize=13, color='black', horizontalalignment='center', verticalalignment='center')
ax1.set_ylabel(r'$K1L$ [1/m]', color='red')
ax1.tick_params(axis='y', labelcolor='red')
FODO_cell_length = twiss_b1['s','mq.28l2.b1']-twiss_b1['s','mq.30l2.b1']
ax2 = ax1.twinx() 
ax2.set_ylim(-10,10)
for ii in (twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['name']):
    if((ii.startswith('mb.')) and ii.endswith('b1')):
        aux =my_dict['elements'][ii]
        kl = my_dict['elements'][ii]['k0']*my_dict['elements'][ii]['length']
        plotLatticeSeries(plt.gca(),twiss_b1, ii, aux, height=kl*1000, v_offset=kl/2*1000, color='blue')
color = 'blue'
ax2.set_ylabel(r'$\theta$=K0L [mrad]', color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.title('LHC lattice in the ARC 34', fontsize = fontsize)
color = 'k'
ax3 = ax1.twinx() 
ax3.set_ylim(-200,200)
ax3.spines.right.set_position(("axes", 1.05))
plt.gca().plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'],
               twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['betx'],'k',label=r'$\beta_{x}$ function')
plt.gca().plot(twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['s'],
               twiss_b1.rows['s.arc.34.b1':'e.arc.34.b1', ]['bety'],'green',label=r'$\beta_{y}$ function')
ax3.set_ylabel(r'$\beta_{x,y}$ [m]', color=color)
ax3.tick_params(axis='y', labelcolor=color)
plt.legend(fontsize = fontsize)
ax1.set_xlabel('s [m]', fontsize = fontsize)
plt.grid()

# %%
'''
First of all some basic comments:
- An LHC `FODO` cell is defined from a defocusing quadrupole to the next defocusing quadrupole and it's length is 106.9 m;
- There are `23 FODO cells in an ARC`;
- Each `dipole kicks` by `5mrad`, so that, with 1232 dipoles around the machine, we get to 2pi (a circle);
- The `beta function` should be a `periodic` function, and this is (almost) the case;
- The beta function in x is opposite to the beta function in y, as expected since the 
`FODO cell focuses in one plane and defocuses in the other`;
Then some questions:
- `All the quadrupoles have the same integrated strength` (absolute value), but the beta function is not the same in all the FODO cells (look at the first and the last cell). Why?
- It is easy to predict the dipolar kick (we must make a circle), but what about the quadrupolar kick? How can we predict it?

The first question requires a bit of knowledge on the ARC and how it is controlled. 

Each ARC is powered by a `single power supply`, therefore all the quadrupoles in the ARC have the same integrated strength.
When multiple components of the machine need to be controlled all together we use something called `knob`. By changing the value of a
knob we can do several things. For example some knobs change the `crossing angle` at the IP, others help us with the `chromaticity` and so on.
By printing out the elements in the ARC you can discover something interesting, some `trim` quadrupoles (mqt):
'''

# %%
for ii in (twiss_b1.rows['s.arc.34.b1':'mq.19r3.b1', ]['name']):
    if((ii.startswith('mqt.')) and ii.endswith('b1')):
        aux =my_dict['elements'][ii]
        k1l_t = my_dict['elements'][ii]['k1']*my_dict['elements'][ii]['length']
        print('Name: ',ii,',k1L: ', k1l_t)

# %%
'''
You can see that the first two (and try to repeat the exercise for the last two) have a different integrated strength!

This is because the first (and last) are use to match the beta function at the entrance (and exit) of the ARC.
All the other ones are controlled by the following knobs:
'''

# %%
# Defocusing quadrupoles
print(collider.vars['kqtd.a34b1']._find_dependant_targets())
# Focusing quadrupoles
print(collider.vars['kqtf.a34b1']._find_dependant_targets())

# %%
'''
The first two are controlled by the following knobs (and you can guess the knobs for the last two):
'''

# %%
print(collider.vars['kqt12.r3b1']._find_dependant_targets())
print(collider.vars['kqt13.r3b1']._find_dependant_targets())

# %%
'''
Now we can try to answer the second question. A similar treatment of the problem is found in many books, 
for example in A. Wolski's book.

The idea is to equate the transfer matrix in terms of the FODO lattice parameters (k,L) 
and the transfer matrix in terms of the beta functions.
This leads to the following stability condition:



'''

# %%
x= np.arange(0,4.01,0.01)
y=2*np.arcsin(x/4)/np.pi
FODO_cell_length = twiss_b1['s','mq.28l2.b1']-twiss_b1['s','mq.30l2.b1']
LHCFODO = np.abs(k1l)*FODO_cell_length
y_LHC = 2*np.arcsin(LHCFODO/4)/np.pi
fig, ax1 = plt.subplots()
ax1.plot(x,y,'-')
ax1.set_ylabel("$\Delta \mu / \pi [rad]$", fontsize=16)
ax1.set_xlabel("$K*L_{quad}*L_{cell}$ [-]", fontsize=16)
ax1.grid()
ax1.tick_params(axis='both', labelsize=16)
phase_advance = np.abs((twiss_b1['mux','mq.30l2.b1']-twiss_b1['mux','mq.28l2.b1']))
ax1.plot(LHCFODO, y_LHC, '*', markersize=10, color='red', label='LHC FODO cell')
ax1.set_title('Relation between phase advance and FODO cell properties', fontsize=16)
ax1.legend(fontsize=10)
plt.tight_layout()

# %%
'''
So regarding the LHC FODO each cell provides a ~pi/2 phase advance.

From the same equation we can also impose that the beta function maximum and minimum are small enough to avoid the
beam pipe to be too large. In a FODO cell the average beta function is minimized whern each cell provides a phase advance of pi/2.
'''

# %%
x=np.arange(0.5,3.90,0.01)
betamax=(1+(x/4))/(np.sin(2*np.arcsin(x/4)))
betamin=(1-(x/4))/(np.sin(2*np.arcsin(x/4)))
x_LHC = np.abs(k1l)*FODO_cell_length
betamax_LHC=(1+(x_LHC/4))/(np.sin(2*np.arcsin(x_LHC/4)))
betamin_LHC=(1-(x_LHC/4))/(np.sin(2*np.arcsin(x_LHC/4)))
fig, ax1 = plt.subplots()
ax1.plot(x,betamax,'-',label=r"$\beta_{max}/L_{cell}$")
ax1.plot(x,betamin,'-',label=r"$\beta_{min}/L_{cell}$")
ax1.plot(x_LHC,betamax_LHC, '*', markersize=10, color='red', label=r'LHC FODO cell $\beta_{max}$')
ax1.plot(x_LHC,betamin_LHC, '*', markersize=10, color='red', label=r'LHC FODO cell $\beta_{min}$')
ax1.set_ylabel("[-]", fontsize=16)
ax1.set_xlabel("$K*L_{quad}*L_{cell}$ [-]", fontsize=16)
plt.grid()
plt.legend()
plt.tick_params(axis='both', labelsize=16)
plt.tight_layout() 

# %%
'''
Now we can try to question ourselves: the arc itself is a periodic structure, `can we find the beta functions`?

To do this we need to build a new line with the arc only. We can do this by using the following:
'''

# %%
start = 'mq.15r3.b1_entry'
end = 'mq.15l4.b1_entry'
my_line = xt.Line(
    elements=(collider['lhcb1'].element_dict),
    element_names=twiss_b1.rows[start:end, ]['name'])
my_line.build_tracker()

# %%
'''
Notice that we skipped the first and last quadrupoles, since they are used to match the beta function 
at the entrance and exit of the arc and therefore would not give us a periodic solution.

We can twiss (in 4D) the line and plot the beta functions. 
'''

# %%
ref = xp.Particles(mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9)
twiss_b1_line = my_line.twiss(particle_ref=ref, method='4d')
plt.plot(twiss_b1_line.s,twiss_b1_line.betx, label='betx')
plt.plot(twiss_b1_line.s,twiss_b1_line.bety, label='bety')
plt.xlabel('s [m]')
plt.ylabel('beta [m]')
plt.grid()
plt.legend()

# %%
'''
Indeed we recovered the periodic solution.

Now something more interesting: can we find the beta functions of the arc by using the tracking?

In Xsuite the twiss is a tracking anyway, so we should be able to do this. 

The procedure is the following:
- We launch one particle, and since the motion is uncoupled we can directly input a starting x and y coordinate;
- This particle is tracked for several turns, and this will fill the phase space ellipse in both planes since at each
turn the particle will reach a slightly different position;
- At this point from the turn by turn coordinates we can calculate the beta functions via `SVD`.
'''

# %%
#We define the function to retrieve the beta functions
def getbeta(w,pw):
    U, s ,V = np.linalg.svd([w,pw])
    N = np.dot(U,np.diag(s))
    theta = np.arctan2(-N[0,1],N[0,0])
    R = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
    W = np.dot(N,R)
    betaw = np.abs(W[0,0]/W[1,1])
    alfw = W[1,0]/W[1,1]
    ew = s[0]*s[1]/(len(w))
    return betaw,alfw,ew

# %%
x = 1e-6
y = 1e-6
aux = xp.Particles(ctx = ctx,mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9, x = x, y=y)
n_turns = 5000
xs = []
pxs = []
ys = []
pys = []
for ii in range(n_turns):
    xs.append(ctx.nparray_from_context_array(aux.x).copy())
    pxs.append(ctx.nparray_from_context_array(aux.px).copy())
    ys.append(ctx.nparray_from_context_array(aux.y).copy())
    pys.append(ctx.nparray_from_context_array(aux.py).copy())
    my_line.track(aux, num_turns=1)
xs = np.array(xs)
pxs = np.array(pxs)
ys = np.array(ys)
pys = np.array(pys)

# %%
plt.plot(xs,pxs,'o')
betax, alfx, ex = getbeta(xs.reshape(n_turns),pxs.reshape(n_turns))
print('Tracking betx:',betax,', alfa:',alfx)
print('Twiss betx:',twiss_b1_line.betx[0],', alfa:',twiss_b1_line.alfx[0])
plt.plot(ys,pys,'o')
betay,alfay,ey = getbeta(ys.reshape(n_turns),pys.reshape(n_turns))
print('Tracking bety:',betay,', alfa:',alfay)
print('Twiss bety:',twiss_b1_line.bety[0],', alfa:',twiss_b1_line.alfy[0])
plt.xlabel('x,y [m]')
plt.ylabel('px,py [rad]')
plt.grid()
plt.title('Phase space ellipses')

# %%

