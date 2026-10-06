PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np
import sys

@dataclass
class State:
    velocity:float
    time:float
    xpos:float
    ypos:float

time_step = 0.01
plot_size = 500

def step (state:State) -> State:
    #constants
    air_density = 1.2
    cross_sectional_area = 1.2
    drag_coefficient = 0.7
    mass = 300

    #time based conditions that determine driver_input
    if (state.time <= 10):
        driver_input = 5
    else:
        driver_input = 0

    #calculations
    drag = 0.5 * cross_sectional_area * drag_coefficient * air_density * (state.velocity**2)
    net_accel = driver_input - (drag/mass)

    #create and return a new State object using calculated values
    return State(
        velocity = state.velocity + (net_accel * time_step),
        time = state.time + time_step, 
        xpos = state.xpos + (state.velocity * time_step),
        ypos = 0.0
        )

def animate (i):
    global s0, ani
    s0 = step(s0)    
    if (s0.time >= 10 and s0.velocity <= 0.1):
        print("Simulation Stopped")
        ani.event_source.stop()
    
    ax.clear()
    ax.scatter([s0.xpos],[s0.ypos], s = 200, c = 'red', marker = 's')
    ax.set_xlim((s0.xpos // plot_size) * plot_size, (s0.xpos // plot_size + 1) * plot_size)
    ax.set_ylim(0, 10)
    return ax,

s0 = State(velocity = 0, time = 0, xpos = 0, ypos = 0)

fig = plt.figure(figsize=(5,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(0, 10)
ax.set_ylim(-2, 2)
# these lines are so the animation doesnt zoom in or out
plt.pause(3)
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()
