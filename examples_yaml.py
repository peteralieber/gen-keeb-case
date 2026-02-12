#!/usr/bin/env python3
"""
Example demonstrating YAML serialization and image detection features.
"""

import os
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def example_yaml_export():
    """Example: Create a layout and export it to YAML."""
    print("=" * 60)
    print("Example 1: Create and Export Layout to YAML")
    print("=" * 60)
    
    # Create a 60% keyboard layout
    layout = KeyboardLayout(
        rows=5,
        cols=15,
        switch_type_name="cherry_mx"
    )
    
    # Save to YAML
    output_yaml = "examples/60_percent_layout.yaml"
    layout.save_yaml(output_yaml)
    print(f"Saved layout to: {output_yaml}")
    
    # Display a preview of the YAML
    with open(output_yaml, 'r') as f:
        lines = f.readlines()
        print("\nYAML Preview (first 15 lines):")
        print("".join(lines[:15]))


def example_yaml_import():
    """Example: Import a layout from YAML and generate a case."""
    print("\n" + "=" * 60)
    print("Example 2: Import Layout from YAML")
    print("=" * 60)
    
    # Import from YAML
    yaml_file = "examples/60_percent_layout.yaml"
    layout = KeyboardLayout.load_yaml(yaml_file)
    print(f"Loaded layout from: {yaml_file}")
    print(f"  Layout: {layout.rows}x{layout.cols}")
    print(f"  Keys: {len(layout.custom_keys)}")
    print(f"  Switch: {layout.switch_type.name}")
    
    # Generate case from imported layout
    generator = CaseGenerator(layout=layout)
    output_scad = "examples/60_percent_from_yaml.scad"
    generator.save(output_scad)
    print(f"Generated case: {output_scad}")


def example_custom_layout():
    """Example: Create a custom layout with rotated keys."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Layout with Rotated Keys")
    print("=" * 60)
    
    spacing = 19.05
    
    # Create a small split keyboard with angled thumb keys
    custom_keys = []
    
    # Left half (3x4 grid)
    for row in range(3):
        for col in range(4):
            custom_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'rotation': 0
            })
    
    # Left thumb key (angled)
    custom_keys.append({
        'x': spacing * 1.5,
        'y': spacing * 3.5,
        'rotation': -15
    })
    
    # Right half (3x4 grid, offset)
    offset_x = spacing * 6
    for row in range(3):
        for col in range(4):
            custom_keys.append({
                'x': offset_x + col * spacing,
                'y': row * spacing,
                'rotation': 0
            })
    
    # Right thumb key (angled opposite)
    custom_keys.append({
        'x': offset_x + spacing * 2.5,
        'y': spacing * 3.5,
        'rotation': 15
    })
    
    # Create layout
    layout = KeyboardLayout(
        custom_keys=custom_keys,
        switch_type_name="kailh_choc"
    )
    
    print(f"Created custom layout with {len(layout.custom_keys)} keys")
    
    # Save to YAML
    yaml_file = "examples/custom_split_layout.yaml"
    layout.save_yaml(yaml_file)
    print(f"Saved to: {yaml_file}")
    
    # Generate case
    generator = CaseGenerator(layout=layout)
    scad_file = "examples/custom_split_case.scad"
    generator.save(scad_file)
    print(f"Generated: {scad_file}")
    
    # Show a sample of the YAML
    with open(yaml_file, 'r') as f:
        lines = f.readlines()
        print("\nYAML Preview (showing rotated keys):")
        # Find and show lines with rotation
        for i, line in enumerate(lines):
            if 'rotation: -15' in line or 'rotation: 15' in line:
                # Show context around rotated keys
                start = max(0, i-2)
                end = min(len(lines), i+1)
                print("".join(lines[start:end]))


def example_programmatic_workflow():
    """Example: Complete programmatic workflow."""
    print("\n" + "=" * 60)
    print("Example 4: Complete Programmatic Workflow")
    print("=" * 60)
    
    # 1. Create layout programmatically
    print("Step 1: Creating layout...")
    layout = KeyboardLayout(rows=3, cols=10, switch_type_name="cherry_mx")
    
    # 2. Save to YAML (for backup or sharing)
    yaml_path = "examples/compact_layout.yaml"
    print(f"Step 2: Saving to YAML: {yaml_path}")
    layout.save_yaml(yaml_path)
    
    # 3. Later, load from YAML
    print(f"Step 3: Loading from YAML...")
    loaded_layout = KeyboardLayout.load_yaml(yaml_path)
    
    # 4. Generate multiple outputs with different parameters
    print("Step 4: Generating cases with different parameters...")
    
    # Standard case
    gen1 = CaseGenerator(loaded_layout, wall_thickness=3.0)
    gen1.save("examples/compact_standard.scad")
    print("  - Standard case: examples/compact_standard.scad")
    
    # Thin-walled case
    gen2 = CaseGenerator(loaded_layout, wall_thickness=2.0, base_height=8.0)
    gen2.save("examples/compact_thin.scad")
    print("  - Thin-walled case: examples/compact_thin.scad")
    
    # Tall case
    gen3 = CaseGenerator(loaded_layout, base_height=15.0, top_clearance=10.0)
    gen3.save("examples/compact_tall.scad")
    print("  - Tall case: examples/compact_tall.scad")
    
    print("\nWorkflow complete! All files saved to examples/")


if __name__ == "__main__":
    # Make sure examples directory exists
    os.makedirs("examples", exist_ok=True)
    
    # Run all examples
    example_yaml_export()
    example_yaml_import()
    example_custom_layout()
    example_programmatic_workflow()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - YAML layouts: examples/*.yaml")
    print("  - OpenSCAD cases: examples/*.scad")
    print("\nNext steps:")
    print("  1. Open the YAML files to see the layout format")
    print("  2. Open the .scad files in OpenSCAD to view 3D models")
    print("  3. Try modifying the YAML files and re-generating cases")
