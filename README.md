# Image Type Converting & Mask Generation

This project converts and processes image data with geospatial annotations to generate segmentation masks for machine learning applications.

## Overview

We use QGIS to label image data and export annotations as `.geojson` files. These annotations are then processed to generate corresponding mask images with different pixel values for each category.

## Directory Structure

```
data-set(b)/
├── annotations/          # Individual category annotations
│   ├── building/        # Building annotations (b_001.geojson - b_010.geojson)
│   ├── road/            # Road annotations (r_001.geojson - r_010.geojson)
│   ├── sport/           # Sport facility annotations (s_001.geojson - s_010.geojson)
│   ├── vege/            # Vegetation annotations (v_001.geojson - v_010.geojson)
│   └── water/           # Water body annotations (w_001.geojson - w_010.geojson)
├── combined_annotations/ # Combined annotations (generated)
│   └── 001.geojson - 010.geojson  # All categories merged per image
├── masks/               # Individual category masks (generated)
│   ├── building/
│   ├── road/
│   ├── sport/
│   ├── vege/
│   └── water/
├── combined_masks/      # Multi-class masks (generated)
│   └── 001.png - 010.png         # All categories in one mask
└── image/               # Source images
```

## Workflow

### Step 1: Label Images with QGIS
1. Open raw images from the `data-set(b)/image/` directory in QGIS
2. Create polygon annotations for each category:
   - Building structures
   - Roads and pathways
   - Sport facilities
   - Vegetation areas
   - Water bodies
3. Export annotations as `.geojson` files
4. Place the `.geojson` files in the appropriate subdirectory under `data-set(b)/annotations/`
   - Use naming convention: `{prefix}_{number}.geojson` (e.g., `b_001.geojson`, `r_001.geojson`)

### Step 2: Combine Annotations (Optional but Recommended)
Merge all category annotations into single files per image:
```bash
python combine_annotations.py
```

The script will:
- Read all annotations from the 5 categories (building, road, sport, vege, water)
- Combine annotations with the same image number into single geojson files
- Add `category` property to each feature for identification
- Save combined files to `data-set(b)/combined_annotations/`
- Output: `001.geojson` through `010.geojson`

### Step 3: Generate Masks
Run the mask generation script:
```bash
python generate_masks.py
```

The script will:
- **Process individual category annotations:**
  - Convert each geojson to a grayscale mask (pixel value = 123)
  - Save to `data-set(b)/masks/{category}/` preserving the subdirectory structure
  
- **Process combined annotations:**
  - Convert each combined geojson to a multi-class mask
  - Assign different pixel values per category:
    - Building: 51 (dark gray)
    - Road: 102
    - Sport: 153 (mid gray)
    - Vege: 204
    - Water: 255 (white/brightest)
  - Save to `data-set(b)/combined_masks/`

- Generate 1024x1024 pixel PNG masks
- Automatically flip Y coordinates to correct QGIS coordinate system

## Dataset Statistics

- **Total Images:** 10 (001-010)
- **Categories:** 5 (building, road, sport, vegetation, water)
- **Annotation Files:** 50 (10 images × 5 categories)
- **Mask Resolution:** 1024×1024 pixels
- **File Format:** GeoJSON for annotations, PNG for masks

## Mask Color Values

### Individual Category Masks
- Feature pixels: 123 (gray)
- Background: 0 (black)

### Combined Multi-class Masks
- Background: 0 (black)
- Building: 51
- Road: 102
- Sport: 153
- Vegetation: 204
- Water: 255

To modify these values, edit the `CATEGORY_VALUES` dictionary in [generate_masks.py](generate_masks.py).

## Notes

- Masks are automatically flipped to correct Y-coordinate system from QGIS exports
- All masks are generated at 1024×1024 resolution
- Combined masks allow for multi-class semantic segmentation training
- Individual masks can be used for single-class or binary segmentation tasks
