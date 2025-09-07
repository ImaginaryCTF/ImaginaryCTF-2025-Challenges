# clcg
**Category:** Crypto
**Difficulty:** Medium
**Author:** wjaaaaaaat

## Description
Like a bundle of sticks, a bundle of LCGs is stronger together... right?

## Distribution
clcg.zip

## Solution
Note that if `x1 = a*x0 + c` then `x1 + c/(a-1) = a*x0 + ac/(a-1) = a(x0 + c/(a-1))` so `xi = C*a**i - c/(a-1)`. If we add up 8 LCGs, it will be of the form `sum(Cj*aj**i for j) - D`, and taking the partial differences gets rid of `D`. We now note that this satisfies the linear recurrence whose characteristic polynomial is `prod(x - aj for j)`. We use this recurrence to build a lattice that will be `0` mod `p` when multiplied by the vector of true differences between state sums.
