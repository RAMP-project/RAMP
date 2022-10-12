"""
RAMP: An open-source bottom-up stochastic model for generating multi-energy load profiles

RAMP is a bottom-up stochastic model for the generation of high-resolution multi-energy profiles, 
conceived for application in contexts where only rough information about users' behaviour are obtainable. 
Those may range from remote villages to whole countries.


Package dependencies:
    - numpy
    - matplotlib
    - math
    - random
"""


from ramp._version import __version__
from ramp.core.core import UseCase
from ramp.core.core import User
from ramp.core.core import Appliance

__authors__ = "Listed in AUTHORS"
__copyright__ = ".."


