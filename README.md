# Theia PNG

![CI](https://github.com/Theia-Scientific/theia-png/actions/workflows/python-package.yml/badge.svg)

A Python package for manipulating PNG files exported or imported using the 
Theia web application.

## Introduction

A Python package for manipulating PNG files exported or imported using the 
Theia web application. These files have data embedded in the PNG, and this 
package unpacks and makes the data readily usable.

## Quick Start

1. Import function to python script.

from extraction import *

2. Use function to extract image data.

extract(PATH_TO_DATA)

## Getting Started

1. Clone this repository.

   ```sh
   git clone https://github.com/Theia-Scientific/theia-png.git && cd theia-png
   ```

## Testing

Testing is divided into unit and integration tests. Unit tests are located in
the package source code tree and are defined on a per-module basis with a
`test_<module>.py` format, while the integration tests are defined in the
`tests` directory.

## License

- [LICENSE](https://github.com/Theia-Scientific/theia-png/blob/main/LICENSE).