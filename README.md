# gen-keeb-case

Generate OpenSCAD models of mechanical keyboard cases. The case is generated based on keyboard layout dimensions and switch types, which have standardized sizes.

## Proof of Concept

This POC demonstrates automatic generation of 3D printable keyboard cases using OpenSCAD. The generator creates cases based on:
- Number of rows and columns in the keyboard layout
- Switch type (Cherry MX, Kailh Choc, etc.) with known dimensions
- Customizable wall thickness, base height, and clearance

## Features

- 🔧 **Multiple switch types**: Cherry MX, Cherry MX Low Profile, Kailh Choc
- 📐 **Parametric design**: Easily adjust dimensions and layout
- 🎯 **OpenSCAD output**: Industry-standard CAD format for 3D printing
- 🚀 **Simple CLI**: Generate cases with a single command
- 🔲 **Grid layouts**: Define keyboards by rows and columns
- 🎨 **Custom key positions**: Place keys at any position with rotation
- ➕ **Grid + Custom combo**: Combine grid layouts with additional custom keys
- ✂️ **Split keyboards**: Support for split keyboard layouts
- 🔄 **Mirror/Copy modes**: Automatically mirror or copy keys across halves
- 🔍 **Overlap detection**: Automatic validation to prevent overlapping keys
- 📦 **Separate halves**: Generate individual cases for each half

## Installation

No external dependencies required! Uses Python 3 standard library only.

```bash
git clone https://github.com/peteralieber/gen-keeb-case.git
cd gen-keeb-case
```

## Quick Start

### Generate Example Cases

```bash
python3 examples.py
```

This creates three example cases in the `examples/` directory:
- `60_percent_keyboard.scad` - Standard 60% keyboard (5x15)
- `numpad.scad` - Numeric keypad (5x4)
- `compact_choc.scad` - Compact keyboard with Kailh Choc switches (3x10)

### Generate Advanced Feature Examples

```bash
python3 examples_new_features.py
```

This generates additional examples demonstrating new features:
- `grid_with_custom_keys` - Grid layout with additional custom thumb keys
- `split_keyboard_unified` - Split keyboard in a unified case
- `split_keyboard_copied_thumbs` - Split with copied thumb keys on both halves
- `split_keyboard_mirrored_thumbs` - Split with mirrored thumb keys
- `separate_halves_with_thumbs` - Two separate cases for left and right halves

### Generate Custom Case

```bash
python3 generate_case.py --rows 5 --cols 15 --switch-type cherry_mx --output my_keyboard.scad
```

## Advanced Usage

### Grid + Custom Keys

Combine a regular grid layout with custom positioned keys:

```python
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

# Create a 3x6 grid with additional custom thumb keys
custom_keys = [
    {'x': 28.575, 'y': 66.675, 'rotation': -10},  # Angled thumb key
    {'x': 47.625, 'y': 66.675, 'rotation': 0},     # Straight thumb key
]

layout = KeyboardLayout(
    rows=3,
    cols=6,
    switch_type_name="cherry_mx",
    custom_keys=custom_keys  # Additional keys beyond the grid
)

generator = CaseGenerator(layout=layout)
generator.save("my_keyboard.scad")
```

### Split Keyboards

Create split keyboard layouts with unified or separate cases:

```python
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

spacing = 19.05  # Standard key spacing

# Define left half keys
left_keys = []
for row in range(3):
    for col in range(6):
        left_keys.append({
            'x': col * spacing,
            'y': row * spacing,
            'half': 'left'
        })

# Define right half keys (offset to the right)
right_keys = []
for row in range(3):
    for col in range(6):
        right_keys.append({
            'x': (col + 8) * spacing,  # Offset for gap
            'y': row * spacing,
            'half': 'right'
        })

# Create unified split keyboard case
layout = KeyboardLayout(
    switch_type_name="cherry_mx",
    custom_keys=left_keys + right_keys,
    split=True,
    split_distance=spacing * 2
)

generator = CaseGenerator(layout=layout)
generator.save("split_keyboard.scad")
```

### Separate Halves

Generate two separate cases for a split keyboard:

```python
layout = KeyboardLayout(
    switch_type_name="cherry_mx",
    custom_keys=left_keys + right_keys,
    split=True,
    split_distance=spacing * 2,
    separate_halves=True  # Generate two separate cases
)

generator = CaseGenerator(layout=layout)
generator.save("split_keyboard_halves.scad")
```

### Mirror and Copy Modes

Apply custom keys to both halves with mirror or copy mode:

```python
# Define keys that appear on both halves
thumb_keys = [
    # Mirror mode: position and rotation are mirrored across center
    {'x': 19.05, 'y': 57.15, 'rotation': -15, 'half': 'both', 'mirror': True},
    
    # Copy mode: same position used on both halves
    {'x': 38.1, 'y': 57.15, 'rotation': 0, 'half': 'both', 'mirror': False},
]

layout = KeyboardLayout(
    switch_type_name="cherry_mx",
    custom_keys=left_keys + right_keys + thumb_keys,
    split=True
)
```

### Overlap Detection

The generator automatically validates that keys don't overlap:

```python
try:
    # These keys are too close and will raise an error
    overlapping_keys = [
        {'x': 0, 'y': 0},
        {'x': 10, 'y': 0},  # Too close! Need ~19mm spacing
    ]
    
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=overlapping_keys
    )
except ValueError as e:
    print(f"Error: {e}")
    # Output: Key overlap detected: keys at (0.00, 0.00) and (10.00, 0.00) 
    #         are too close (distance: 10.00mm, minimum: 14.04mm)
```

### Available Options

```
--rows              Number of rows (default: 5)
--cols              Number of columns (default: 15)
--switch-type       Switch type: cherry_mx, cherry_mx_lp, kailh_choc (default: cherry_mx)
--wall-thickness    Case wall thickness in mm (default: 3.0)
--base-height       Height of case base in mm (default: 10.0)
--top-clearance     Clearance above switches in mm (default: 8.0)
--output, -o        Output filename (default: keyboard_case.scad)
```

## Viewing and Rendering

1. Install [OpenSCAD](https://openscad.org/downloads.html)
2. Open the generated `.scad` file in OpenSCAD
3. Press F5 to preview or F6 to render
4. Export as STL for 3D printing

## Switch Types

| Switch Type | Dimensions | Cutout Size | Travel |
|-------------|------------|-------------|--------|
| Cherry MX | 15.6 x 15.6 mm | 14.0 mm | 4.0 mm |
| Cherry MX LP | 15.6 x 15.6 mm | 14.0 mm | 3.2 mm |
| Kailh Choc | 15.0 x 15.0 mm | 13.8 mm | 3.0 mm |

## Project Structure

```
gen-keeb-case/
├── gen_keeb_case/          # Python package
│   ├── __init__.py
│   ├── generator.py        # OpenSCAD code generator
│   └── switch_types.py     # Switch definitions
├── generate_case.py        # Main CLI script
├── examples.py             # Example generator
├── examples/               # Generated examples
│   ├── 60_percent_keyboard.scad
│   ├── numpad.scad
│   └── compact_choc.scad
└── README.md
```

## Future Enhancements

- Image-based layout detection
- Front profile customization
- PCB mounting holes
- Angled/tilted case designs
- Multiple case styles (floating key, integrated plate, etc.)
- STL export without OpenSCAD dependency
- Bluetooth/USB controller mounting
- Underglow LED support

## API Reference

### KeyboardLayout

Main class for defining keyboard layouts.

**Parameters:**
- `rows` (int, optional): Number of rows for grid layout
- `cols` (int, optional): Number of columns for grid layout
- `switch_type_name` (str): Switch type - "cherry_mx", "cherry_mx_lp", or "kailh_choc"
- `custom_keys` (list, optional): List of custom key positions
- `split` (bool): True for split keyboard layouts
- `split_distance` (float, optional): Distance between split halves in mm
- `separate_halves` (bool): True to generate separate cases for each half

**Custom Key Format:**
```python
{
    'x': float,              # X position in mm
    'y': float,              # Y position in mm
    'rotation': float,       # Rotation in degrees (optional)
    'half': str,            # 'left', 'right', or 'both' (optional, for split)
    'mirror': bool          # True to mirror, False to copy (optional, for 'both')
}
```

### CaseGenerator

Class for generating OpenSCAD code.

**Parameters:**
- `layout` (KeyboardLayout): The keyboard layout to generate
- `wall_thickness` (float): Case wall thickness in mm (default: 3.0)
- `base_height` (float): Height of case base in mm (default: 10.0)
- `top_clearance` (float): Clearance above switches in mm (default: 8.0)

**Methods:**
- `generate_scad()`: Returns OpenSCAD code as string
- `save(filename)`: Saves OpenSCAD code to file
- `generate_svg()`: Returns SVG top-down view as string
- `save_svg(filename)`: Saves SVG to file

## License

MIT License - See LICENSE file for details.
