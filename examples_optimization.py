#!/usr/bin/env python3
"""
Generate examples demonstrating different optimization methods.
This script creates the same keyboard layout with two different optimization methods
so you can compare their performance in OpenSCAD.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def generate_optimization_examples():
    """Generate example keyboards with different optimization methods."""
    
    # Create a keyboard layout with many keys to demonstrate performance differences
    layout = KeyboardLayout(
        rows=5,
        cols=15,
        switch_type_name="cherry_mx"
    )
    
    print("Generating keyboard cases with different optimization methods...")
    print(f"Layout: 5 rows x 15 columns (75 keys total)")
    print()
    
    # Generate with render() optimization (default)
    print("1. Generating with render() optimization...")
    generator_render = CaseGenerator(layout=layout, optimization_method='render')
    generator_render.saveScad("examples/optimization_render.scad")
    
    # Generate with surface() optimization (creates height map)
    print("2. Generating with surface() optimization (with height map)...")
    generator_surface = CaseGenerator(layout=layout, optimization_method='surface')
    # Note: When using surface optimization without explicit heightmap_filename,
    # the heightmap is not automatically saved. Use export() or provide heightmap_filename.
    generator_surface.saveScad("examples/optimization_surface.scad")
    generator_surface.saveHeightMap("examples/switch_plate_heightmap.dat")
    
    print()
    print("✓ All optimization examples generated!")
    print()
    print("Performance comparison instructions:")
    print("1. Open each .scad file in OpenSCAD")
    print("2. Press F6 to render (this will show the render time)")
    print("3. Compare the render times:")
    print("   - optimization_render.scad: Using render() wrapper (recommended)")
    print("   - optimization_surface.scad: Using surface() with height map file")
    print()
    print("Expected results:")
    print("- render() provides significant performance improvement for many keys")
    print("- surface() method creates a height map file and uses OpenSCAD's surface()")
    print("- With 75 keys, you should see noticeable performance differences")
    print()
    print("Note: The surface() method generates .dat height map files in the examples/ directory.")


if __name__ == "__main__":
    generate_optimization_examples()
