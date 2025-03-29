# Marker GUI Wrapper 

Marker GUI Wrapper is a GUI based on PyQt5, serving as a wrapper for the [marker](https://github.com/vikparuchuri/marker) project. `marker` is a powerful document processing tool that supports extracting and converting content from various formats such as PDFs, images, and Office documents.

## Installation

1. Ensure Python 3 and the `marker_single` tool are installed.
   ```bash
   pip install marker-pdf
   ```

2. Install PyQt5:
   ```bash
   pip install PyQt5
   ```

3. Clone or download this project locally:
   ```bash
   git clone https://github.com/your-repo/marker-gui-wrapper.git
   cd marker-gui-wrapper
   ```

## Usage

1. Run the GUI:
   ```bash
   python marker-tools.py
   ```

2. In the interface:
   - Click the **Browse...** button to select the input file and output directory.
   - Configure the required options (e.g., output format, LLM settings, etc.).
   - Click the **Convert** button to start the conversion.

3. Once the conversion is complete, the output files will be saved in the specified output directory.

## Contribution

Feel free to submit issues and feature requests! You can contribute via GitHub by submitting Pull Requests or Issues.

## License

This project is open-sourced under the [MIT License](LICENSE).