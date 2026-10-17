PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass, field
import numpy as np
import gspread

# Simulation Parameters
@dataclass(frozen=True)
class Parameters:
    """
    An object that stores the simulation parameters.
    Can be edited to change simulation values, or add new parameter variables.
    Units are Base SI unless otherwise stated.
    """
    # Time Config
    simulationDuration: float = 22.0 # The simulation ends when time > this variable. '-1' makes it run indefinitely
    simulationEndCondition: float = -1 # The simulation ends when xVelocity <= this variable '-1' makes it so there is no end condition.
    simulationEndConditionStart: float = 10.0 # The time to start checking for the simulation end condition, if there is one
    timestep: float = 0.01
    # Plot Config
    xPlotSize: int = 300
    yPlotSize: int = 10
    expandGraph: bool = True # If true, the simulation's graph plot will change pages to fit the car
    # Initial Variable Config
    initPosition: list[float] = field(default_factory = lambda: [0.0, 0.0])
    initVelocity: list[float] = field(default_factory = lambda: [0.0, 0.0])
    # Constant Config
    maxPropulsionForce: float = 2000
    vMax: float = 27
    mass: float = 300.0
    # Sheet Config
    spreadsheetKey: str = '1zBsF46AYu-NVthRxKRAfHhW2454yw_v6TmWknU5z_Wk' # Key of spreadsheet to input data into
    worksheet: str = 'Motor'


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


class Sheet:
    def __init__ (self, worksheet: gspread.worksheet, initdata:list):
        self.worksheet = worksheet
        self.data = [initdata]

    def addData (self, data:list):
        roundedData = [round(i, 5) for i in data]
        self.data.append(roundedData)

    def pushData (self):
        self.worksheet.clear()
        self.worksheet.update(self.data, 'A2')

def step (state:State) -> State:
    """
    Steps the car's state forwards by one timestep, performs calculations for this new State, 
    and returns a newly updates State object.
    Can be edited to change input conditions and times, and change equations for calculation
    """
    # Driver input conditions
    if (state.time <= 7):
        driverInput = state.time / 7
    else:
        driverInput = 1.0
    # Calculate acceleration
    force = parameters.maxPropulsionForce * driverInput * (1 - (state.xVelocity / parameters.vMax))
    acceleration = force / parameters.mass

    newTime = state.time + parameters.timestep
    newXPos = state.xPos + (state.xVelocity * parameters.timestep)
    newYPos = 0.0
    newXVelocity = max(state.xVelocity + (acceleration * parameters.timestep), 0.0)
    newYVelocity = 0.0
    sheet.addData([newTime, newXPos, newYPos, newXVelocity, newYVelocity, acceleration * parameters.timestep])

    return State(
        time = newTime,
        xPos = newXPos,
        yPos = newYPos,
        xVelocity = newXVelocity,
        yVelocity = newYVelocity
    )


def animate (i):
    """
    Is repeatedly called by FuncAnimation, calls step() and edits the graph.
    """
    global s0, car
    # Step forwards and get updated state
    s0 = step(s0)  
    
    # Check for simulation stop conditions
    if ((parameters.simulationDuration != -1 and s0.time > parameters.simulationDuration) or
        (parameters.simulationEndCondition != -1 and s0.time >= parameters.simulationEndConditionStart
        and s0.xVelocity <= parameters.simulationEndCondition)
        ):
        print("Simulation Terminated")
        sheet.pushData()
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

gc = gspread.oauth()
sh = gc.open_by_key(parameters.spreadsheetKey)
worksheet = sh.worksheet(parameters.worksheet)
sheet = Sheet(worksheet = worksheet, initdata = [0, parameters.initPosition[0], parameters.initPosition[1],
                                                 parameters.initVelocity[0], parameters.initVelocity[1], 0.0])
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
