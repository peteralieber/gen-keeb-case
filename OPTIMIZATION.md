# Optimization Methods

This document explains the performance optimization options available for SCAD generation.

## Overview

When generating keyboard cases with many keys (e.g., 60+ keys), OpenSCAD's difference() operations can become slow. This implementation supports two optimization methods that can significantly improve render performance.

## Available Methods

### 1. Render (Default)
```bash
python3 generate_case.py --optimization render
# or simply (render is the default)
python3 generate_case.py
```

Wraps the switch plate with `render()` to pre-compute the geometry before the difference operation. This is the recommended default and typically provides the best performance improvement.

**Generated SCAD:**
```openscad
difference() {
    // Outer shell
    cube([...]);
    
    // Switch cutouts
    render() switch_plate();  // Pre-computed geometry
}

module switch_plate() {
    // Individual cubes for each key
    translate([...]) cube([...]);
    translate([...]) cube([...]);
    ...
}
```

### 2. Surface
```bash
python3 generate_case.py --optimization surface
```

Generates a height map file (.dat format) representing the switch plate cutouts, then uses OpenSCAD's `surface()` function to read it. This is an experimental method that creates an actual 2D raster of the switch cutouts.
**Generated SCAD:**
```openscad
difference() {
    // Outer shell
    cube([...]);
    
    // Switch cutouts
    switch_plate();
}

module switch_plate() {
    // Switch cutouts using height map surface
    // Height map file: switch_plate_heightmap.dat
    scale([1, 1, base_height + 2])
        surface(file = "switch_plate_heightmap.dat", center = false, invert = true);
}
```

**Generated Files:**
- `keyboard_case.scad` - The OpenSCAD file
- `switch_plate_heightmap.dat` - Text-based height map (0.0 = cutout, 1.0 = solid)

The height map is a 2D raster where each point represents 1mm². Values of 0.0 indicate areas where switch cutouts should be, and 1.0 indicates solid material.

## Performance Comparison

To compare performance:

1. Generate examples with both methods:
   ```bash
   python3 examples_optimization.py
   ```

2. Open each generated file in OpenSCAD:
   - `examples/optimization_render.scad`
   - `examples/optimization_surface.scad`

3. Press F6 to render each one and note the render time

Expected results with a 75-key keyboard:
- **render**: Fast, ~2-5x faster than unoptimized (recommended)
- **surface**: Performance varies, uses height map approach

## Programmatic Usage

```python
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

# Create your layout
layout = KeyboardLayout(rows=5, cols=15, switch_type_name="cherry_mx")

# Generate with default optimization (render)
generator = CaseGenerator(layout=layout)
generator.save("keyboard_case.scad")

# Or specify explicitly
generator = CaseGenerator(
    layout=layout,
    optimization_method='surface'  # or 'render'
)
generator.save("keyboard_case.scad")
# For surface method, this also generates switch_plate_heightmap.dat
```

## Recommendations

1. **Default (render)**: Recommended for all keyboard sizes - provides consistent performance improvement
2. **Surface method**: Experimental - generates height map files for an alternative approach
3. **For best performance**: Use `render` (the default)

## Technical Details

- `render()`: Forces OpenSCAD to compute the geometry at that point in the tree, creating a single mesh. This is faster for difference operations because OpenSCAD only needs to compute the difference once with a pre-merged mesh instead of computing it separately for each individual cube.

- `surface()`: Generates a text-based height map (.dat file) where each value represents whether that point should be solid (1.0) or a cutout (0.0). The height map has a resolution of 1 point per mm². OpenSCAD's `surface()` function then reads this file to create the geometry. This is a proper implementation of height map-based surface modeling.

## Limitations

- Height map resolution for surface method is 1mm per point, which may result in slightly imprecise edges for rotated keys
- Render optimization adds a small overhead to the OpenSCAD compilation phase, but this is more than compensated by faster rendering
- The optimization benefit scales with the number of keys - more keys = more benefit
- Surface method generates additional .dat files that must be kept alongside the .scad file
