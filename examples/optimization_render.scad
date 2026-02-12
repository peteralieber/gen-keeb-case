// Generated keyboard case
// Layout: 5x15
// Switch type: Cherry MX
// Optimization: render

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
            render() switch_plate();
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
    translate([190.50, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([209.55, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([228.60, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([247.65, 0.00, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([266.70, 0.00, 0])
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
    translate([190.50, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([209.55, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([228.60, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([247.65, 19.05, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([266.70, 19.05, 0])
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
    translate([190.50, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([209.55, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([228.60, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([247.65, 38.10, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([266.70, 38.10, 0])
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
    translate([95.25, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([190.50, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([209.55, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([228.60, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([247.65, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([266.70, 57.15, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([0.00, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([19.05, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([38.10, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([57.15, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([76.20, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([95.25, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([114.30, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([133.35, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([152.40, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([171.45, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([190.50, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([209.55, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([228.60, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([247.65, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
    translate([266.70, 76.20, 0])
        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);
}

// Generate the case
keyboard_case();