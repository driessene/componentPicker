# Component Picker
This program returns the best components for a system based on output functions and targets. For example, for a user to select the proper resistors for an OpAmp with a target gain of -2, the user will input the equation to minimize based on the values of components in the system. The program will return several sets of components that will suit the user's needs.
## Components
### Passive Components
A class used to describe a very simple passive component. Only holds nominal value and tolerance.
### Resistors
 A passive component with an additional power rating
### Capacitors
A passive component with an additional voltage rating
## Systems
Holds components, and output equations. Can evaluate the output of itself based on the components and equations. Can evaluate a single output or all outputs as a list
## Problems
This is the main feature of this program. Problems hold a dictionary whose key represents a component. Each key holds a list of every possible component for this component. When provided with all targets, output equations, and components, the problem will iteratively test every possible system based on the total error from the targets.
### Using Problems
Problems must be given:
- A dictionary whose key is the name of a component. Each item in the dictionary is a list holding each possible component
- A dictionary whose key is a name of an output equation. Each item in the dictionary must be a function. This can be acomplished by passing a lambda function
- A diciotnary whose key is the name of an output equation. Each item in the dicionary is a number which represents the target for the corresponding output equation
Evaluate the problem by running "evaluate". This will return a list of tuples. The first item in the tuple is the system while the second is the net error. The list is sorted from best system to worst system based on the net error.
