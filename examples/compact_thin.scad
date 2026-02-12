// Generated keyboard case
// Layout: 3x10
// Switch type: Cherry MX

// Parameters
case_width = 201.05;
case_height = 67.70;
case_depth = 16.00;
wall_thickness = 2.00;
base_height = 8.00;
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
    translate([0.00, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([95.25, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([0.00, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([95.25, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([0.00, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([95.25, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
}

// Generate the case
keyboard_case();