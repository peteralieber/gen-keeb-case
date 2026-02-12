#!/usr/bin/env python3
"""
Test separate halves with surface optimization.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator
import os
import shutil

def test_separate_halves_surface():
    """Test separate halves with surface optimization."""
    print("\n=== Testing separate halves with surface optimization ===")
    
    # Create split keyboard layout
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
    
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=custom_keys,
        split=True,
        separate_halves=True
    )
    
    generator = CaseGenerator(
        layout=layout,
        name='test_separate_surface',
        optimization_method='surface'
    )
    
    # Create test directory
    test_dir = '/tmp/test_separate_surface'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Test export (which should create both left and right heightmaps)
    generator.export(test_dir)
    
    # Check that files were created
    scad_file = os.path.join(test_dir, 'test_separate_surface.scad')
    svg_file = os.path.join(test_dir, 'test_separate_surface.svg')
    left_heightmap = os.path.join(test_dir, 'test_separate_surface_heightmap_left.dat')
    right_heightmap = os.path.join(test_dir, 'test_separate_surface_heightmap_right.dat')
    
    print(f"Checking for files:")
    print(f"  SCAD: {os.path.exists(scad_file)}")
    print(f"  SVG: {os.path.exists(svg_file)}")
    print(f"  Left heightmap: {os.path.exists(left_heightmap)}")
    print(f"  Right heightmap: {os.path.exists(right_heightmap)}")
    
    assert os.path.exists(scad_file), "SCAD file not created"
    assert os.path.exists(svg_file), "SVG file not created"
    assert os.path.exists(left_heightmap), "Left heightmap not created"
    assert os.path.exists(right_heightmap), "Right heightmap not created"
    
    # Check SCAD file references both heightmaps
    with open(scad_file, 'r') as f:
        content = f.read()
    
    assert 'test_separate_surface_heightmap_left.dat' in content, "SCAD doesn't reference left heightmap"
    assert 'test_separate_surface_heightmap_right.dat' in content, "SCAD doesn't reference right heightmap"
    
    print("✓ All files created correctly")
    print("✓ SCAD file references both heightmaps correctly")
    
    # Clean up
    shutil.rmtree(test_dir)
    print("✓ Test passed!")

if __name__ == "__main__":
    test_separate_halves_surface()
