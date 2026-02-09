#!/usr/bin/env python3
"""
Main script to generate keyboard case OpenSCAD files.
"""

import sys
import argparse
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator
from gen_keeb_case.switch_types import SWITCH_TYPES


def main():
    parser = argparse.ArgumentParser(
        description="Generate OpenSCAD model for a mechanical keyboard case"
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--import-yaml",
        help="Import keyboard layout from a YAML file"
    )
    input_group.add_argument(
        "--image",
        help="Detect keyboard layout from a top-down image"
    )
    
    # Image detection options
    parser.add_argument(
        "--reference-spacing",
        type=float,
        help="Known spacing between keys in pixels (for image detection)"
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Visualize detected keys from image"
    )
    parser.add_argument(
        "--save-yaml",
        help="Save detected layout to YAML file (used with --image)"
    )
    
    # Manual layout options (used when not importing)
    parser.add_argument(
        "--rows",
        type=int,
        default=5,
        help="Number of rows in the keyboard layout (default: 5)"
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=15,
        help="Number of columns in the keyboard layout (default: 15)"
    )
    parser.add_argument(
        "--switch-type",
        choices=list(SWITCH_TYPES.keys()),
        default="cherry_mx",
        help="Type of mechanical switch (default: cherry_mx)"
    )
    
    # Case parameters
    parser.add_argument(
        "--wall-thickness",
        type=float,
        default=3.0,
        help="Thickness of case walls in mm (default: 3.0)"
    )
    parser.add_argument(
        "--base-height",
        type=float,
        default=10.0,
        help="Height of case base in mm (default: 10.0)"
    )
    parser.add_argument(
        "--top-clearance",
        type=float,
        default=8.0,
        help="Clearance above switches in mm (default: 8.0)"
    )
    
    # Output options
    parser.add_argument(
        "--output",
        "-o",
        default="keyboard_case.scad",
        help="Output filename (default: keyboard_case.scad)"
    )
    
    args = parser.parse_args()
    
    # Create layout based on input method
    if args.import_yaml:
        # Import from YAML file
        print(f"Importing layout from {args.import_yaml}...")
        layout = KeyboardLayout.load_yaml(args.import_yaml)
        print(f"  Loaded layout with {len(layout.custom_keys)} keys")
        
    elif args.image:
        # Detect from image
        print(f"Detecting keyboard layout from image: {args.image}")
        
        from gen_keeb_case.image_detector import detect_keyboard_from_image
        
        # Detect layout from image
        layout_dict = detect_keyboard_from_image(
            args.image,
            switch_type_name=args.switch_type,
            reference_spacing_px=args.reference_spacing,
            visualize=args.visualize,
            output_vis_path=args.output.replace('.scad', '_detection.png') if args.visualize else None
        )
        
        print(f"  Detected {len(layout_dict['keys'])} keys")
        
        # Save to YAML if requested
        if args.save_yaml:
            import yaml
            with open(args.save_yaml, 'w') as f:
                yaml.dump(layout_dict, f, default_flow_style=False, sort_keys=False)
            print(f"  Layout saved to {args.save_yaml}")
        
        # Create layout from detected data
        layout = KeyboardLayout.from_dict(layout_dict)
        
    else:
        # Create manual grid layout
        layout = KeyboardLayout(
            rows=args.rows,
            cols=args.cols,
            switch_type_name=args.switch_type
        )
    
    # Create generator
    generator = CaseGenerator(
        layout=layout,
        wall_thickness=args.wall_thickness,
        base_height=args.base_height,
        top_clearance=args.top_clearance
    )
    
    # Generate and save
    print(f"\nGenerating keyboard case:")
    if layout.rows and layout.cols:
        print(f"  Layout: {layout.rows} rows x {layout.cols} columns")
    else:
        print(f"  Layout: Custom ({len(layout.custom_keys)} keys)")
    print(f"  Switch type: {layout.switch_type.name}")
    print(f"  Dimensions: {layout.get_dimensions()[0]:.2f}mm x {layout.get_dimensions()[1]:.2f}mm")
    print()
    
    generator.save(args.output)
    print()
    print(f"Success! You can now open '{args.output}' in OpenSCAD to view and render the model.")


if __name__ == "__main__":
    main()
