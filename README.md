# rimworld_stuff

This is a dump of the code I've been using to edit the rimworld wiki.

Useful things:
* curve.expected_from_discrete_curve(x, y) gives the expected number of offspring from a given liter curve pdf, accounting for the fact that you only get whole numbers of offspring
* curve.post_process_curve(pre, x, y) finds the value of pre after being modified by the curve defined by x and y
* infobox_checker.py takes an input infobox from input.txt and prints what it should be based on the def xmls, listing the changes. Animal only atm.
