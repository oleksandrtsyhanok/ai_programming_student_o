Certainly! A transportation problem typically involves determining the optimal way to transport goods from suppliers to consumers to minimize the total transportation cost. While traditional transportation problems are often linear, we can formulate a quadratic convex optimization problem that resembles a transportation problem with two unknowns.

### Problem: Quadratic Transportation Problem

Suppose we have two suppliers and two consumers. The goal is to determine the amount of goods to transport from each supplier to each consumer to minimize the total transportation cost, which includes a quadratic term to represent additional costs such as congestion or wear and tear.

#### Variables:
- \( x_{11} \): Amount of goods transported from Supplier 1 to Consumer 1.
- \( x_{12} \): Amount of goods transported from Supplier 1 to Consumer 2.
- \( x_{21} \): Amount of goods transported from Supplier 2 to Consumer 1.
- \( x_{22} \): Amount of goods transported from Supplier 2 to Consumer 2.

For simplicity, let's assume we only need to optimize \( x_{11} \) and \( x_{12} \) (the amounts from Supplier 1), and the amounts from Supplier 2 are fixed or can be derived from these variables.

#### Objective Function:
The objective is to minimize the total transportation cost, which includes a linear term for the base cost and a quadratic term for additional costs.

\[ \min \quad c_{11} x_{11} + c_{12} x_{12} + d_{11} x_{11}^2 + d_{12} x_{12}^2 \]

where \( c_{11} \) and \( c_{12} \) are the linear costs, and \( d_{11} \) and \( d_{12} \) are the quadratic cost coefficients.

#### Constraints:
1. The total amount transported from Supplier 1 should not exceed its supply.
2. The total amount received by each consumer should meet their demand.

Assume the following data:
- Supplier 1 has a supply of 100 units.
- Consumer 1 demands 60 units.
- Consumer 2 demands 40 units.
- Linear costs: \( c_{11} = 2 \), \( c_{12} = 3 \).
- Quadratic costs: \( d_{11} = 0.01 \), \( d_{12} = 0.02 \).

### Formulation:

\[ \min \quad 2x_{11} + 3x_{12} + 0.01x_{11}^2 + 0.02x_{12}^2 \]

subject to:

\[ x_{11} + x_{12} \leq 100 \]
\[ x_{11} \geq 60 \]
\[ x_{12} \geq 40 \]
\[ x_{11}, x_{12} \geq 0 \]

### Solving with OSQP:

Here's how you might set up and solve this problem using OSQP in Python:

```python
import numpy as np
import osqp

# Define the problem data
P = np.array([[0.02, 0.0],
              [0.0, 0.04]])
q = np.array([2.0, 3.0])
A = np.array([[1.0, 1.0],
              [1.0, 0.0],
              [0.0, 1.0]])
l = np.array([-np.inf, 60.0, 40.0])
u = np.array([100.0, np.inf, np.inf])

# Define the lower and upper bounds for the variables
lb = np.array([0.0, 0.0])
ub = np.array([np.inf, np.inf])

# Create an OSQP object
prob = osqp.OSQP()

# Setup workspace
prob.setup(P, q, A, l, u, lb, ub)

# Solve the problem
res = prob.solve()

# Print the results
print("Optimal values:", res.x)
```

This code sets up and solves the quadratic transportation problem using OSQP. The `P` matrix represents the quadratic cost coefficients, `q` represents the linear cost coefficients, `A` is the constraint matrix, and `l` and `u` are the lower and upper bounds for the constraints.

The solution will provide the optimal values of \( x_{11} \) and \( x_{12} \) that minimize the total transportation cost while satisfying the supply and demand constraints.