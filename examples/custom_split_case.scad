// Generated keyboard case
// Layout: Custom (26 keys)
// Switch type: Kailh Choc

// Parameters
case_width = 202.45;
case_height = 97.67;
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
    translate([0.00, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([0.00, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([28.58, 66.67, 0])
        rotate([0, 0, -15.00])
            translate([-6.90, -6.90, 0])
                cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([161.93, 66.67, 0])
        rotate([0, 0, 15.00])
            translate([-6.90, -6.90, 0])
                cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
}

// Generate the case
keyboard_case();