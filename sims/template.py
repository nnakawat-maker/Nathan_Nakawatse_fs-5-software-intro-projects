PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass, field
import numpy as np
import sys

# Simulation Parameters
@dataclass(frozen=True)
class Parameters:
    """
    An object that stores the simulation parameters.
    Can be edited to change simulation values, or add new parameter variables.
    Units are Base SI unless otherwise stated.
    """
    # Time Config
    simulationDuration: float = 10.0 # The simulation ends when time >= this variable. '-1' makes it run indefinitely
    simulationEndCondition: float = -1 # The simulation ends when xVelocity <= this variable '-1' makes it so there is no end condition.
    simulationEndConditionStart: float = 10.0 # The time to start checking for the simulation end condition, if there is one
    timestep: float = 0.1
    # Plot Config
    xPlotSize: int = 300
    yPlotSize: int = 10
    expandGraph: bool = True # If true, the simulation's graph plot will change pages to fit the car
    # Initial Variable Config
    initPosition: list[float] = field(default_factory = lambda: [0.0, 0.0])
    initVelocity: list[float] = field(default_factory = lambda: [0.0, 0.0])
    # Constant Config
    mass: float = 300.0
    # Data Config
    storeData: bool = True # If true, the Data dataclass will be used to store simulation data


@dataclass
class State:
    """
    An object that stores the car's data related to its position and velocity at a specific time.
    """
    time: float
    xPos: float
    yPos: float
    xVelocity: float
    yVelocity: float


@dataclass
class Data:
    """
    An object that stores simulation results
    """
    length: int = 0
    timeList: list[float] = field(default_factory = list)
    xPosList: list[float] = field(default_factory = list)
    yPosList: list[float] = field(default_factory = list)
    xVelocityList: list[float] = field(default_factory = list)
    yVelocityList: list[float] = field(default_factory = list)

    def addData (self, time:float, xPos:float, yPos:float, xVelocity:float, yVelocity:float):
        """
        Takes data, and adds it to lists for storage
        """
        self.length += 1
        self.timeList.append(time)
        self.xPosList.append(xPos)
        self.yPosList.append(yPos)
        self.xVelocityList.append(xVelocity)
        self.yVelocityList.append(yVelocity)

    def printData (self):
        """
        Iterates through lists, and prints data. Also adds labels at top and bottom of data
        """
        print(f"{'time':>10} {'xPos':>10} {'yPos':>10} {'xVelocity':>10} {'yVelocity':>10}")

        for i in range(self.length):
            print(f"{self.timeList[i]:>10.3f} {self.xPosList[i]:>10.3f} {self.yPosList[i]:>10.3f} {self.xVelocityList[i]:>10.3f} {self.yVelocityList[i]:>10.3f}")

        print(f"{'time':>10} {'xPos':>10} {'yPos':>10} {'xVelocity':>10} {'yVelocity':>10}")

def step (state:State) -> State:
    """
    Steps the car's state forwards by one timestep, performs calculations for this new State, 
    and returns a newly updates State object.
    Can be edited to change input conditions and times, and change equations for calculation
    """
    # Driver input conditions
    if (state.time <= 10):
        driverInput = 1
    else:
        driverInput = 0
    # Calculate acceleration
    acceleration = driverInput

    # Return a new State with updated time, position and velocity
    return State(
        time = state.time + parameters.timestep,
        xPos = state.xPos + (state.xVelocity * parameters.timestep),
        yPos = 0.0,
        xVelocity = state.xVelocity + (acceleration * parameters.timestep),
        yVelocity = 0.0
    )

def animate (i):
    """
    Is repeatedly called by FuncAnimation, calls step() and edits the graph.
    """
    global s0, car
    # Step forwards and get updated state
    s0 = step(s0)  

    # Update Data if necessary
    if (parameters.storeData):
        data.addData(s0.time, s0.xPos, s0.yPos, s0.xVelocity, s0.yVelocity)
        
    # Check for simulation stop conditions
    if ((parameters.simulationDuration != -1 and s0.time >= parameters.simulationDuration) or
        (parameters.simulationEndCondition != -1 and s0.time >= parameters.simulationEndConditionStart
        and s0.xVelocity <= parameters.simulationEndCondition)
        ):
        print("Simulation Terminated")
        if (parameters.storeData):
            data.printData()
        ani.event_source.stop()
        return

    # Update the car's coordinates
    car.set_offsets([[s0.xPos, s0.yPos]])

    # Check if the car's coordinates exceed the current page of the plot
    if (parameters.expandGraph):
        xCurrentPage = s0.xPos // parameters.xPlotSize
        xMin = xCurrentPage * parameters.xPlotSize
        xMax = (xCurrentPage + 1) * parameters.xPlotSize
        
        yCurrentPage = s0.yPos // parameters.yPlotSize
        yMin = yCurrentPage * parameters.yPlotSize
        yMax = (yCurrentPage + 1) * parameters.yPlotSize

        # Update the limits of the plot
        if ax.get_xlim() != (xMin, xMax):
            ax.set_xlim(xMin, xMax)
        if ax.get_ylim() != (yMin, yMax):
            ax.set_ylim(yMin, yMax)
    return


parameters = Parameters()
if (parameters.storeData):
    data = Data()
s0 = State(time = 0, xPos = parameters.initPosition[0], yPos = parameters.initPosition[1], xVelocity = parameters.initVelocity[0], yVelocity= parameters.initVelocity[1])

fig = plt.figure(figsize = (3,3), dpi = 150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
# These lines are so the animation doesnt zoom in or out
plt.pause(3)

ax.set_xlim(0, parameters.xPlotSize)
ax.set_ylim(0, parameters.yPlotSize)

car = ax.scatter([parameters.initPosition[0]],[parameters.initPosition[1]], s = 200, c = 'red', marker = 's')

ani = animation.FuncAnimation(fig, animate, interval = 0)
plt.show()
