# tspng: A Python package for Computer Vision and Machine Learning metadata manipulation

[![CI](https://github.com/Theia-Scientific/theia-png/actions/workflows/ci.yml/badge.svg)](https://github.com/Theia-Scientific/theia-png/actions/workflows/ci.yml)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iC5KLoQUY4D54D9SH4YB2pJ0rTXXq2Fs?usp=sharing)
[![codecov](https://codecov.io/gh/Theia-Scientific/tspng/graph/badge.svg?token=psDVCL46ta)](https://codecov.io/gh/Theia-Scientific/tspng)

A Python package for manipulating Portable Network Graphics (PNG) files with
embedded [JavaScript Object Notation] (JSON) metadata from Machine Learning (ML)
applications, such as the TS platform for microscopy image analysis and
quantitation. These files have data embedded in the PNG in JSON or as plain
text. This package provides extraction of the embedded data and implantation of
embedded data into existing PNGs.

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

4. Create a `png_dump.py` script to extract embedded data from a PNG file,

   ```python
   from tspng.extraction import extract_from_file

   print(extract_from_file("PATH_TO_FILE").model_dump_json(exclude_none=True, indent=2))
   ```

   where `PATH_TO_FILE` is replaced, in quotes, with the path to a `.ts.png` file on disk.

5. Run the `png_dump.py` script,

   ```sh
   $ python3 ./png_dump.py
   {
     // ...  omitted for clarity
   }
   ```

   where the contents of the PNG metadata will be printed to STDOUT as JSON. The
   actual contents are omitted for clarity. The [jq] application can also be
   used to query and filter the output.

6. Alternatively, data can be implanted into an existing PNG.

   ```python
   from tspng.implantation import implant

   implant("Path/to/file.json", "Path/to/existing.png", "Path/to/new.png")
   ```

7. Creating Metadata for use in other components is also possible with the schema API.

   ```python
   from tspng.schema.data import Meta as Metadata

   print(Metadata(embedded=[Embedded(data="Hello, World!", mime_type="text/plain")]).model_dump_json(ident=2))
   ```

### Application

1. Install the application.

   ```sh
   python3 -m pip install ".[cli]"
   ```
   
2. Run the application.

   ```sh
   $ tspng extract example.ts.png
   {...}  // Omitted for clarity
   ```

3. (Optional) Use the [jq] utility to obtain specific fields and information
   from the extracted metadata. For example, to pretty print the output:
   
   ```sh
   tspng extract example.ts.png | jq .
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
   python3 -m pip install -e ".[dev,cli]"
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
[javascript object notation]: https://www.json.org/json-en.html
[jq]: https://jqlang.github.io/jq/
