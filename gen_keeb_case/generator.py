"""
OpenSCAD code generator for keyboard cases.
"""

from gen_keeb_case.switch_types import SWITCH_TYPES


class KeyboardLayout:
    """Represents a keyboard layout with switch positions."""
    
    def __init__(self, rows=None, cols=None, switch_type_name="cherry_mx", custom_keys=None):
        """
        Initialize a keyboard layout.
        
        Args:
            rows: Number of rows (for grid layouts)
            cols: Number of columns (for grid layouts)
            switch_type_name: Type of mechanical switch to use
            custom_keys: List of custom key positions, each as dict with:
                        {'x': float, 'y': float, 'rotation': float (optional, degrees)}
                        If provided, rows and cols are ignored.
        """
        self.rows = rows
        self.cols = cols
        self.switch_type = SWITCH_TYPES.get(switch_type_name, SWITCH_TYPES["cherry_mx"])
        self.key_spacing = 19.05  # Standard key spacing in mm (0.75 inches)
        
        # Support custom key positions for non-grid layouts
        if custom_keys is not None:
            self.custom_keys = custom_keys
            self.is_custom = True
        else:
            self.is_custom = False
            # Generate grid layout if rows/cols provided
            if rows is not None and cols is not None:
                self.custom_keys = []
                for row in range(rows):
                    for col in range(cols):
                        self.custom_keys.append({
                            'x': col * self.key_spacing,
                            'y': row * self.key_spacing,
                            'rotation': 0
                        })
            else:
                self.custom_keys = []
        
    def get_dimensions(self):
        """Calculate overall keyboard dimensions."""
        if not self.custom_keys:
            return 0, 0
            
        # Calculate bounding box for all keys
        min_x = min(key['x'] for key in self.custom_keys)
        max_x = max(key['x'] for key in self.custom_keys)
        min_y = min(key['y'] for key in self.custom_keys)
        max_y = max(key['y'] for key in self.custom_keys)
        
        width = max_x - min_x + self.switch_type.width
        height = max_y - min_y + self.switch_type.length
        return width, height
    
    def get_offset(self):
        """Get the minimum x,y offset for positioning keys."""
        if not self.custom_keys:
            return 0, 0
        min_x = min(key['x'] for key in self.custom_keys)
        min_y = min(key['y'] for key in self.custom_keys)
        return min_x, min_y


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
        if self.layout.rows and self.layout.cols:
            scad_code.append(f"// Layout: {self.layout.rows}x{self.layout.cols}")
        else:
            scad_code.append(f"// Layout: Custom ({len(self.layout.custom_keys)} keys)")
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
        offset_x, offset_y = self.layout.get_offset()
        scad_code.append(f"        translate([wall_thickness + 5 - {offset_x:.2f}, wall_thickness + 5 - {offset_y:.2f}, -1])")
        scad_code.append("            switch_plate();")
        scad_code.append("    }")
        scad_code.append("}")
        scad_code.append("")
        
        # Switch plate module - now supports custom positions and rotation
        scad_code.append("module switch_plate() {")
        for key in self.layout.custom_keys:
            x = key['x']
            y = key['y']
            rotation = key.get('rotation', 0)
            
            if rotation != 0:
                # For rotated keys, rotate around the center of the switch
                center_offset = self.layout.switch_type.plate_cutout_size / 2
                scad_code.append(f"    translate([{x:.2f}, {y:.2f}, 0])")
                scad_code.append(f"        rotate([0, 0, {rotation:.2f}])")
                scad_code.append(f"            translate([{-center_offset:.2f}, {-center_offset:.2f}, 0])")
                scad_code.append(f"                cube([switch_cutout_size, switch_cutout_size, base_height + 2]);")
            else:
                scad_code.append(f"    translate([{x:.2f}, {y:.2f}, 0])")
                scad_code.append(f"        cube([switch_cutout_size, switch_cutout_size, base_height + 2]);")
        
        scad_code.append("}")
        scad_code.append("")
        
        # Main call
        scad_code.append("// Generate the case")
        scad_code.append("keyboard_case();")
        
        return "\n".join(scad_code)
    
    def generate_svg(self):
        """Generate an SVG representation of the top-down view of the case."""
        width, height = self.layout.get_dimensions()
        
        # Add margins for walls
        case_width = width + 2 * self.wall_thickness + 10
        case_height = height + 2 * self.wall_thickness + 10
        
        # SVG setup with padding
        padding = 20
        svg_width = case_width + 2 * padding
        svg_height = case_height + 2 * padding
        
        svg_lines = []
        svg_lines.append(f'<?xml version="1.0" encoding="UTF-8"?>')
        svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width:.2f}mm" height="{svg_height:.2f}mm" viewBox="0 0 {svg_width:.2f} {svg_height:.2f}">')
        svg_lines.append(f'  <title>Keyboard Case Top View - {self.layout.rows}x{self.layout.cols}</title>')
        svg_lines.append(f'  <desc>Generated keyboard case layout for {self.layout.switch_type.name} switches</desc>')
        svg_lines.append('')
        
        # Define styles
        svg_lines.append('  <defs>')
        svg_lines.append('    <style>')
        svg_lines.append('      .case-outer { fill: #e0e0e0; stroke: #333; stroke-width: 1; }')
        svg_lines.append('      .case-inner { fill: #f5f5f5; stroke: #666; stroke-width: 0.5; }')
        svg_lines.append('      .switch-cutout { fill: #fff; stroke: #000; stroke-width: 0.5; }')
        svg_lines.append('      .text { font-family: Arial, sans-serif; font-size: 8px; fill: #333; }')
        svg_lines.append('    </style>')
        svg_lines.append('  </defs>')
        svg_lines.append('')
        
        # Outer case
        svg_lines.append(f'  <!-- Outer case -->')
        svg_lines.append(f'  <rect class="case-outer" x="{padding}" y="{padding}" width="{case_width:.2f}" height="{case_height:.2f}" rx="2"/>')
        svg_lines.append('')
        
        # Inner cavity
        inner_x = padding + self.wall_thickness
        inner_y = padding + self.wall_thickness
        inner_width = case_width - 2 * self.wall_thickness
        inner_height = case_height - 2 * self.wall_thickness
        svg_lines.append(f'  <!-- Inner cavity -->')
        svg_lines.append(f'  <rect class="case-inner" x="{inner_x:.2f}" y="{inner_y:.2f}" width="{inner_width:.2f}" height="{inner_height:.2f}" rx="1"/>')
        svg_lines.append('')
        
        # Switch cutouts
        svg_lines.append(f'  <!-- Switch cutouts -->')
        offset_x_base = padding + self.wall_thickness + 5
        offset_y_base = padding + self.wall_thickness + 5
        offset_min_x, offset_min_y = self.layout.get_offset()
        cutout_size = self.layout.switch_type.plate_cutout_size
        
        for key in self.layout.custom_keys:
            x = offset_x_base + key['x'] - offset_min_x
            y = offset_y_base + key['y'] - offset_min_y
            rotation = key.get('rotation', 0)
            
            if rotation != 0:
                # For rotated keys, use SVG transform
                cx = x + cutout_size / 2
                cy = y + cutout_size / 2
                svg_lines.append(f'  <rect class="switch-cutout" x="{x:.2f}" y="{y:.2f}" width="{cutout_size:.2f}" height="{cutout_size:.2f}" transform="rotate({rotation:.2f} {cx:.2f} {cy:.2f})"/>')
            else:
                svg_lines.append(f'  <rect class="switch-cutout" x="{x:.2f}" y="{y:.2f}" width="{cutout_size:.2f}" height="{cutout_size:.2f}"/>')
        
        svg_lines.append('')
        
        # Add labels
        svg_lines.append(f'  <!-- Labels -->')
        svg_lines.append(f'  <text class="text" x="{padding + 5}" y="{padding + case_height + 15}">')
        if self.layout.rows and self.layout.cols:
            svg_lines.append(f'    Layout: {self.layout.rows}x{self.layout.cols} | Switch: {self.layout.switch_type.name} | Dimensions: {case_width:.1f}x{case_height:.1f}mm')
        else:
            svg_lines.append(f'    Layout: Custom ({len(self.layout.custom_keys)} keys) | Switch: {self.layout.switch_type.name} | Dimensions: {case_width:.1f}x{case_height:.1f}mm')
        svg_lines.append(f'  </text>')
        
        svg_lines.append('</svg>')
        
        return "\n".join(svg_lines)
    
    def save(self, filename):
        """Save the generated OpenSCAD code to a file."""
        with open(filename, 'w') as f:
            f.write(self.generate_scad())
        print(f"Generated OpenSCAD file: {filename}")
    
    def save_svg(self, filename):
        """Save the generated SVG top-down view to a file."""
        with open(filename, 'w') as f:
            f.write(self.generate_svg())
        print(f"Generated SVG file: {filename}")
