#!/usr/bin/env python3
"""
Demonstrate the new export() method and name property.
This example shows how to use the new CaseGenerator API.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator
import os

def demo_export_method():
    """Demonstrate the new export() method."""
    
    print("="*60)
    print("Demonstrating new CaseGenerator API features")
    print("="*60)
    
    # Example 1: Basic export with name
    print("\n1. Basic export with custom name:")
    print("-" * 60)
    layout1 = KeyboardLayout(rows=3, cols=10, switch_type_name="cherry_mx")
    generator1 = CaseGenerator(layout=layout1, name="compact_30key")
    generator1.export("examples/exported")
    
    # Example 2: Export with surface optimization (includes heightmap)
    print("\n2. Export with surface optimization:")
    print("-" * 60)
    layout2 = KeyboardLayout(rows=5, cols=15, switch_type_name="cherry_mx")
    generator2 = CaseGenerator(
        layout=layout2, 
        name="full_75key",
        optimization_method='surface'
    )
    generator2.export("examples/exported")
    
    # Example 3: Split keyboard with custom name
    print("\n3. Split keyboard export:")
    print("-" * 60)
    spacing = 19.05
    custom_keys = []
    
    # Left half
    for row in range(3):
        for col in range(6):
            custom_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'left'
            })
    
    # Right half
    for row in range(3):
        for col in range(6):
            custom_keys.append({
                'x': (col + 8) * spacing,
                'y': row * spacing,
                'half': 'right'
            })
    
    layout3 = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=custom_keys,
        split=True
    )
    generator3 = CaseGenerator(layout=layout3, name="split_36key")
    generator3.export("examples/exported")
    
    # Example 4: Using saveScad directly with custom heightmap filename
    print("\n4. Advanced: Custom heightmap filename:")
    print("-" * 60)
    layout4 = KeyboardLayout(rows=4, cols=12, switch_type_name="cherry_mx")
    generator4 = CaseGenerator(
        layout=layout4,
        name="planck_48key",
        optimization_method='surface'
    )
    os.makedirs("examples/exported", exist_ok=True)
    generator4.saveScad(
        "examples/exported/planck_48key.scad",
        "planck_custom_heightmap.dat"
    )
    print("  Generated with custom heightmap filename")
    
    # Example 5: Separate heightmap save
    print("\n5. Saving heightmap separately:")
    print("-" * 60)
    layout5 = KeyboardLayout(rows=2, cols=8, switch_type_name="kailh_choc")
    generator5 = CaseGenerator(
        layout=layout5,
        name="mini_16key",
        optimization_method='surface'
    )
    os.makedirs("examples/exported", exist_ok=True)
    generator5.saveScad("examples/exported/mini_16key.scad")
    generator5.saveHeightMap("examples/exported/mini_16key_manual.dat")
    print("  Note: Heightmap saved manually, SCAD file won't reference it")
    
    print("\n" + "="*60)
    print("✓ All export examples completed!")
    print("="*60)
    print("\nGenerated files are in examples/exported/")
    print("Each case has a descriptive name prefix:")
    print("  - compact_30key.*")
    print("  - full_75key.* (with heightmap)")
    print("  - split_36key.*")
    print("  - planck_48key.* (with custom heightmap name)")
    print("  - mini_16key.*")
    print("\nYou can open .scad files in OpenSCAD to view 3D models")
    print("You can open .svg files in a browser to view top-down layouts")

if __name__ == "__main__":
    demo_export_method()
