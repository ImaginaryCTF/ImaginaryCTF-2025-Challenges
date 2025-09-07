# twisted

**Category**: Misc
**Difficulty**: Easy
**Author**: c-bass

# Description

I lost my flag! Can you help me recover it?

# Distribution

- chall.py

# Solution

Looking at the output data, you can recognize this involves 3D transformations applied to ASCII values of the flag - in particular, rotations (via quaternions), scaling, and translation with added Gaussian noise. Use the Umeyama algorithm to estimate the transformation parameters utilizing the flag format, creating correspondence points between known ASCII values and the transformed coordinates. Iteratively refine the parameters to account for noise, then decode the transformed points back to ascii to recover the original flag.
