# tspng: A Python package for Computer Vision and Machine Learning metadata manipulation

[![CI](https://github.com/Theia-Scientific/theia-png/actions/workflows/ci.yml/badge.svg)](https://github.com/Theia-Scientific/theia-png/actions/workflows/ci.yml)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iC5KLoQUY4D54D9SH4YB2pJ0rTXXq2Fs?usp=sharing)
[![codecov](https://codecov.io/gh/Theia-Scientific/tspng/graph/badge.svg?token=psDVCL46ta)](https://codecov.io/gh/Theia-Scientific/tspng)

A Python package for manipulating Portable Network Graphics (PNG) files with
embedded JavaScript Object Notation (JSON) metadata from Machine Learning (ML)
applications, such as the Theiascope&trade; platform for microscopy image
analysis and quantitation. These files have data embedded in the PNG in a [COCO
JSON format] compatible form. This package provides extraction of the JSON data
and implantation of JSON data into existing PNGs.

## Quick Start

### Library

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

   from tspng.extraction import extract_from_file

   print(json.dumps(extract_from_file("PATH_TO_FILE"), indent=2))
   ```

   where `PATH_TO_FILE` is replaced, in quotes, with the path to a `.ts.png` file on disk.

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

### Application

1. Install the application.

   ```sh
   python3 -m pip install .[cli]
   ```
   
2. Run the application.

   ```sh
   $ tspng extract example.ts.png
   {...}  // Omitted for clarity
   ```

3. (Optional) Use the [jq] utility to obtain specific fields and information
   from the extracted metadata. For example, to pretty print the output:
   
   ```sh
   tspng extract example.ts.png | jq 
   ```

## Contributing

1. Clone this repository.

   ```sh
   git clone https://github.com/Theia-Scientific/tspng && cd tspng
   ```

2. Create a virtual environment.

   ```sh
   python3 -m venv .venv
   ```

3. Activate the virtual environment.

   ```sh
   source .venv/bin/activate
   ```

4. Upgrade `pip`.

   ```sh
   python3 -m pip install --upgrade pip
   ```
   
5. Install all the dependencies.

   ```sh
   python3 -m pip install -e .[dev,cli]
   ```

6. Create a local branch.

   ```sh
   git checkout -b feature-awesome-new-feature
   ```

7. Modify the code.
8. Run the tests.

   ```sh
   pytest --color=yes
   ```

9. Commit changes to your local branch.

   ```sh
   git add -A && git commit -m "Add new feature"
   ```

10. Push your local branch to GitHub to create a Pull Request (PR).

   ```sh
   git push origin feature-awesome-new-feature
   ```

11. Create a Pull Request (PR) in GitHub.
12. Wait for CI to complete.
13. Add comment to PR that it is ready to review.

## License

- [LICENSE](https://github.com/Theia-Scientific/tspng/blob/main/LICENSE).

## Acknowledgments

This material is based upon work supported by the U.S. Department of Energy,
Office of Nuclear Energy under Award Number DE-SC0021529.

[coco json format]: https://cocodataset.org/#format-data
[jq]: https://jqlang.github.io/jq/
