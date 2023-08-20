# Genetic Algorithm for Function Maximization

This is an implementation of a genetic algorithm that maximizes a family of functions. The code in Python is in file `program.py` and the full analysis of the task is in `report.pdf`.

## Implementation

The functions maximized by our algorithm are of the form $F(x)=x^TAx+b^Tx+c$, and our binary representation is signed binary, as it behaves better when it comes to our algorithm. There are 4 main functions used - fitvalues, roullete_wheel_selection, crossover and mutation - all discussed further in the report.
