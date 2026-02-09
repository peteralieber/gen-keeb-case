"""
Image detection module for detecting keyboard layouts from top-down images.
"""

import cv2
import numpy as np


class KeyboardImageDetector:
    """Detects keyboard key positions from a top-down image."""
    
    def __init__(self, image_path, switch_type_name="cherry_mx", key_spacing=19.05):
        """
        Initialize the keyboard image detector.
        
        Args:
            image_path: Path to the top-down keyboard image
            switch_type_name: Type of mechanical switch (default: cherry_mx)
            key_spacing: Expected spacing between keys in mm (default: 19.05mm)
        """
        self.image_path = image_path
        self.switch_type_name = switch_type_name
        self.key_spacing = key_spacing
        self.image = None
        self.gray = None
        self.keys = []
        
    def load_image(self):
        """Load and preprocess the image."""
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"Could not load image from {self.image_path}")
        
        # Convert to grayscale
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
    def detect_keys(self, min_area=100, max_area=10000, aspect_ratio_range=(0.7, 1.3)):
        """
        Detect key positions from the image.
        
        Args:
            min_area: Minimum contour area to consider as a key
            max_area: Maximum contour area to consider as a key
            aspect_ratio_range: Tuple of (min, max) aspect ratio for key detection
            
        Returns:
            list: List of detected keys with positions and rotations
        """
        if self.gray is None:
            self.load_image()
        
        # Apply adaptive thresholding to handle varying lighting
        thresh = cv2.adaptiveThreshold(
            self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Apply morphological operations to clean up the image
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_keys = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < min_area or area > max_area:
                continue
            
            # Get the minimum area rectangle (handles rotation)
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
            
            # Ensure width > height for consistent angle calculation
            if w < h:
                w, h = h, w
                angle = angle + 90
            
            # Filter by aspect ratio (keys are roughly square)
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio < aspect_ratio_range[0] or aspect_ratio > aspect_ratio_range[1]:
                continue
            
            # Normalize angle to [-45, 45] range
            if angle > 45:
                angle = angle - 90
            elif angle < -45:
                angle = angle + 90
            
            detected_keys.append({
                'x': float(x),
                'y': float(y),
                'width': float(w),
                'height': float(h),
                'rotation': float(angle)
            })
        
        self.keys = detected_keys
        return detected_keys
    
    def convert_to_mm(self, reference_spacing_px=None):
        """
        Convert pixel coordinates to millimeters.
        
        Args:
            reference_spacing_px: Known spacing between keys in pixels.
                                 If None, will attempt to estimate from detected keys.
                                 
        Returns:
            list: Keys with coordinates in millimeters
        """
        if not self.keys:
            raise ValueError("No keys detected. Run detect_keys() first.")
        
        # If no reference spacing provided, estimate it
        if reference_spacing_px is None:
            reference_spacing_px = self._estimate_key_spacing()
        
        # Calculate scale factor (mm per pixel)
        scale = self.key_spacing / reference_spacing_px if reference_spacing_px > 0 else 1.0
        
        # Convert all coordinates to mm
        keys_mm = []
        for key in self.keys:
            keys_mm.append({
                'x': key['x'] * scale,
                'y': key['y'] * scale,
                'rotation': key['rotation']  # Rotation stays the same
            })
        
        return keys_mm
    
    def _estimate_key_spacing(self):
        """
        Estimate the spacing between keys in pixels.
        
        Returns:
            float: Estimated spacing in pixels
        """
        if len(self.keys) < 2:
            # Cannot estimate with less than 2 keys
            return 1.0
        
        # Sort keys by y-coordinate, then x-coordinate
        sorted_keys = sorted(self.keys, key=lambda k: (k['y'], k['x']))
        
        # Find minimum horizontal distance between consecutive keys in same row
        min_spacing = float('inf')
        for i in range(len(sorted_keys) - 1):
            k1 = sorted_keys[i]
            k2 = sorted_keys[i + 1]
            
            # Check if keys are in roughly the same row (similar y-coordinate)
            y_diff = abs(k1['y'] - k2['y'])
            if y_diff < 30:  # Threshold for same row
                x_diff = abs(k1['x'] - k2['x'])
                if x_diff > 10 and x_diff < min_spacing:  # Must have some separation
                    min_spacing = x_diff
        
        # If no horizontal spacing found, try vertical spacing
        if min_spacing == float('inf'):
            for i in range(len(sorted_keys) - 1):
                k1 = sorted_keys[i]
                k2 = sorted_keys[i + 1]
                y_diff = abs(k1['y'] - k2['y'])
                if y_diff > 10 and y_diff < min_spacing:
                    min_spacing = y_diff
        
        return min_spacing if min_spacing != float('inf') else 1.0
    
    def normalize_positions(self, keys_mm):
        """
        Normalize key positions so the minimum x,y is at (0, 0).
        
        Args:
            keys_mm: List of keys with positions in mm
            
        Returns:
            list: Keys with normalized positions
        """
        if not keys_mm:
            return []
        
        min_x = min(key['x'] for key in keys_mm)
        min_y = min(key['y'] for key in keys_mm)
        
        normalized_keys = []
        for key in keys_mm:
            normalized_keys.append({
                'x': key['x'] - min_x,
                'y': key['y'] - min_y,
                'rotation': key['rotation']
            })
        
        return normalized_keys
    
    def detect_grid_layout(self, keys_mm, tolerance=2.0):
        """
        Attempt to detect if keys form a regular grid pattern.
        
        Args:
            keys_mm: List of keys with positions in mm
            tolerance: Tolerance in mm for grid alignment
            
        Returns:
            dict or None: Grid info with rows/cols if detected, None otherwise
        """
        if len(keys_mm) < 4:
            return None
        
        # Round positions to nearest grid point
        rounded_keys = []
        for key in keys_mm:
            rounded_x = round(key['x'] / self.key_spacing) * self.key_spacing
            rounded_y = round(key['y'] / self.key_spacing) * self.key_spacing
            
            # Check if key is close to grid point
            if abs(key['x'] - rounded_x) < tolerance and abs(key['y'] - rounded_y) < tolerance:
                rounded_keys.append({
                    'grid_x': int(round(key['x'] / self.key_spacing)),
                    'grid_y': int(round(key['y'] / self.key_spacing)),
                    'rotation': key['rotation']
                })
        
        # If most keys fit the grid (>80%), consider it a grid layout
        if len(rounded_keys) / len(keys_mm) < 0.8:
            return None
        
        # Check if all keys have 0 rotation (or very close to 0)
        if not all(abs(key['rotation']) < 5 for key in keys_mm):
            return None
        
        # Calculate grid dimensions
        grid_cols = len(set(key['grid_x'] for key in rounded_keys))
        grid_rows = len(set(key['grid_y'] for key in rounded_keys))
        
        # Verify we have the right number of keys for a complete grid
        if len(rounded_keys) == grid_rows * grid_cols:
            return {
                'rows': grid_rows,
                'cols': grid_cols
            }
        
        return None
    
    def create_layout_dict(self, reference_spacing_px=None):
        """
        Create a complete layout dictionary from the detected keys.
        
        Args:
            reference_spacing_px: Known spacing between keys in pixels
            
        Returns:
            dict: Layout dictionary compatible with KeyboardLayout.from_dict()
        """
        if not self.keys:
            self.detect_keys()
        
        # Convert to mm and normalize
        keys_mm = self.convert_to_mm(reference_spacing_px)
        keys_normalized = self.normalize_positions(keys_mm)
        
        # Try to detect grid layout
        grid_info = self.detect_grid_layout(keys_normalized)
        
        layout_dict = {
            'switch_type': self.switch_type_name,
            'key_spacing': self.key_spacing,
            'keys': keys_normalized
        }
        
        if grid_info:
            layout_dict['grid'] = grid_info
        
        return layout_dict
    
    def visualize_detection(self, output_path=None):
        """
        Visualize the detected keys on the original image.
        
        Args:
            output_path: Path to save the visualization. If None, displays interactively.
        """
        if self.image is None:
            self.load_image()
        
        if not self.keys:
            self.detect_keys()
        
        # Create a copy for visualization
        vis_image = self.image.copy()
        
        # Draw detected keys
        for key in self.keys:
            # Get rotated rectangle
            rect = ((key['x'], key['y']), (key['width'], key['height']), key['rotation'])
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            
            # Draw rectangle
            cv2.drawContours(vis_image, [box], 0, (0, 255, 0), 2)
            
            # Draw center point
            center = (int(key['x']), int(key['y']))
            cv2.circle(vis_image, center, 3, (0, 0, 255), -1)
        
        # Add text with number of keys detected
        text = f"Detected {len(self.keys)} keys"
        cv2.putText(vis_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 255, 0), 2)
        
        if output_path:
            cv2.imwrite(output_path, vis_image)
            print(f"Visualization saved to {output_path}")
        else:
            cv2.imshow("Detected Keys", vis_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def detect_keyboard_from_image(image_path, switch_type_name="cherry_mx", 
                               key_spacing=19.05, reference_spacing_px=None,
                               visualize=False, output_vis_path=None):
    """
    High-level function to detect keyboard layout from an image.
    
    Args:
        image_path: Path to the keyboard image
        switch_type_name: Type of mechanical switch
        key_spacing: Expected spacing between keys in mm
        reference_spacing_px: Known spacing between keys in pixels
        visualize: Whether to visualize the detection
        output_vis_path: Path to save visualization
        
    Returns:
        dict: Layout dictionary compatible with KeyboardLayout.from_dict()
    """
    detector = KeyboardImageDetector(image_path, switch_type_name, key_spacing)
    layout_dict = detector.create_layout_dict(reference_spacing_px)
    
    if visualize:
        detector.visualize_detection(output_vis_path)
    
    return layout_dict
