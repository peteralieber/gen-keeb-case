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
    parser.add_argument(
        "--output",
        "-o",
        default="keyboard_case.scad",
        help="Output filename (default: keyboard_case.scad)"
    )
    
    args = parser.parse_args()
    
    # Create layout
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
    print(f"Generating keyboard case:")
    print(f"  Layout: {args.rows} rows x {args.cols} columns")
    print(f"  Switch type: {layout.switch_type.name}")
    print(f"  Dimensions: {layout.get_dimensions()[0]:.2f}mm x {layout.get_dimensions()[1]:.2f}mm")
    print()
    
    generator.save(args.output)
    print()
    print(f"Success! You can now open '{args.output}' in OpenSCAD to view and render the model.")


if __name__ == "__main__":
    main()
