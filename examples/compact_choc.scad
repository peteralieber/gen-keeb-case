// Generated keyboard case
// Layout: 3x10
// Switch type: Kailh Choc

// Parameters
case_width = 202.45;
case_height = 69.10;
case_depth = 18.00;
wall_thickness = 3.00;
base_height = 10.00;
switch_cutout_size = 13.80;
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
        translate([wall_thickness + 5, wall_thickness + 5, -1])
            switch_plate();
    }
}

module switch_plate() {
    for (row = [0:2]) {
        for (col = [0:9]) {
            translate([col * key_spacing, row * key_spacing, 0])
                cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
        }
    }
}

// Generate the case
keyboard_case();