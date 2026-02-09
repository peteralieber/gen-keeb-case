#!/usr/bin/env python3
"""
Example script demonstrating the keyboard case generator.
"""

from gen_keeb_case.generator import KeyboardLayout, CaseGenerator


def generate_example_cases():
    """Generate several example keyboard cases."""
    
    examples = [
        {
            "name": "60_percent_keyboard",
            "rows": 5,
            "cols": 15,
            "switch_type": "cherry_mx",
            "description": "Standard 60% keyboard layout"
        },
        {
            "name": "numpad",
            "rows": 5,
            "cols": 4,
            "switch_type": "cherry_mx",
            "description": "Numeric keypad"
        },
        {
            "name": "compact_choc",
            "rows": 3,
            "cols": 10,
            "switch_type": "kailh_choc",
            "description": "Compact keyboard with Kailh Choc switches"
        }
    ]
    
    for example in examples:
        print(f"\nGenerating {example['description']}...")
        print(f"  Output: examples/{example['name']}.scad")
        print(f"  Output: examples/{example['name']}.svg")
        
        # Create layout
        layout = KeyboardLayout(
            rows=example["rows"],
            cols=example["cols"],
            switch_type_name=example["switch_type"]
        )
        
        # Create generator
        generator = CaseGenerator(layout=layout)
        
        # Save to examples directory
        generator.save(f"examples/{example['name']}.scad")
        generator.save_svg(f"examples/{example['name']}.svg")
    
    # Generate split keyboard with angled thumb keys
    print(f"\nGenerating Split keyboard with angled thumb keys...")
    print(f"  Output: examples/split_keyboard_angled_thumbs.scad")
    print(f"  Output: examples/split_keyboard_angled_thumbs.svg")
    generate_split_keyboard_example()
    
    print("\n✓ All example cases generated successfully!")
    print("\nYou can open these .scad files in OpenSCAD to view the 3D models.")
    print("You can open the .svg files in a web browser to view the top-down layouts.")


def generate_split_keyboard_example():
    """Generate a split keyboard with angled thumb keys."""
    spacing = 19.05  # Standard key spacing
    
    # Define custom key positions
    custom_keys = []
    
    # Left half - 3 rows, 6 columns
    for row in range(3):
        for col in range(6):
            custom_keys.append({
                'x': col * spacing,
                'y': row * spacing,
                'rotation': 0
            })
    
    # Left thumb cluster - 2 keys at an angle
    thumb_base_x = spacing * 1.5
    thumb_base_y = spacing * 3.2
    custom_keys.append({
        'x': thumb_base_x,
        'y': thumb_base_y,
        'rotation': -15  # Angled inward
    })
    custom_keys.append({
        'x': thumb_base_x + spacing * 1.0,
        'y': thumb_base_y + spacing * 0.1,
        'rotation': -10
    })
    
    # Right half - 3 rows, 6 columns (offset to the right)
    right_offset = spacing * 8  # Gap between halves
    for row in range(3):
        for col in range(6):
            custom_keys.append({
                'x': right_offset + col * spacing,
                'y': row * spacing,
                'rotation': 0
            })
    
    # Right thumb cluster - 2 keys at an angle
    thumb_base_x_right = right_offset + spacing * 3.5
    thumb_base_y_right = spacing * 3.2
    custom_keys.append({
        'x': thumb_base_x_right,
        'y': thumb_base_y_right,
        'rotation': 10  # Angled inward (opposite direction)
    })
    custom_keys.append({
        'x': thumb_base_x_right + spacing * 1.0,
        'y': thumb_base_y_right + spacing * 0.1,
        'rotation': 15
    })
    
    # Create layout with custom keys
    layout = KeyboardLayout(
        switch_type_name="cherry_mx",
        custom_keys=custom_keys
    )
    
    # Create generator
    generator = CaseGenerator(layout=layout)
    
    # Save files
    generator.save("examples/split_keyboard_angled_thumbs.scad")
    generator.save_svg("examples/split_keyboard_angled_thumbs.svg")


if __name__ == "__main__":
    import os
    os.makedirs("examples", exist_ok=True)
    generate_example_cases()
