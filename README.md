# File Lister

This script scans a directory for files, optionally excluding specific directories and file extensions, and saves the list to a text file.

## Features

- Scan directories recursively
- Exclude specific directories and file extensions
- Save results to a text file
- Verbose mode to include file sizes
- Option to sort files by size

## Usage

```
python true.py [-h] [-o OUTPUT] [--exclude-dirs [EXCLUDE_DIRS ...]]
                [--exclude-extensions [EXCLUDE_EXTENSIONS ...]] [-v] [-s]
                directory
```

### Arguments

- `directory`: Directory to scan for files
- `-o OUTPUT, --output OUTPUT`: Output file name (default: files_to_add.txt)
- `--exclude-dirs [EXCLUDE_DIRS ...]`: Directories to exclude
- `--exclude-extensions [EXCLUDE_EXTENSIONS ...]`: File extensions to exclude
- `-v, --verbose`: Enable verbose output (includes file sizes)
- `-s, --sort-by-size`: Sort files by size (largest first)

### Examples

1. Basic usage:
   ```
   python true.py /path/to/directory
   ```

2. Exclude specific directories and file extensions:
   ```
   python true.py /path/to/directory --exclude-dirs .git __pycache__ --exclude-extensions .pyc .tmp
   ```

3. Use verbose mode and sort by size:
   ```
   python true.py /path/to/directory -v -s
   ```

4. Specify custom output file:
   ```
   python true.py /path/to/directory -o my_file_list.txt
   ```

## Requirements

- Python 3.6+

## License

This project is open source and available under the [MIT License](LICENSE).
# AI Builder for Cities of Lights

Welcome to the AI Builder for Cities of Lights, an innovative project aimed at creating 3D assets for the harbor of AI in the Metaverse.

## About the Project

The AI Builder is an autonomous system designed to generate and manipulate 3D assets for the Cities of Lights. Our goal is to create a vibrant, immersive environment in the Metaverse, populated with a wide variety of 3D elements including:

- Buildings and architectural structures
- Avatars and characters
- Environmental elements (trees, plants, water features)
- Vehicles and transportation systems
- Urban furniture and decorative elements

## Features

- Autonomous generation of 3D assets
- Texture transformation and manipulation
- GLB file processing and optimization
- Scaling and exaggeration of 3D geometries
- UV coordinate manipulation for enhanced texturing

## How It Works

The AI Builder uses advanced algorithms and machine learning techniques to:

1. Analyze requirements for new 3D assets
2. Generate or modify 3D models based on specified parameters
3. Apply texture transformations and optimizations
4. Process and output GLB files ready for use in the Metaverse

## Getting Started

To use the AI Builder, follow these steps:

1. Clone this repository
2. Install the required dependencies (listed in `requirements.txt`)
3. Run the main script with your input GLB file:

   ```
   python main.py <input_file.glb> <output_file.glb>
   ```

4. The processed 3D asset will be saved as the specified output file

## Contributing

We welcome contributions from the community! If you have ideas for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or feedback, please open an issue in this repository or contact the project maintainers.

Join us in building the Cities of Lights - the future of AI in the Metaverse!
