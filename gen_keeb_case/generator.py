"""
OpenSCAD code generator for keyboard cases.
"""

from gen_keeb_case.switch_types import SWITCH_TYPES


class KeyboardLayout:
    """Represents a keyboard layout with switch positions."""
    
    def __init__(self, rows, cols, switch_type_name="cherry_mx"):
        self.rows = rows
        self.cols = cols
        self.switch_type = SWITCH_TYPES.get(switch_type_name, SWITCH_TYPES["cherry_mx"])
        self.key_spacing = 19.05  # Standard key spacing in mm (0.75 inches)
        
    def get_dimensions(self):
        """Calculate overall keyboard dimensions."""
        width = (self.cols - 1) * self.key_spacing + self.switch_type.width
        height = (self.rows - 1) * self.key_spacing + self.switch_type.length
        return width, height


class CaseGenerator:
    """Generate OpenSCAD code for keyboard cases."""
    
    def __init__(self, layout, wall_thickness=3.0, base_height=10.0, top_clearance=8.0):
        self.layout = layout
        self.wall_thickness = wall_thickness
        self.base_height = base_height
        self.top_clearance = top_clearance
        
    def generate_scad(self):
        """Generate the complete OpenSCAD code."""
        width, height = self.layout.get_dimensions()
        
        # Add margins for walls
        case_width = width + 2 * self.wall_thickness + 10  # 5mm margin on each side
        case_height = height + 2 * self.wall_thickness + 10
        case_depth = self.base_height + self.top_clearance
        
        scad_code = []
        scad_code.append("// Generated keyboard case")
        scad_code.append(f"// Layout: {self.layout.rows}x{self.layout.cols}")
        scad_code.append(f"// Switch type: {self.layout.switch_type.name}")
        scad_code.append("")
        
        # Parameters
        scad_code.append("// Parameters")
        scad_code.append(f"case_width = {case_width:.2f};")
        scad_code.append(f"case_height = {case_height:.2f};")
        scad_code.append(f"case_depth = {case_depth:.2f};")
        scad_code.append(f"wall_thickness = {self.wall_thickness:.2f};")
        scad_code.append(f"base_height = {self.base_height:.2f};")
        scad_code.append(f"switch_cutout_size = {self.layout.switch_type.plate_cutout_size:.2f};")
        scad_code.append(f"key_spacing = {self.layout.key_spacing:.2f};")
        scad_code.append("")
        
        # Main case module
        scad_code.append("module keyboard_case() {")
        scad_code.append("    difference() {")
        scad_code.append("        // Outer shell")
        scad_code.append("        translate([0, 0, 0])")
        scad_code.append("            cube([case_width, case_height, case_depth]);")
        scad_code.append("")
        scad_code.append("        // Inner cavity")
        scad_code.append("        translate([wall_thickness, wall_thickness, base_height])")
        scad_code.append("            cube([case_width - 2*wall_thickness, ")
        scad_code.append("                  case_height - 2*wall_thickness, ")
        scad_code.append("                  case_depth - base_height + 1]);")
        scad_code.append("")
        scad_code.append("        // Switch cutouts")
        scad_code.append(f"        translate([wall_thickness + 5, wall_thickness + 5, -1])")
        scad_code.append("            switch_plate();")
        scad_code.append("    }")
        scad_code.append("}")
        scad_code.append("")
        
        # Switch plate module
        scad_code.append("module switch_plate() {")
        scad_code.append(f"    for (row = [0:{self.layout.rows - 1}]) {{")
        scad_code.append(f"        for (col = [0:{self.layout.cols - 1}]) {{")
        scad_code.append("            translate([col * key_spacing, row * key_spacing, 0])")
        scad_code.append("                cube([switch_cutout_size, switch_cutout_size, base_height + 2]);")
        scad_code.append("        }")
        scad_code.append("    }")
        scad_code.append("}")
        scad_code.append("")
        
        # Main call
        scad_code.append("// Generate the case")
        scad_code.append("keyboard_case();")
        
        return "\n".join(scad_code)
    
    def save(self, filename):
        """Save the generated OpenSCAD code to a file."""
        with open(filename, 'w') as f:
            f.write(self.generate_scad())
        print(f"Generated OpenSCAD file: {filename}")
