# Simulations Onboarding Project - Fall 2026 (fs-5 design cycle)

- All parts follow exact same template (template.py)
- Parameters allows configeration of:
    * Simulation time
    * Matplotlib
    * Initial values
    * Constants
    * Data storage
- Parameters is a dataclass that can easily accomdate additions.
- Steps is where all calculations occur for each timestep.
- You can modify:
    * Input conditions (if-else statements)
    * calcuations
- Matplotlib is used to animate the car in a plot.
  The car is simulated by the red rectangle
- If enabled in parameters, the program will also output a table of all the data collected during the simulation after it is completed.