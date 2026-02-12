"""
OpenSCAD code generator for keyboard cases.
"""

from gen_keeb_case.switch_types import SWITCH_TYPES


class KeyboardLayout:
    """Represents a keyboard layout with switch positions."""
    
    def __init__(self, rows=None, cols=None, switch_type_name="cherry_mx", custom_keys=None,
                 split=False, split_distance=None, separate_halves=False):
        """
        Initialize a keyboard layout.
        
        Args:
            rows: Number of rows (for grid layouts)
            cols: Number of columns (for grid layouts)
            switch_type_name: Type of mechanical switch to use
            custom_keys: List of custom key positions, each as dict with:
                        {'x': float, 'y': float, 'rotation': float (optional, degrees),
                         'half': 'left'/'right'/'both' (optional, for split keyboards),
                         'mirror': bool (optional, for 'both' half - mirror vs copy)}
            split: If True, keyboard is split into two halves
            split_distance: Distance between split halves (mm). If None, calculated from layout.
            separate_halves: If True, generate two separate case halves instead of one unified case
        """
        self.rows = rows
        self.cols = cols
        self.switch_type = SWITCH_TYPES.get(switch_type_name, SWITCH_TYPES["cherry_mx"])
        self.key_spacing = 19.05  # Standard key spacing in mm (0.75 inches)
        self.split = split
        self.split_distance = split_distance
        self.separate_halves = separate_halves
        
        # Generate base keys from grid layout
        grid_keys = []
        if rows is not None and cols is not None:
            for row in range(rows):
                for col in range(cols):
                    grid_keys.append({
                        'x': col * self.key_spacing,
                        'y': row * self.key_spacing,
                        'rotation': 0
                    })
        
        # Combine grid and custom keys
        if custom_keys is not None:
            self.is_custom = True
            # Expand custom keys that have 'both' half into left and right
            expanded_keys = []
            for key in custom_keys:
                expanded_keys.extend(self._expand_key(key))
            
            # Merge grid and custom keys
            all_keys = grid_keys + expanded_keys
        else:
            self.is_custom = len(grid_keys) == 0
            all_keys = grid_keys
        
        # Validate no overlaps
        self._validate_no_overlaps(all_keys)
        
        self.custom_keys = all_keys
    
    def _expand_key(self, key):
        """Expand a key with 'both' half into left and right keys."""
        half = key.get('half', None)
        
        if half == 'both':
            # Need to create both left and right versions
            mirror = key.get('mirror', False)
            
            # Calculate the center line for mirroring
            if self.split_distance is not None:
                # If split distance is set, use it to calculate center
                center_x = self._get_split_center_x()
            else:
                # Otherwise, mirror around x=0
                center_x = 0
            
            left_key = {
                'x': key['x'],
                'y': key['y'],
                'rotation': key.get('rotation', 0),
                'half': 'left'
            }
            
            if mirror:
                # Mirror the position across the center line
                right_key = {
                    'x': 2 * center_x - key['x'],
                    'y': key['y'],
                    'rotation': -key.get('rotation', 0),  # Mirror rotation too
                    'half': 'right'
                }
            else:
                # Copy the same position relative to each half
                right_key = {
                    'x': key['x'],
                    'y': key['y'],
                    'rotation': key.get('rotation', 0),
                    'half': 'right'
                }
            
            return [left_key, right_key]
        else:
            # Single key, just return as-is
            return [key]
    
    def _get_split_center_x(self):
        """Calculate the center x coordinate for split keyboards."""
        if not self.split or self.split_distance is None:
            return 0
        
        # For now, assume split in the middle
        # This will be refined based on actual layout
        if self.cols is not None:
            return (self.cols * self.key_spacing) / 2 + self.split_distance / 2
        return 0
    
    def _validate_no_overlaps(self, keys):
        """Validate that no keys overlap. Raises ValueError if overlaps detected."""
        import math
        
        # Check each pair of keys
        for i, key1 in enumerate(keys):
            for j, key2 in enumerate(keys):
                if i >= j:
                    continue
                
                # Skip checking if keys are on different halves in a split keyboard
                if self.split:
                    half1 = key1.get('half')
                    half2 = key2.get('half')
                    # If both have half specified and they're different, skip overlap check
                    if half1 and half2 and half1 != half2:
                        continue
                
                # Calculate distance between key centers
                dx = key1['x'] - key2['x']
                dy = key1['y'] - key2['y']
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Keys overlap if centers are closer than the switch size
                # Add small tolerance for floating point comparison
                min_distance = self.switch_type.width * 0.9  # 90% of switch width
                
                if distance < min_distance:
                    raise ValueError(
                        f"Key overlap detected: keys at ({key1['x']:.2f}, {key1['y']:.2f}) "
                        f"and ({key2['x']:.2f}, {key2['y']:.2f}) are too close "
                        f"(distance: {distance:.2f}mm, minimum: {min_distance:.2f}mm)"
                    )
        
    def get_dimensions(self):
        """Calculate overall keyboard dimensions."""
        if not self.custom_keys:
            return 0, 0
        
        if self.separate_halves:
            # Return dimensions for a single half (will generate two separate cases)
            left_keys = [k for k in self.custom_keys if k.get('half') != 'right']
            right_keys = [k for k in self.custom_keys if k.get('half') != 'left']
            
            # Return dimensions for the larger half
            left_dims = self._calculate_bounding_box(left_keys) if left_keys else (0, 0)
            right_dims = self._calculate_bounding_box(right_keys) if right_keys else (0, 0)
            
            return max(left_dims[0], right_dims[0]), max(left_dims[1], right_dims[1])
        else:
            # Return dimensions for unified case (or non-split keyboard)
            return self._calculate_bounding_box(self.custom_keys)
    
    def _calculate_bounding_box(self, keys):
        """Calculate bounding box dimensions for given keys."""
        if not keys:
            return 0, 0
            
        # Calculate bounding box for all keys
        min_x = min(key['x'] for key in keys)
        max_x = max(key['x'] for key in keys)
        min_y = min(key['y'] for key in keys)
        max_y = max(key['y'] for key in keys)
        
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
        if self.layout.separate_halves and self.layout.split:
            # Generate two separate cases
            return self._generate_separate_halves_scad()
        else:
            # Generate single unified case
            return self._generate_unified_scad()
    
    def _generate_unified_scad(self):
        """Generate OpenSCAD code for a unified case."""
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
        if self.layout.split:
            scad_code.append(f"// Split keyboard: unified case")
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
        
        # Switch plate module
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
    
    def _generate_separate_halves_scad(self):
        """Generate OpenSCAD code for separate left and right halves."""
        left_keys = [k for k in self.layout.custom_keys if k.get('half') != 'right']
        right_keys = [k for k in self.layout.custom_keys if k.get('half') != 'left']
        
        # Calculate dimensions for each half
        left_width, left_height = self.layout._calculate_bounding_box(left_keys) if left_keys else (0, 0)
        right_width, right_height = self.layout._calculate_bounding_box(right_keys) if right_keys else (0, 0)
        
        # Add margins for walls
        left_case_width = left_width + 2 * self.wall_thickness + 10
        left_case_height = left_height + 2 * self.wall_thickness + 10
        right_case_width = right_width + 2 * self.wall_thickness + 10
        right_case_height = right_height + 2 * self.wall_thickness + 10
        case_depth = self.base_height + self.top_clearance
        
        scad_code = []
        scad_code.append("// Generated keyboard case - Separate halves")
        scad_code.append(f"// Layout: Custom ({len(self.layout.custom_keys)} keys total)")
        scad_code.append(f"// Switch type: {self.layout.switch_type.name}")
        scad_code.append(f"// Split keyboard: separate halves")
        scad_code.append("")
        
        # Parameters
        scad_code.append("// Parameters")
        scad_code.append(f"left_case_width = {left_case_width:.2f};")
        scad_code.append(f"left_case_height = {left_case_height:.2f};")
        scad_code.append(f"right_case_width = {right_case_width:.2f};")
        scad_code.append(f"right_case_height = {right_case_height:.2f};")
        scad_code.append(f"case_depth = {case_depth:.2f};")
        scad_code.append(f"wall_thickness = {self.wall_thickness:.2f};")
        scad_code.append(f"base_height = {self.base_height:.2f};")
        scad_code.append(f"switch_cutout_size = {self.layout.switch_type.plate_cutout_size:.2f};")
        scad_code.append(f"separation = 50;  // Distance between halves for visualization")
        scad_code.append("")
        
        # Left half module
        scad_code.append("module left_half() {")
        scad_code.append("    difference() {")
        scad_code.append("        // Outer shell")
        scad_code.append("        cube([left_case_width, left_case_height, case_depth]);")
        scad_code.append("")
        scad_code.append("        // Inner cavity")
        scad_code.append("        translate([wall_thickness, wall_thickness, base_height])")
        scad_code.append("            cube([left_case_width - 2*wall_thickness, ")
        scad_code.append("                  left_case_height - 2*wall_thickness, ")
        scad_code.append("                  case_depth - base_height + 1]);")
        scad_code.append("")
        scad_code.append("        // Switch cutouts")
        if left_keys:
            left_offset_x = min(key['x'] for key in left_keys)
            left_offset_y = min(key['y'] for key in left_keys)
            scad_code.append(f"        translate([wall_thickness + 5 - {left_offset_x:.2f}, wall_thickness + 5 - {left_offset_y:.2f}, -1])")
            scad_code.append("            left_switch_plate();")
        scad_code.append("    }")
        scad_code.append("}")
        scad_code.append("")
        
        # Right half module
        scad_code.append("module right_half() {")
        scad_code.append("    difference() {")
        scad_code.append("        // Outer shell")
        scad_code.append("        cube([right_case_width, right_case_height, case_depth]);")
        scad_code.append("")
        scad_code.append("        // Inner cavity")
        scad_code.append("        translate([wall_thickness, wall_thickness, base_height])")
        scad_code.append("            cube([right_case_width - 2*wall_thickness, ")
        scad_code.append("                  right_case_height - 2*wall_thickness, ")
        scad_code.append("                  case_depth - base_height + 1]);")
        scad_code.append("")
        scad_code.append("        // Switch cutouts")
        if right_keys:
            right_offset_x = min(key['x'] for key in right_keys)
            right_offset_y = min(key['y'] for key in right_keys)
            scad_code.append(f"        translate([wall_thickness + 5 - {right_offset_x:.2f}, wall_thickness + 5 - {right_offset_y:.2f}, -1])")
            scad_code.append("            right_switch_plate();")
        scad_code.append("    }")
        scad_code.append("}")
        scad_code.append("")
        
        # Left switch plate module
        scad_code.append("module left_switch_plate() {")
        for key in left_keys:
            x = key['x']
            y = key['y']
            rotation = key.get('rotation', 0)
            
            if rotation != 0:
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
        
        # Right switch plate module
        scad_code.append("module right_switch_plate() {")
        for key in right_keys:
            x = key['x']
            y = key['y']
            rotation = key.get('rotation', 0)
            
            if rotation != 0:
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
        
        # Main call - show both halves side by side
        scad_code.append("// Generate both halves")
        scad_code.append("left_half();")
        scad_code.append("translate([left_case_width + separation, 0, 0])")
        scad_code.append("    right_half();")
        
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
        if self.layout.rows and self.layout.cols:
            svg_lines.append(f'  <title>Keyboard Case Top View - {self.layout.rows}x{self.layout.cols}</title>')
        else:
            svg_lines.append(f'  <title>Keyboard Case Top View - Custom Layout</title>')
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
