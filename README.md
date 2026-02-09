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

### Generate Custom Case

```bash
python3 generate_case.py --rows 5 --cols 15 --switch-type cherry_mx --output my_keyboard.scad
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

## License

MIT License - See LICENSE file for details.
