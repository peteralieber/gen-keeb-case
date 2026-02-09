// Generated keyboard case - Separate halves
// Layout: Custom (44 keys total)
// Switch type: Cherry MX
// Split keyboard: separate halves

// Parameters
left_case_width = 107.80;
left_case_height = 111.61;
right_case_width = 107.80;
right_case_height = 111.61;
case_depth = 18.00;
wall_thickness = 3.00;
base_height = 10.00;
switch_cutout_size = 14.00;
separation = 50;  // Distance between halves for visualization

module left_half() {
    difference() {
        // Outer shell
        cube([left_case_width, left_case_height, case_depth]);

        // Inner cavity
        translate([wall_thickness, wall_thickness, base_height])
            cube([left_case_width - 2*wall_thickness, 
                  left_case_height - 2*wall_thickness, 
                  case_depth - base_height + 1]);

        // Switch cutouts
        translate([wall_thickness + 5 - 0.00, wall_thickness + 5 - 0.00, -1])
            left_switch_plate();
    }
}

module right_half() {
    difference() {
        // Outer shell
        cube([right_case_width, right_case_height, case_depth]);

        // Inner cavity
        translate([wall_thickness, wall_thickness, base_height])
            cube([right_case_width - 2*wall_thickness, 
                  right_case_height - 2*wall_thickness, 
                  case_depth - base_height + 1]);

        // Switch cutouts
        translate([wall_thickness + 5 - 0.00, wall_thickness + 5 - 0.00, -1])
            right_switch_plate();
    }
}

module left_switch_plate() {
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
    translate([0.00, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([28.58, 80.01, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([47.62, 80.01, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
}

module right_switch_plate() {
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
    translate([0.00, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([28.58, 80.01, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([47.62, 80.01, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
}

// Generate both halves
left_half();
translate([left_case_width + separation, 0, 0])
    right_half();