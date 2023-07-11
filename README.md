# Theia PNG

![CI](https://github.com/Theia-Scientific/theia-png/actions/workflows/python-package.yml/badge.svg)

A Python package for manipulating PNG files exported or imported using the 
Theia web application. These files have data embedded in the PNG, and this 
package unpacks and makes the data readily usable.

## Contributing

1. Clone this repository.

   ```sh
   git clone https://github.com/Theia-Scientific/theia-png.git && cd theia-png
   ```

2. Install the dependencies.

   ```sh
   python3 -m pip install .[dev]
   ```

3. Build the package.

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