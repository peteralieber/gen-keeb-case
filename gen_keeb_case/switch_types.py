"""
Switch type definitions for mechanical keyboard switches.
"""

class SwitchType:
    """Base class for mechanical keyboard switch types."""
    
    def __init__(self, name, width, length, plate_cutout_size, travel_distance):
        self.name = name
        self.width = width  # mm
        self.length = length  # mm
        self.plate_cutout_size = plate_cutout_size  # mm
        self.travel_distance = travel_distance  # mm


# Common switch types
CHERRY_MX = SwitchType(
    name="Cherry MX",
    width=15.6,
    length=15.6,
    plate_cutout_size=14.0,
    travel_distance=4.0
)

CHERRY_MX_LOW_PROFILE = SwitchType(
    name="Cherry MX Low Profile",
    width=15.6,
    length=15.6,
    plate_cutout_size=14.0,
    travel_distance=3.2
)

KAILH_CHOC = SwitchType(
    name="Kailh Choc",
    width=15.0,
    length=15.0,
    plate_cutout_size=13.8,
    travel_distance=3.0
)

# Dictionary for easy lookup
SWITCH_TYPES = {
    "cherry_mx": CHERRY_MX,
    "cherry_mx_lp": CHERRY_MX_LOW_PROFILE,
    "kailh_choc": KAILH_CHOC,
}
