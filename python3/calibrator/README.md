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

#### Universal:
`$ python3 Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]`

#### OSX / Linux:
`$ ./Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]`

#### Windows only:
`$ py Gauge_Calibrator.py [--no-graph || --draw-graph] [--percentage || --voltage] [-v int] [-p <points>]`

## Arguments:
Flag | Function | Argument Type
-----|----------|--------------
 --draw-graph | Draw graph (default = ask) | NULL
 --no-graph | Don't draw graph (default = ask) | NULL
 --percentage | The X coordinate represents a percentage | NULL
 --voltage | The X coordinate represents a voltage (Vin) | NULL
 -v \<voltage> | Voltage that represents a 100% load | INT \|\| FLOAT
 -p \<point, [point, point...]> | Supply one or more points as argument instead of typing them in at runtime<br> Whitespaces are ignored Period (.) is user for decimal notation | STRING (x,y) \|\| STRING (x;y)
