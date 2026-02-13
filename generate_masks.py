import json
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm

TILE_SIZE = 1024
BUILDING_VALUE = 123   # grey building
BACKGROUND_VALUE = 0   # black background

annotations_dir = Path("data-set(b)/annotations")
masks_dir = Path("data-set(b)/masks")

def flip_y_if_negative(coords):
    new_coords = []
    for x, y in coords:
        # Convert negative Y coordinates to positive (flip vertically)
        new_coords.append([x, abs(y)])
    return new_coords

# Recursively find all geojson files in subdirectories
for geojson_file in tqdm(list(annotations_dir.glob("**/*.geojson"))):

    with open(geojson_file) as f:
        data = json.load(f)

    mask = np.full((TILE_SIZE, TILE_SIZE), BACKGROUND_VALUE, dtype=np.uint8)

    for feature in data["features"]:
        geom = feature["geometry"]

        if geom["type"] != "Polygon":
            continue

        polygon = geom["coordinates"][0]

        polygon = flip_y_if_negative(polygon)

        pts = np.array(polygon, np.int32)
        pts = pts.reshape((-1,1,2))

        cv2.fillPoly(mask, [pts], BUILDING_VALUE)

    # Preserve subdirectory structure in masks
    relative_path = geojson_file.relative_to(annotations_dir)
    out_path = masks_dir / relative_path.parent / (geojson_file.stem + ".png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), mask)