#!/usr/bin/env python3
"""
Test script for new CaseGenerator API features.
"""

import os
import shutil
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

def test_name_property():
    """Test that name property is set correctly."""
    print("\n=== Testing name property ===")
    layout = KeyboardLayout(rows=3, cols=3, switch_type_name="cherry_mx")
    
    # Test default name
    gen1 = CaseGenerator(layout=layout)
    assert gen1.name == 'keyboard_case', f"Expected 'keyboard_case', got '{gen1.name}'"
    print("✓ Default name: keyboard_case")
    
    # Test custom name
    gen2 = CaseGenerator(layout=layout, name='my_custom_case')
    assert gen2.name == 'my_custom_case', f"Expected 'my_custom_case', got '{gen2.name}'"
    print("✓ Custom name: my_custom_case")

def test_saveScad():
    """Test saveScad method."""
    print("\n=== Testing saveScad() ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='test_case')
    
    # Create test directory
    test_dir = '/tmp/test_scad'
    os.makedirs(test_dir, exist_ok=True)
    
    # Test saveScad without heightmap
    scad_file = os.path.join(test_dir, 'test.scad')
    generator.saveScad(scad_file)
    assert os.path.exists(scad_file), "SCAD file was not created"
    print(f"✓ saveScad() created file: {scad_file}")
    
    # Read and check content
    with open(scad_file, 'r') as f:
        content = f.read()
    assert '// Generated keyboard case' in content, "SCAD content is missing header"
    print("✓ SCAD file contains expected content")
    
    # Clean up
    shutil.rmtree(test_dir)

def test_saveScad_with_heightmap():
    """Test saveScad with heightmap parameter."""
    print("\n=== Testing saveScad() with heightmap ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='test_surface', optimization_method='surface')
    
    # Create test directory
    test_dir = '/tmp/test_heightmap'
    os.makedirs(test_dir, exist_ok=True)
    
    # Test saveScad with custom heightmap filename
    scad_file = os.path.join(test_dir, 'test.scad')
    heightmap_name = 'custom_heightmap.dat'
    generator.saveScad(scad_file, heightmap_name)
    
    assert os.path.exists(scad_file), "SCAD file was not created"
    print(f"✓ saveScad() with heightmap created SCAD file")
    
    # Check heightmap file was created
    heightmap_file = os.path.join(test_dir, heightmap_name)
    assert os.path.exists(heightmap_file), "Heightmap file was not created"
    print(f"✓ Heightmap file created: {heightmap_file}")
    
    # Check SCAD file references the custom heightmap
    with open(scad_file, 'r') as f:
        content = f.read()
    assert heightmap_name in content, f"SCAD file doesn't reference {heightmap_name}"
    print(f"✓ SCAD file references custom heightmap filename")
    
    # Clean up
    shutil.rmtree(test_dir)

def test_saveHeightMap():
    """Test saveHeightMap method."""
    print("\n=== Testing saveHeightMap() ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='test_case', optimization_method='surface')
    
    # Create test directory
    test_dir = '/tmp/test_save_heightmap'
    os.makedirs(test_dir, exist_ok=True)
    
    # Test saveHeightMap
    heightmap_file = os.path.join(test_dir, 'my_heightmap.dat')
    generator.saveHeightMap(heightmap_file)
    
    assert os.path.exists(heightmap_file), "Heightmap file was not created"
    print(f"✓ saveHeightMap() created file: {heightmap_file}")
    
    # Check file has content
    with open(heightmap_file, 'r') as f:
        content = f.read()
    assert len(content) > 0, "Heightmap file is empty"
    assert ' ' in content or '\n' in content, "Heightmap doesn't look like a DAT file"
    print("✓ Heightmap file contains data")
    
    # Clean up
    shutil.rmtree(test_dir)

def test_export():
    """Test export method."""
    print("\n=== Testing export() ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='exported_case')
    
    # Create test directory
    test_dir = '/tmp/test_export'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # Test export
    generator.export(test_dir)
    
    # Check files exist
    scad_file = os.path.join(test_dir, 'exported_case.scad')
    svg_file = os.path.join(test_dir, 'exported_case.svg')
    
    assert os.path.exists(scad_file), f"SCAD file not created: {scad_file}"
    assert os.path.exists(svg_file), f"SVG file not created: {svg_file}"
    print(f"✓ export() created SCAD file: exported_case.scad")
    print(f"✓ export() created SVG file: exported_case.svg")
    
    # Clean up
    shutil.rmtree(test_dir)

def test_export_with_surface():
    """Test export method with surface optimization."""
    print("\n=== Testing export() with surface optimization ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='surface_case', optimization_method='surface')
    
    # Create test directory
    test_dir = '/tmp/test_export_surface'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # Test export
    generator.export(test_dir)
    
    # Check files exist
    scad_file = os.path.join(test_dir, 'surface_case.scad')
    svg_file = os.path.join(test_dir, 'surface_case.svg')
    heightmap_file = os.path.join(test_dir, 'surface_case_heightmap.dat')
    
    assert os.path.exists(scad_file), f"SCAD file not created"
    assert os.path.exists(svg_file), f"SVG file not created"
    assert os.path.exists(heightmap_file), f"Heightmap file not created"
    print(f"✓ export() created SCAD file")
    print(f"✓ export() created SVG file")
    print(f"✓ export() created heightmap file")
    
    # Check SCAD references the heightmap
    with open(scad_file, 'r') as f:
        content = f.read()
    assert 'surface_case_heightmap.dat' in content, "SCAD doesn't reference heightmap"
    print(f"✓ SCAD file references heightmap")
    
    # Clean up
    shutil.rmtree(test_dir)

def test_backward_compatibility():
    """Test that old save() method still works (with deprecation warning)."""
    print("\n=== Testing backward compatibility with save() ===")
    layout = KeyboardLayout(rows=2, cols=3, switch_type_name="cherry_mx")
    generator = CaseGenerator(layout=layout, name='compat_case')
    
    # Create test directory
    test_dir = '/tmp/test_compat'
    os.makedirs(test_dir, exist_ok=True)
    
    # Test old save() method (should show deprecation warning)
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        scad_file = os.path.join(test_dir, 'test.scad')
        generator.save(scad_file)
        
        # Check that deprecation warning was issued
        assert len(w) == 1, f"Expected 1 warning, got {len(w)}"
        assert issubclass(w[0].category, DeprecationWarning), "Expected DeprecationWarning"
        assert "save() is deprecated" in str(w[0].message), "Wrong deprecation message"
        print("✓ save() shows deprecation warning")
    
    assert os.path.exists(scad_file), "SCAD file was not created"
    print(f"✓ save() still works for backward compatibility")
    
    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    print("Testing new CaseGenerator API features...")
    
    test_name_property()
    test_saveScad()
    test_saveScad_with_heightmap()
    test_saveHeightMap()
    test_export()
    test_export_with_surface()
    test_backward_compatibility()
    
    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)
