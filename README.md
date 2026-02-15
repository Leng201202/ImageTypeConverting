# Image Type Converting & Mask Generation

This project converts and processes image data with annotations to generate binary masks for machine learning applications.

## Overview

We use QGIS to label image data and export annotations as `.geojson` files. These annotations are then processed to generate corresponding mask images.

## Directory Structure

```
data-set(b)/
├── annotations/
│   ├── b/          # Building annotations
│   ├── r/          # Road annotations
│   └── v/          # Vegetation annotations
└── masks/          # Generated masks (created automatically)
    ├── b/
    ├── r/
    └── v/
raw/                # Raw TIFF images
```

## Workflow

### Step 1: Label Images with QGIS
1. Open raw images from the `raw/` directory in QGIS
2. Create polygon annotations for your features
3. Export annotations as `.geojson` files
4. Place the `.geojson` files in the appropriate subdirectory under `data-set(b)/annotations/`
   - `building/` for buildings
   - `road/` for roads
   - `vege/` for vegetation

### Step 2: Generate Masks
Run the mask generation script:
```bash
python generate_masks.py
```

The script will:
- Recursively process all `.geojson` files in `data-set(b)/annotations/`
- Convert polygon annotations to binary masks (building pixels = 123, background = 0)
- Save masks to `data-set(b)/masks/{category}/{filename}.png` preserving the subdirectory structure
  - Example: `annotations/building/b_001.geojson` → `masks/building/b_001.png`
  - Example: `annotations/road/r_001.geojson` → `masks/road/r_001.png`
- Generate 1024x1024 pixel PNG masks

### Step 3: Convert Images (Optional)
Convert TIFF images to PNG format:
```bash
python convert.py
```

## Notes

- Currently working on labeling 48 images from the raw dataset
- Masks are automatically flipped to correct coordinate system from QGIS exports
- All masks are generated at 1024x1024 resolution
