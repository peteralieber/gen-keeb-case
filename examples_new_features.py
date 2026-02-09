#!/usr/bin/env python3
"""
Example demonstrating the new features: grid + custom keys with split support.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def example_1_grid_with_custom_keys():
    """Example 1: A grid layout with additional custom keys (e.g., thumb cluster)."""
    print("Example 1: 3x6 grid with custom thumb keys...")
    
    spacing = 19.05
    
    # Add custom thumb keys below the grid
    custom_keys = [
        {'x': spacing * 1.5, 'y': spacing * 3.5, 'rotation': -10},
        {'x': spacing * 2.5, 'y': spacing * 3.5, 'rotation': 0},
        {'x': spacing * 3.5, 'y': spacing * 3.5, 'rotation': 10},
    ]
    
    layout = KeyboardLayout(
        rows=3,
        cols=6,
        switch_type_name="cherry_mx",
        custom_keys=custom_keys
    )
    
    generator = CaseGenerator(layout=layout)
    generator.save("examples/grid_with_custom_keys.scad")
    generator.save_svg("examples/grid_with_custom_keys.svg")
    print(f"  Generated with {len(layout.custom_keys)} keys (18 grid + 3 custom)")


def example_2_split_keyboard_unified():
    """Example 2: Split keyboard in a single unified case."""
    print("\nExample 2: Split keyboard (unified case)...")
    
    spacing = 19.05
    
    # Left half: 3x6 grid
    left_keys = []
    for row in range(3):
        for col in range(6):
            left_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'left'
            })
    
    # Right half: 3x6 grid with offset
    split_gap = spacing * 2  # 2 key widths gap between halves
    right_keys = []
    for row in range(3):
        for col in range(6):
            right_keys.append({
                'x': (col + 8) * spacing,  # Offset to the right
                'y': row * spacing,
                'half': 'right'
            })
    
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=left_keys + right_keys,
        split=True,
        split_distance=split_gap
    )
    
    generator = CaseGenerator(layout=layout)
    generator.save("examples/split_keyboard_unified.scad")
    generator.save_svg("examples/split_keyboard_unified.svg")
    print(f"  Generated with {len(layout.custom_keys)} keys")


def example_3_split_with_both_halves_copy():
    """Example 3: Split keyboard with custom keys copied to both halves."""
    print("\nExample 3: Split keyboard with copied custom keys...")
    
    spacing = 19.05
    
    # Main grid on left
    left_keys = []
    for row in range(4):
        for col in range(5):
            left_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'left'
            })
    
    # Main grid on right
    right_keys = []
    for row in range(4):
        for col in range(5):
            right_keys.append({
                'x': (col + 7) * spacing,
                'y': row * spacing,
                'half': 'right'
            })
    
    # Custom thumb keys that will be copied to both halves
    # Using 'both' with mirror=False means same position on each half
    thumb_keys = [
        {'x': spacing * 1.5, 'y': spacing * 4.2, 'rotation': 0, 'half': 'both', 'mirror': False},
        {'x': spacing * 2.5, 'y': spacing * 4.2, 'rotation': 0, 'half': 'both', 'mirror': False},
    ]
    
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=left_keys + right_keys + thumb_keys,
        split=True,
        split_distance=spacing * 2
    )
    
    generator = CaseGenerator(layout=layout)
    generator.save("examples/split_keyboard_copied_thumbs.scad")
    generator.save_svg("examples/split_keyboard_copied_thumbs.svg")
    print(f"  Generated with {len(layout.custom_keys)} keys (includes copied thumbs)")


def example_4_split_with_both_halves_mirror():
    """Example 4: Split keyboard with custom keys mirrored to both halves."""
    print("\nExample 4: Split keyboard with mirrored custom keys...")
    
    spacing = 19.05
    
    # Simple layout with just custom keys
    # Left side keys
    left_keys = []
    for row in range(3):
        for col in range(5):
            left_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'half': 'left'
            })
    
    # Right side keys (positioned separately)
    right_keys = []
    for row in range(3):
        for col in range(5):
            right_keys.append({
                'x': (col + 7) * spacing,
                'y': row * spacing,
                'half': 'right'
            })
    
    # Thumb keys that will be mirrored
    # Using 'both' with mirror=True means mirrored position and rotation
    thumb_keys = [
        {'x': spacing * 1.0, 'y': spacing * 3.3, 'rotation': -15, 'half': 'both', 'mirror': True},
        {'x': spacing * 2.0, 'y': spacing * 3.5, 'rotation': -10, 'half': 'both', 'mirror': True},
    ]
    
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=left_keys + right_keys + thumb_keys,
        split=True,
        split_distance=spacing * 2
    )
    
    generator = CaseGenerator(layout=layout)
    generator.save("examples/split_keyboard_mirrored_thumbs.scad")
    generator.save_svg("examples/split_keyboard_mirrored_thumbs.svg")
    print(f"  Generated with {len(layout.custom_keys)} keys (includes mirrored thumbs)")


def example_5_error_handling():
    """Example 5: Demonstrate error handling for overlapping keys."""
    print("\nExample 5: Error handling for overlapping keys...")
    
    try:
        # These keys are too close and should fail
        overlapping_keys = [
            {'x': 0, 'y': 0},
            {'x': 10, 'y': 0},  # Too close! Should be at least ~15mm apart
        ]
        
        layout = KeyboardLayout(
            switch_type_name="cherry_mx",
            custom_keys=overlapping_keys
        )
        print("  ERROR: Overlapping keys were not detected!")
    except ValueError as e:
        print(f"  ✓ Gracefully caught overlap: {e}")


if __name__ == "__main__":
    import os
    os.makedirs("examples", exist_ok=True)
    
    example_1_grid_with_custom_keys()
    example_2_split_keyboard_unified()
    example_3_split_with_both_halves_copy()
    example_4_split_with_both_halves_mirror()
    example_5_error_handling()
    
    print("\n✓ All examples generated successfully!")
    print("\nYou can open the .scad files in OpenSCAD to view the 3D models.")
    print("You can open the .svg files in a web browser to view the top-down layouts.")
