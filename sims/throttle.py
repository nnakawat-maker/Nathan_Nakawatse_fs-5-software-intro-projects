PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    v:float
    t:float
    xpos:float
    ypos:float

time_step = 0.01

def step (state:State) -> State:
    #constants
    m = 300
    mmt = 180
    r = 0.216
    gr = 300

    if (state.t <= 7):
        driver_input = state.t/7
    elif (state.t <= 22):
        driver_input = 1.0
    else:
        driver_input = 0.0

    c_torque = driver_input * mmt
    f = (c_torque * gr) / r
    a = f/m

    new_v = state.v + (a * time_step)
    new_xpos = state.xpos + (state.v * time_step)
    new_t = state.t + time_step

    return State(v = new_v, t = new_t, xpos = new_xpos, ypos = 0.0)

def animate (i):
    global s0
    s0 = step(s0)    
    ax.clear()
    ax.scatter([s0.xpos],[s0.ypos], s = 200, c = 'red', marker = 's')
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 10)
    return ax,

s0 = State(v = 0, t = 0, xpos = 0, ypos = 0)

fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
# these lines are so the animation doesnt zoom in or out
plt.pause(3)
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()
