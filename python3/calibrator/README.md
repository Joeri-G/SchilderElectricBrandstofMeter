# Function Finder

## What it does
The script `Function_Finder.py` finds a quadratic equation ( y = ax<sup>2</sup> + bx + c ) that goes through (or near) the points provided
The points are notated with:
* `(x,y)`
* `(x;y)`
* `( x ; y )`
* `( x , y )`

 `.` and  `;` are interchangeable, as are `whitespace` / ` `, `\t` and \<empty> / \<none>.

## Usage
Dependencies:
* python3
  * numpy
  * matplotlib.plypot
  * decimal

`$ ./Function_Finder`

Flag | Function | Arguments
-----|----------|----------
-p   | Add points as argument instead of writing them during run-time | [\<point>, \<point>, ...]
--no-graph | Don't ask the user to show the graph and end the program
--show-graph | Don't ask the user to show the graph and show the graph as soon as the function is found
