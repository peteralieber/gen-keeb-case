#!/usr/bin/env python3
"""
Test separate halves feature.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def test_separate_halves():
    """Test generating separate halves."""
    print("Testing separate halves generation...")
    
    spacing = 19.05
    
    # Left half: 3x5 grid
    left_keys = []
    for row in range(3):
        for col in range(5):
            left_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'left'
            })
    
    # Right half: 3x5 grid
    right_keys = []
    for row in range(3):
        for col in range(5):
            right_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'right'
            })
    
    # Create layout with separate halves
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=left_keys + right_keys,
        split=True,
        split_distance=spacing * 2,
        separate_halves=True
    )
    
    generator = CaseGenerator(layout=layout)
    generator.save("examples/separate_halves.scad")
    print(f"✓ Generated separate halves with {len(layout.custom_keys)} keys")


if __name__ == "__main__":
    import os
    os.makedirs("examples", exist_ok=True)
    test_separate_halves()
    print("\n✓ Test completed!")
