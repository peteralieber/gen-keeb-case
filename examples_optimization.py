#!/usr/bin/env python3
"""
Generate examples demonstrating different optimization methods.
This script creates the same keyboard layout with three different optimization methods
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
    
    # Generate with no optimization
    print("1. Generating without optimization...")
    generator_none = CaseGenerator(layout=layout, optimization_method='none')
    generator_none.save("examples/optimization_none.scad")
    
    # Generate with render() optimization
    print("2. Generating with render() optimization...")
    generator_render = CaseGenerator(layout=layout, optimization_method='render')
    generator_render.save("examples/optimization_render.scad")
    
    # Generate with surface() optimization
    print("3. Generating with surface() optimization...")
    generator_surface = CaseGenerator(layout=layout, optimization_method='surface')
    generator_surface.save("examples/optimization_surface.scad")
    
    print()
    print("✓ All optimization examples generated!")
    print()
    print("Performance comparison instructions:")
    print("1. Open each .scad file in OpenSCAD")
    print("2. Press F6 to render (this will show the render time)")
    print("3. Compare the render times:")
    print("   - optimization_none.scad: Baseline (no optimization)")
    print("   - optimization_render.scad: Using render() wrapper")
    print("   - optimization_surface.scad: Using surface() wrapper")
    print()
    print("Expected results:")
    print("- render() typically provides the best performance improvement")
    print("- surface() may work but has limitations with CSG operations")
    print("- With 75 keys, you should see noticeable performance differences")


if __name__ == "__main__":
    generate_optimization_examples()
