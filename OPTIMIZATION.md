# Optimization Methods

This document explains the performance optimization options available for SCAD generation.

## Overview

When generating keyboard cases with many keys (e.g., 60+ keys), OpenSCAD's difference() operations can become slow. This implementation supports two optimization methods that can significantly improve render performance.

## Available Methods

### 1. None (Default)
```bash
python3 generate_case.py --optimization none
```

No optimization applied. This is the default behavior and maintains backward compatibility.

**Generated SCAD:**
```openscad
difference() {
    // Outer shell
    cube([...]);
    
    // Switch cutouts
    switch_plate();  // Individual cubes for each key
}
```

### 2. Render
```bash
python3 generate_case.py --optimization render
```

Wraps the switch plate with `render()` to pre-compute the geometry before the difference operation. This typically provides the best performance improvement.

**Generated SCAD:**
```openscad
difference() {
    // Outer shell
    cube([...]);
    
    // Switch cutouts
    render() switch_plate();  // Pre-computed geometry
}
```

### 3. Surface
```bash
python3 generate_case.py --optimization surface
```

Wraps the switch plate with `surface()`. **Note**: This is experimental and may not work as expected, as OpenSCAD's `surface()` function is primarily designed for importing height map data, not for CSG optimization. It is provided for testing purposes to match the original request.

**Generated SCAD:**
```openscad
difference() {
    // Outer shell
    cube([...]);
    
    // Switch cutouts
    surface() switch_plate();  // Experimental, may not work properly
}
```

## Performance Comparison

To compare performance:

1. Generate examples with all three methods:
   ```bash
   python3 examples_optimization.py
   ```

2. Open each generated file in OpenSCAD:
   - `examples/optimization_none.scad`
   - `examples/optimization_render.scad`
   - `examples/optimization_surface.scad`

3. Press F6 to render each one and note the render time

Expected results with a 60-key keyboard:
- **none**: Baseline (slowest)
- **render**: ~2-5x faster than baseline (recommended)
- **surface**: Likely will not work correctly (experimental)

## Programmatic Usage

```python
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

# Create your layout
layout = KeyboardLayout(rows=5, cols=15, switch_type_name="cherry_mx")

# Generate with optimization
generator = CaseGenerator(
    layout=layout,
    optimization_method='render'  # or 'none', 'surface'
)

generator.save("keyboard_case.scad")
```

## Recommendations

1. **For small keyboards (<20 keys)**: Use `none` - optimization overhead not worth it
2. **For medium keyboards (20-60 keys)**: Use `render` - noticeable performance improvement
3. **For large keyboards (60+ keys)**: Use `render` - significant performance improvement
4. **For experimentation**: Try all three and compare

## Technical Details

- `render()`: Forces OpenSCAD to compute the geometry at that point in the tree, creating a single mesh. This is faster for difference operations because OpenSCAD only needs to compute the difference once with a pre-merged mesh instead of computing it separately for each individual cube.

- `surface()`: **Note - This is experimental and likely won't work properly.** OpenSCAD's `surface()` function is designed to import height map data from external files (like PNG or DAT files), not to optimize CSG operations. It's included here as per the original request, but `render()` is the recommended optimization method.

## Limitations

- **Surface optimization is experimental**: OpenSCAD's `surface()` function is primarily for importing height map data from files, not for CSG optimization. This option is provided for experimentation as requested, but likely will not produce correct results.
- Render optimization adds a small overhead to the OpenSCAD compilation phase
- The optimization benefit scales with the number of keys - more keys = more benefit
