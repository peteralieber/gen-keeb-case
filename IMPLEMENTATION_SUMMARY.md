# CaseGenerator API Changes Summary

## Overview
This PR implements the requested enhancements to the CaseGenerator class API as specified in the problem statement.

## Changes Implemented

### 1. Added `name` Property
- **Location**: `gen_keeb_case/generator.py` - `CaseGenerator.__init__()`
- **Default value**: `'keyboard_case'`
- **Purpose**: Provides a descriptive name for the case that is used as a prefix when exporting files
- **Example**:
  ```python
  generator = CaseGenerator(layout=layout, name='my_custom_keyboard')
  ```

### 2. Renamed `save()` to `saveScad()`
- **Location**: `gen_keeb_case/generator.py` - `saveScad()` method
- **Signature**: `saveScad(filename, heightmap_filename=None)`
- **Changes**:
  - More descriptive method name
  - Accepts optional `heightmap_filename` parameter
  - Only saves heightmap when `heightmap_filename` is explicitly provided
  - Updates SCAD file to reference the custom heightmap filename
- **Backward compatibility**: Old `save()` method still exists with deprecation warning
- **Example**:
  ```python
  # Basic usage
  generator.saveScad("output.scad")
  
  # With custom heightmap
  generator.saveScad("output.scad", "custom_map.dat")
  ```

### 3. Added `saveHeightMap()` Method
- **Location**: `gen_keeb_case/generator.py` - `saveHeightMap()` method
- **Signature**: `saveHeightMap(filename)`
- **Purpose**: Saves the heightmap to a specific file
- **Features**:
  - Only applicable when `optimization_method='surface'`
  - Automatically handles separate halves by creating `_left` and `_right` versions
  - Shows warning if called with non-surface optimization method
- **Example**:
  ```python
  generator = CaseGenerator(layout=layout, optimization_method='surface')
  generator.saveHeightMap("my_heightmap.dat")
  # Creates my_heightmap_left.dat and my_heightmap_right.dat for separate halves
  ```

### 4. Added `export()` Method
- **Location**: `gen_keeb_case/generator.py` - `export()` method
- **Signature**: `export(path)`
- **Purpose**: Exports all case files to a directory with the name property as prefix
- **Files created**:
  - `{name}.scad` - OpenSCAD file
  - `{name}.svg` - SVG top-down view
  - `{name}_heightmap.dat` - Heightmap (if using surface optimization)
  - `{name}_heightmap_left.dat` and `{name}_heightmap_right.dat` (for separate halves)
- **Example**:
  ```python
  generator = CaseGenerator(layout=layout, name='ergodox')
  generator.export("output_dir")
  # Creates:
  #   output_dir/ergodox.scad
  #   output_dir/ergodox.svg
  #   output_dir/ergodox_heightmap.dat (if using surface optimization)
  ```

## Implementation Details

### SCAD File Generation Updates
- `generate_scad()` now accepts optional `heightmap_filename` parameter
- `_generate_unified_scad()` updated to use custom heightmap filename
- `_generate_separate_halves_scad()` updated to use custom heightmap filenames for left and right
- Surface module generation references the provided heightmap filename

### Backward Compatibility
The old `save()` method remains available but shows a deprecation warning:
```python
warnings.warn("save() is deprecated, use saveScad() instead", DeprecationWarning)
```

For backward compatibility, it automatically saves heightmap files when using surface optimization, maintaining the old behavior.

## Files Changed

### Core Implementation
- `gen_keeb_case/generator.py` - Main implementation

### Examples Updated
- `examples.py` - Updated to use `saveScad()`
- `examples_new_features.py` - Updated to use `saveScad()`
- `examples_optimization.py` - Updated to use `saveScad()` and demonstrate `saveHeightMap()`
- `examples_yaml.py` - Updated to use `saveScad()`
- `examples_export.py` - **NEW** - Demonstrates all new API features

### Tests Updated
- `tests/test_separate_halves.py` - Updated to use `saveScad()`
- `test_new_api.py` - **NEW** - Comprehensive test coverage for all new features
- `test_separate_halves_surface.py` - **NEW** - Tests separate halves with surface optimization

### Other Changes
- `.gitignore` - Added `*.dat` and `examples/exported/` to exclude generated files

## Testing

### Unit Tests
All new functionality has been tested with comprehensive test scripts:
- Name property setting and retrieval
- `saveScad()` with and without heightmap parameter
- `saveHeightMap()` for unified and separate halves
- `export()` for regular and surface optimization cases
- Backward compatibility with deprecated `save()` method
- Separate halves with surface optimization

### Integration Tests
All existing tests pass:
- `tests/test_overlap.py` ✓
- `tests/test_separate_halves.py` ✓
- `tests/test_optimization.py` ✓

### Example Scripts
All example scripts run successfully:
- `examples.py` ✓
- `examples_new_features.py` ✓
- `examples_optimization.py` ✓
- `examples_yaml.py` ✓
- `examples_export.py` ✓

## Security
CodeQL security scan completed with no alerts found.

## Usage Examples

### Basic Export
```python
from gen_keeb_case.generator import KeyboardLayout, CaseGenerator

layout = KeyboardLayout(rows=5, cols=15, switch_type_name="cherry_mx")
generator = CaseGenerator(layout=layout, name="60_percent")
generator.export("output")
# Creates: output/60_percent.scad, output/60_percent.svg
```

### Surface Optimization with Custom Heightmap
```python
layout = KeyboardLayout(rows=5, cols=15, switch_type_name="cherry_mx")
generator = CaseGenerator(
    layout=layout, 
    name="optimized_case",
    optimization_method='surface'
)
generator.export("output")
# Creates: output/optimized_case.scad, output/optimized_case.svg, 
#          output/optimized_case_heightmap.dat
```

### Manual Control
```python
layout = KeyboardLayout(rows=3, cols=10, switch_type_name="cherry_mx")
generator = CaseGenerator(
    layout=layout,
    name="compact",
    optimization_method='surface'
)
generator.saveScad("my_case.scad", "my_custom_heightmap.dat")
generator.save_svg("my_case.svg")
# Creates: my_case.scad (references my_custom_heightmap.dat), 
#          my_custom_heightmap.dat, my_case.svg
```

## Breaking Changes
None. All changes are backward compatible. The old `save()` method still works but shows a deprecation warning.

## Migration Guide

### Old Code
```python
generator = CaseGenerator(layout=layout)
generator.save("output.scad")
generator.save_svg("output.svg")
```

### New Code (Recommended)
```python
generator = CaseGenerator(layout=layout, name="my_keyboard")
generator.export("output_dir")
# Or manually:
generator.saveScad("output.scad")
generator.save_svg("output.svg")
```

## Summary of Problem Statement Requirements

✅ **Add a name to the CaseGenerator class** - Implemented as `name` parameter in `__init__()`

✅ **Add export() method** - Implemented to save scad, svg, and dat files with name prefix

✅ **Add saveHeightMap() function** - Implemented to save heightmap to specific filename

✅ **Change save() to saveScad()** - Implemented with backward compatibility

✅ **Don't automatically save dat in saveScad** - Implemented; only saves when `heightmap_filename` is provided

✅ **Save heightmap if second parameter given** - Implemented; `heightmap_filename` parameter controls this

✅ **Alter SCAD file to use custom filename** - Implemented; SCAD references the provided heightmap filename

All requirements from the problem statement have been successfully implemented and tested.
