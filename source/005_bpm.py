# %%
import json
import xtrack as xt
import xpart as xp
import xobjects as xo
from matplotlib import pyplot as plt

context = xo.ContextCpu()

with open('../data/collider_thin.json') as f:
    dct = json.load(f)

line = xt.Line.from_dict(dct['lines']['lhcb1'])
line_edited =line.copy()

# %%
my_particle = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9)
line.particle_ref = my_particle

line.build_tracker()
aux = line.twiss()

# %%
monitors = {}  # Create an empty dictionary to store the monitors
num_particles = 1
num_turns = 1

for jj, ii in enumerate((['ip3']+list(aux[:, 'bpm.*']['name']))):
    monitor_name = f"mymon_{ii.replace('.', '_')}"
    monitors[monitor_name] = xt.ParticlesMonitor(start_at_turn=0, stop_at_turn=1, num_particles=num_particles)
    line_edited.insert_element(index=ii,
                                element=monitors[monitor_name], 
                                name=monitor_name)

# %%
line_edited.particle_ref = my_particle
line_edited.build_tracker()
line_edited.twiss()[:, 'mymon_.*']

# %%
particles = xp.Particles(
                    mass0=xp.PROTON_MASS_EV, q0=1, energy0=7000e9, x=-0.001)
line_edited.track(particles, num_turns=num_turns)

# %%

s_list = [monitors[ii].s[0,0] for ii in monitors]
x_list = [monitors[ii].x[0,0] for ii in monitors]
plt.plot(s_list, x_list, '.-r')