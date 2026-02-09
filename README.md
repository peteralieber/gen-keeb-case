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
- 🖼️ **Image detection**: Detect keyboard layout from top-down images
- 📄 **YAML serialization**: Save and load keyboard layouts from YAML files

## Installation

Install the required dependencies:

```bash
git clone https://github.com/peteralieber/gen-keeb-case.git
cd gen-keeb-case
pip install -r requirements.txt
```

For basic case generation (grid layouts only), no external dependencies are required.
For image detection and YAML support, install:
- OpenCV (`opencv-python`)
- PyYAML (`PyYAML`)

## Quick Start

### Generate Example Cases

```bash
python3 examples.py
```

This creates example cases in the `examples/` directory:
- `60_percent_keyboard.scad` - Standard 60% keyboard (5x15)
- `numpad.scad` - Numeric keypad (5x4)
- `compact_choc.scad` - Compact keyboard with Kailh Choc switches (3x10)
- `split_keyboard_angled_thumbs.scad` - Split keyboard with custom angled thumb keys

### Generate YAML Examples

```bash
python3 examples_yaml.py
```

This demonstrates YAML serialization features and creates:
- YAML layout files in `examples/*.yaml`
- Multiple OpenSCAD cases from imported YAML layouts

### Generate Custom Case

```bash
python3 generate_case.py --rows 5 --cols 15 --switch-type cherry_mx --output my_keyboard.scad
```

### Detect Layout from Image

Detect keyboard layout from a top-down image and generate a case:

```bash
python3 generate_case.py --image keyboard_photo.png --reference-spacing 60 --visualize --save-yaml layout.yaml --output detected_case.scad
```

Options:
- `--image`: Path to top-down keyboard image
- `--reference-spacing`: Spacing between keys in pixels (helps with scale calibration)
- `--visualize`: Show detected keys overlaid on the image
- `--save-yaml`: Save the detected layout to a YAML file

### Import Layout from YAML

Load a previously saved or manually created layout from a YAML file:

```bash
python3 generate_case.py --import-yaml layout.yaml --output case_from_yaml.scad
```

### Complete Workflow Example

1. Take a top-down photo of your keyboard
2. Detect the layout and save to YAML:
   ```bash
   python3 generate_case.py --image my_keyboard.jpg --reference-spacing 80 --save-yaml my_layout.yaml --visualize
   ```
3. Edit the YAML file if needed to fine-tune positions
4. Generate the case from the YAML:
   ```bash
   python3 generate_case.py --import-yaml my_layout.yaml --output my_case.scad
   ```

### Available Options

#### Input Options
```
--import-yaml       Import keyboard layout from a YAML file
--image             Detect keyboard layout from a top-down image
```

#### Image Detection Options (used with --image)
```
--reference-spacing Known spacing between keys in pixels (for scale calibration)
--visualize         Show detected keys overlaid on the image
--save-yaml         Save detected layout to YAML file
```

#### Manual Layout Options (used when not importing)
```
--rows              Number of rows (default: 5)
--cols              Number of columns (default: 15)
--switch-type       Switch type: cherry_mx, cherry_mx_lp, kailh_choc (default: cherry_mx)
```

#### Case Parameters
```
--wall-thickness    Case wall thickness in mm (default: 3.0)
--base-height       Height of case base in mm (default: 10.0)
--top-clearance     Clearance above switches in mm (default: 8.0)
```

#### Output Options
```
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

## YAML Layout Format

Keyboard layouts can be saved and loaded from YAML files. The format supports both grid and custom layouts:

### Grid Layout Example
```yaml
switch_type: Cherry MX
key_spacing: 19.05
grid:
  rows: 5
  cols: 15
keys:
  - x: 0.0
    y: 0.0
    rotation: 0
  - x: 19.05
    y: 0.0
    rotation: 0
  # ... more keys
```

### Custom Layout Example (with rotations)
```yaml
switch_type: Kailh Choc
key_spacing: 19.05
keys:
  - x: 0.0
    y: 0.0
    rotation: 0
  - x: 19.05
    y: 0.0
    rotation: 0
  - x: 30.0
    y: 50.0
    rotation: -15  # Angled key (e.g., thumb cluster)
```

Fields:
- `switch_type`: The display name of the switch type (e.g., "Cherry MX", "Kailh Choc")
- `key_spacing`: Spacing between keys in mm (standard is 19.05mm)
- `grid`: Optional - if present, indicates a regular grid layout
- `keys`: List of key positions with x, y coordinates (in mm) and optional rotation (in degrees)

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

- ✅ ~~Image-based layout detection~~ (Implemented!)
- ✅ ~~YAML serialization for layouts~~ (Implemented!)
- Front profile customization
- PCB mounting holes
- Angled/tilted case designs
- Multiple case styles (floating key, integrated plate, etc.)
- STL export without OpenSCAD dependency

## License

MIT License - See LICENSE file for details.
