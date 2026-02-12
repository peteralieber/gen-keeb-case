// Generated keyboard case
// Layout: 5x15
// Switch type: Cherry MX
// Optimization: surface

// Parameters
case_width = 298.30;
case_height = 107.80;
case_depth = 18.00;
wall_thickness = 3.00;
base_height = 10.00;
switch_cutout_size = 14.00;
key_spacing = 19.05;

module keyboard_case() {
    difference() {
        // Outer shell
        translate([0, 0, 0])
            cube([case_width, case_height, case_depth]);

        // Inner cavity
        translate([wall_thickness, wall_thickness, base_height])
            cube([case_width - 2*wall_thickness, 
                  case_height - 2*wall_thickness, 
                  case_depth - base_height + 1]);

        // Switch cutouts
        translate([wall_thickness + 5 - 0.00, wall_thickness + 5 - 0.00, -1])
            switch_plate();
    }
}

module switch_plate() {
    // Switch cutouts using height map surface
    // Height map file: switch_plate_heightmap.dat
    scale([1, 1, base_height + 2])
        surface(file = "switch_plate_heightmap.dat", center = false, invert = true);
}

// Generate the case
keyboard_case();