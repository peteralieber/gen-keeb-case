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
    
    print("\n✓ All example cases generated successfully!")
    print("\nYou can open these .scad files in OpenSCAD to view the 3D models.")


if __name__ == "__main__":
    import os
    os.makedirs("examples", exist_ok=True)
    generate_example_cases()
