# hitomezashi-explorer
A wxPython tool to visualize hitomezashi embroidery patterns

## What does this tool do?

Hitomezashi is a form of embroidery where equally spaced vertical and horizontal running stitches are used to create patterns by their intersections on a grid. The variation in patterns arises from the offset of each running stitches, whether it starts with a section on the top or bottom of the fabric. Each of the two directions of stitches can thus be represented with a bitstring (0 for starting above the work, 1 for starting below); this visualization tool is meant to take pairs of bitstrings as input and visualize them.

## Current features

* Selectable presets for the bitcodes or custom entry
  - The Fibonacci-Pell snowflake
  - The Thue-Morse sequence
  - The Kolakoski sequence
  - A random bitstring
* Customizable colors/styles for gridlines and stitches
* Bounded-region coloring
  - Two-coloring of the regions bounded by stitches
  - Coloration of closed loops by the depth of enclaves

## TODO

* Add an export to PNG, SVG, and TikZ source code feature
* Fix the preset dialog (which goes weird from the second instantiation on)
* Make enclave-depth calculation more efficient

## Warnings

If you ask this tool to do impossible or stupid things, it will try its best to do them with no particular regard for the scope of the job. On a sensible OS it probably can't do much damage, but it will use whatever CPU, memory, and other resources it thinks it needs for the task. So, for instance, if you ask for an order-10 Fibonacci-Pell snowflake with enclave-coloration, it will (a) thrash violently for days on end calculating the enclave coloration on a 4756-by-4756 grid, and (b) try to draw it, which on any reasonable screen resolution will be indistinguishable from a black square.
