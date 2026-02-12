#!/usr/bin/env python3
"""
Test script for overlap detection and new features.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def test_overlap_detection():
    """Test that overlapping keys are detected."""
    print("Testing overlap detection...")
    
    # Test 1: Non-overlapping keys should work
    try:
        custom_keys = [
            {'x': 0, 'y': 0},
            {'x': 19.05, 'y': 0},
            {'x': 38.1, 'y': 0}
        ]
        layout = KeyboardLayout(switch_type_name="cherry_mx", custom_keys=custom_keys)
        print("✓ Test 1 passed: Non-overlapping keys accepted")
    except ValueError as e:
        print(f"✗ Test 1 failed: {e}")
    
    # Test 2: Overlapping keys should fail
    try:
        custom_keys = [
            {'x': 0, 'y': 0},
            {'x': 5, 'y': 0},  # Too close!
        ]
        layout = KeyboardLayout(switch_type_name="cherry_mx", custom_keys=custom_keys)
        print("✗ Test 2 failed: Overlapping keys should have raised ValueError")
    except ValueError as e:
        print(f"✓ Test 2 passed: Overlapping keys rejected - {e}")


def test_grid_plus_custom():
    """Test combining grid and custom keys."""
    print("\nTesting grid + custom keys...")
    
    try:
        # Create a 3x3 grid and add custom keys above it
        custom_keys = [
            {'x': 19.05, 'y': -19.05},  # Above the grid
            {'x': 38.1, 'y': -19.05},
        ]
        layout = KeyboardLayout(rows=3, cols=3, switch_type_name="cherry_mx", custom_keys=custom_keys)
        print(f"✓ Grid + custom keys: {len(layout.custom_keys)} total keys (9 grid + 2 custom)")
    except Exception as e:
        print(f"✗ Grid + custom failed: {e}")


def test_split_keyboard_basic():
    """Test basic split keyboard."""
    print("\nTesting basic split keyboard...")
    
    try:
        # Create a simple split keyboard
        layout = KeyboardLayout(
            rows=3, 
            cols=6, 
            switch_type_name="cherry_mx",
            split=True,
            split_distance=20
        )
        print(f"✓ Split keyboard created with {len(layout.custom_keys)} keys")
    except Exception as e:
        print(f"✗ Split keyboard failed: {e}")


def test_custom_keys_both_halves():
    """Test custom keys on both halves."""
    print("\nTesting custom keys on both halves...")
    
    try:
        # Create custom keys that should appear on both halves
        custom_keys = [
            {'x': 0, 'y': 0, 'half': 'left'},
            {'x': 19.05, 'y': 0, 'half': 'left'},
            {'x': 0, 'y': 0, 'half': 'right'},
            {'x': 19.05, 'y': 0, 'half': 'right'},
        ]
        layout = KeyboardLayout(switch_type_name="cherry_mx", custom_keys=custom_keys, split=True)
        print(f"✓ Custom keys on both halves: {len(layout.custom_keys)} keys")
    except Exception as e:
        print(f"✗ Custom keys on both halves failed: {e}")


def test_custom_keys_both_mode():
    """Test custom keys with 'both' mode (mirror and copy)."""
    print("\nTesting 'both' mode for custom keys...")
    
    try:
        # Test copy mode (same position on both halves)
        custom_keys = [
            {'x': 10, 'y': 10, 'half': 'both', 'mirror': False},
        ]
        layout = KeyboardLayout(switch_type_name="cherry_mx", custom_keys=custom_keys, split=True)
        print(f"✓ Copy mode: Expanded to {len(layout.custom_keys)} keys")
        
        # Test mirror mode (mirrored position)
        custom_keys = [
            {'x': 10, 'y': 10, 'half': 'both', 'mirror': True, 'rotation': 15},
        ]
        layout = KeyboardLayout(switch_type_name="cherry_mx", custom_keys=custom_keys, split=True)
        print(f"✓ Mirror mode: Expanded to {len(layout.custom_keys)} keys")
    except Exception as e:
        print(f"✗ Both mode failed: {e}")


if __name__ == "__main__":
    test_overlap_detection()
    test_grid_plus_custom()
    test_split_keyboard_basic()
    test_custom_keys_both_halves()
    test_custom_keys_both_mode()
    print("\n✓ All tests completed!")
