# significant
**Category**: Misc
**Difficulty**: Easy
**Author**: puzzler7

# Description
The signpost knows where it is at all times. It knows this because it knows where it isn't, by subtracting where it is, from where it isn't, or where it isn't, from where it is, whichever is greater. Consequently, the position where it is, is now the position that it wasn't, and it follows that the position where it was, is now the position that it isn't.

Please find the coordinates (lat, long) of this signpost to the nearest 3 decimals, separated by a comma with no space. Example flag: ictf{-12.345,6.789}

# Distribution
- significant.jpg

# Solution

Searching the text on the sign in quotes (e.g. "Assisi 6187mi") will bring up images of the sign with its header "Sister Cities of San Francisco" visible, which you can search to find the exact location. Alternatively, you can use a tool like https://www.atlist.com/radius-map-tool to draw circles of the appropriate radius and see that they intersect at San Francisco.
