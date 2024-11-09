# JMAGroundDataDownloader

The `JMAGroundDataDownloader` is a Python class designed for downloading and processing ground data from the Japan Meteorological Agency (JMA). This tool fetches meteorological data based on specified stations and dates, supporting both hourly and daily formats. It also translates variable headers from Japanese to English, making data analysis more accessible.

## Table of Contents

- [Installation](##installation)
- [Usage](#usage)
- [Class Structure](##class-structure)
- [Data Variable Mappings](##data-variable-mappings)
- [Methods Overview](##methods-overview)
- [License](##license)

## Installation

To get started, clone the repository and install the required dependencies:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/JMAGroundDataDownloader.git
   cd JMAGroundDataDownloader
   ```

2. Install the necessary Python libraries:

   ```bash
   pip install pandas requests beautifulsoup4 numpy
   ```

## Usage

1. **Prepare AMEDAS Station File**: Ensure you have an `Amedas_list.csv` file with the necessary station details (station ID, location, etc.).

2. **Initialize and Use the Downloader**:

   ```python
   from JMAGroundDataDownloader import JMAGroundDataDownloader
   from datetime import datetime

   # Initialize the downloader
   downloader = JMAGroundDataDownloader(amedas_file='Amedas_list.csv', output_path='grounddata_download')

   # Download data for a specific station and date
   station_id = 12345  # Example station ID
   date = datetime(2023, 8, 1)
   data, url = downloader.download_amedas(point=station_id, date=date, dtype='hourly')
   ```

3. **Output Files**: Downloaded data is saved as CSV files in the specified `output_path`, organized by station and date.

## Class Structure

### Constructor Parameters

- **`amedas_file`** (`str`): Path to the AMEDAS station information CSV file.
- **`output_path`** (`str`): Directory to save the downloaded data files.

### Data Types

The downloader supports both hourly and daily data, with variable names translated from Japanese to English. 

## Data Variable Mappings

The `vard` dictionary within the class maps Japanese weather variable names to English equivalents. Here are a few examples:

- **Hourly Data**:
  - 気温(℃) ➞ `temp_C`
  - 降水量(mm) ➞ `precip_mm`
  - 日照時間(h) ➞ `sunlit_h`

- **Daily Data**:
  - 合計(mm)_降水量 ➞ `precip-accum_mm`
  - 平均(℃)_気温 ➞ `temp_C`
  - 日照時間(h) ➞ `sunlit_h`

Refer to the `vard` dictionary in the code for the full list of mappings.

## Methods Overview

- **`download_amedas(point, date, dtype)`**: Fetches and processes data for a specified station and date.
  - **`point`** (`int`): Station ID.
  - **`date`** (`datetime`): Date for the requested data.
  - **`dtype`** (`str`): Data type, either `'hourly'` or `'daily'`.

- **`get_info(h, att)`**: Retrieves the value of the specified attribute from an HTML element, if available.
- **`rep_text(text)`**: Cleans up specific characters in text, like removing special characters.
- **`rep_text_wdir(text)`**: Converts Japanese compass directions to English abbreviations (e.g., 東 to E).
- **`compass2angle(com)`**: Translates compass directions into angles (e.g., NNE to 22.5°).

### Example Workflow

1. **Download Data**: Use `download_amedas()` to download and save hourly or daily data.
2. **Data Processing**: Headers are translated from Japanese to English, and data is cleaned up for analysis.
3. **Data Saving**: Data is saved in a standardized CSV format, organized in folders by station and date.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

This `README.md` covers the key details, installation, usage instructions, and functionality of the `JMAGroundDataDownloader` class. Adjust any URLs or file names as necessary to match your repository structure!
