#!/usr/bin/env python3
"""
Test script for optimization methods feature.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def test_optimization_methods():
    """Test that all three optimization methods generate valid SCAD code."""
    print("Testing optimization methods...")
    
    # Create a simple layout
    layout = KeyboardLayout(rows=3, cols=3, switch_type_name="cherry_mx")
    
    # Test 1: None optimization
    try:
        generator = CaseGenerator(layout=layout, optimization_method='none')
        scad_code = generator.generate_scad()
        assert "// Optimization: none" in scad_code
        # Check that switch_plate() is called without any wrapper
        assert "switch_plate();" in scad_code
        assert "render()" not in scad_code
        assert "surface()" not in scad_code
        print("✓ Test 1 passed: 'none' optimization works correctly")
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        return False
    
    # Test 2: Render optimization
    try:
        generator = CaseGenerator(layout=layout, optimization_method='render')
        scad_code = generator.generate_scad()
        assert "// Optimization: render" in scad_code
        # Check that render() wraps switch_plate()
        assert "render()" in scad_code and "switch_plate();" in scad_code
        print("✓ Test 2 passed: 'render' optimization works correctly")
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        return False
    
    # Test 3: Surface optimization
    try:
        generator = CaseGenerator(layout=layout, optimization_method='surface')
        scad_code = generator.generate_scad()
        assert "// Optimization: surface" in scad_code
        # Check that surface() wraps switch_plate()
        assert "surface()" in scad_code and "switch_plate();" in scad_code
        print("✓ Test 3 passed: 'surface' optimization works correctly")
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        return False
    
    # Test 4: Invalid optimization method
    try:
        generator = CaseGenerator(layout=layout, optimization_method='invalid')
        print("✗ Test 4 failed: Invalid optimization should have raised ValueError")
        return False
    except ValueError as e:
        print(f"✓ Test 4 passed: Invalid optimization rejected - {e}")
    
    # Test 5: Split keyboard with optimization
    try:
        spacing = 19.05
        left_keys = [{'x': 0, 'y': 0, 'half': 'left'}]
        right_keys = [{'x': spacing * 8, 'y': 0, 'half': 'right'}]
        
        split_layout = KeyboardLayout(
            switch_type_name="cherry_mx",
            custom_keys=left_keys + right_keys,
            split=True,
            separate_halves=True
        )
        
        generator = CaseGenerator(layout=split_layout, optimization_method='render')
        scad_code = generator.generate_scad()
        # Check that render() wraps both left and right switch plates
        assert "render()" in scad_code
        assert "left_switch_plate();" in scad_code
        assert "right_switch_plate();" in scad_code
        print("✓ Test 5 passed: Split keyboard with optimization works correctly")
    except Exception as e:
        print(f"✗ Test 5 failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = test_optimization_methods()
    if success:
        print("\n✓ All optimization tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
