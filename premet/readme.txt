# XML Processor for Error Removal

This script processes XML files based on errors identified in a CSV file. It removes specific sections of the XML files according to the `FULL CODE` values associated with errors.

## Features
- Reads errors from a CSV file and filters rows where both `Result` and `Category` are set to `Error`.
- Extracts `FULL CODE` values from the error descriptions.
- Processes XML files, removing relevant sections based on `Object name` (e.g., `MER-Operator` or `MER-Reader`).
- Supports multiple XML files and associates each with specific error data.

## Prerequisites
- Python 3.6 or higher
- Libraries: `pandas`, `re`, and `xml.etree.ElementTree` (built-in)

## Installation
1. Clone or download this repository.
2. Install required libraries:
   ```bash
   pip install pandas
