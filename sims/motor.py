PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    velocity:float
    time:float
    xpos:float
    ypos:float

time_step = 0.01
plot_size = 150

def step (state:State) -> State:
    #constants
    mass = 300
    max_propulsion_force = 2000
    max_velocity = 27

    if (state.time <= 3):
        driver_input = state.time/7
    elif (state.time <= 23):
        driver_input = 1.0
    else:
        driver_input = 0.0

    
    force = max_propulsion_force * driver_input * (1 - (state.velocity/max_velocity))
    accel = force/mass

    return State(
        velocity = state.velocity + (accel * time_step),
        time = state.time + time_step, 
        xpos = state.xpos + (state.velocity * time_step),
        ypos = 0.0
        )

def animate (i):
    global s0
    s0 = step(s0)    
    ax.clear()
    ax.scatter([s0.xpos],[s0.ypos], s = 200, c = 'red', marker = 's')
    ax.set_xlim((s0.xpos // plot_size) * plot_size, (s0.xpos // plot_size + 1) * plot_size)
    ax.set_ylim(0, 10)
    return ax,

s0 = State(velocity = 0, time = 0, xpos = 0, ypos = 0)

fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
# these lines are so the animation doesnt zoom in or out
plt.pause(3)
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()
