# Theia PNG

[![CI](https://github.com/Theia-Scientific/theia-png/actions/workflows/python-package.yml/badge.svg)](https://github.com/Theia-Scientific/theia-png/actions/workflows/python-package.yml)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iC5KLoQUY4D54D9SH4YB2pJ0rTXXq2Fs?usp=sharing)

A Python package for manipulating PNG files exported or imported using the 
Theia web application. These files have data embedded in the PNG in a [COCO JSON format] compatible form. This package unpacks and makes the data readily usable.

## Quick Start

1. Create a virtual environment.

   ```sh
   python3 -m venv .venv
   ```

2. Activate the virtual environment.

   ```sh
   source .venv/bin/activate
   ```

3. Install tspng.

   ```sh
   python3 -m pip install tspng
   ```

4. Create a `png_dump.py` script to extract inference results from a PNG file,

   ```python
   import json

   from tspng.extraction import extract

   print(json.dumps(extract(PATH_TO_FILE), indent=2))
   ```

   where `PATH_TO_FILE` is replaced with the path to a `.ts.png` file on disk.

5. Run the `png_dump.py` script.

   ```sh
   $ python3 ./png_dump.py
   {
   "info": {
      "description": "Theiascope image",
      "url": "http://www.theiascientific.com",
      "version": "1.0",
      "year": 2023,
      "contributor": "Theia Scientific, LLC",
      "date_created": "2023-05-10 19:22:47.722802+00:00"
   },
   "licenses": {
      "url": "http://www.theiascientific.com",
      "id": 1,
      "name": "Proprietary"
   },
   "images": [
      {
         "license": 1,
         "file_name": "20230510T192247Z.722_crimson-notebook (PML).ts.png",
         "height": 512,
         "width": 512,
         "date_captured": "2023-05-10 19:22:47.722802+00:00",
         "id": 3783,
         "field_of_view": [
         0,
         0,
         512,
         512
         ],
         "scale_bar": {
         "dimensions": [
            25,
            501,
            128,
            1
         ],
         "length": 100.0,
         "units_abbr": "nm",
         "units_name": "nanometers"
         }
      }
   ],
   "annotations": [...],  // Omitted for clarity
   "models": [
      {
         "id": 17,
         "configuration": {
         "image_processing": {
            "brightness": 0,
            "clahe": false,
            "contrast": 1.0,
            "gamma": 1.0,
            "gray": false,
            "invert": false
         },
         "max_concurrency": 2,
         "num_cpus": 0,
         "num_gpus": 1.0,
         "box_nms_thresh": 0.7,
         "crop_n_layers": 0,
         "crop_nms_thresh": 0.7,
         "crop_overlap_ratio": 0.3413333333333333,
         "crop_n_points_downscale_factor": 1,
         "min_mask_region_area": 0,
         "points_per_side": 32,
         "points_per_batch": 64,
         "pred_iou_thresh": 0.88,
         "stability_score_thresh": 0.95,
         "stability_score_offset": 1.0,
         "weights_file": {
            "filename": "sam_vit_b_01ec64.pth",
            "version": "default",
            "path": "/sam/vit-b"
         }
         },
         "created": "2023-05-09 19:46:18.309323+00:00",
         "family": "SAM",
         "name": "vit-b",
         "pid": 1
      }
   ],
   "categories": [
      {
         "supercategory": "defect",
         "id": 1,
         "name": ""
      }
   ]
   }
   ```

## Contributing

1. Create a virtual environment.

   ```sh
   python3 -m venv .venv
   ```

2. Activate the virtual environment.

   ```sh
   source .venv/bin/activate
   ```

3. Clone this repository.

   ```sh
   git clone https://github.com/Theia-Scientific/theia-png.git && cd theia-png
   ```

4. Install the dependencies.

   ```sh
   python3 -m pip install .[dev]
   ```

5. Build the package.

   ```sh
   python3 -m build
   ```

## Testing

Testing is divided into unit and integration tests. Unit tests are located in
the package source code tree and are defined on a per-module basis with a
`test_<module>.py` format, while the integration tests are defined in the
`tests` directory.

## License

- [LICENSE](https://github.com/Theia-Scientific/theia-png/blob/main/LICENSE).

## Acknowledgments

This material is based upon work supported by the U.S. Department of Energy, Office of Nuclear Energy under Award Number DE-SC0021529.

[coco json format]: https://cocodataset.org/#format-data