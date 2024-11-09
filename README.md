# JMA Weather Data Library

This library provides tools to download, process, and visualize meteorological data from the Japan Meteorological Agency (JMA). It contains several classes for handling different types of weather data, including AMEDAS ground data, upper air data, and data plotting. This tutorial covers all classes available in the library.

## Table of Contents

- [Installation](#installation)
- [Classes Overview](#classes-overview)
  - [JMAGroundDataDownloader](#jmagrounddatadownloader)
  - [JMAUpperAirDownloader](#jmaupperairdownloader)
  - [JMADataPlotter](#jmadataplotter)
  - [AmedasData](#amedasdata)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Installation

To use this library, clone the repository and install the required dependencies:

1. Clone the repository:

   ```bash
   git clone https://github.com/doan-van/download_JMA_AMeDAS_data.git
   ```

2. Install the necessary Python libraries:

   ```bash
   pip install pandas requests beautifulsoup4 numpy matplotlib
   ```
   
3. Install:

   ```bash
   cd download_JMA_AMeDAS_data
   pip install .
   ```
## Classes Overview

### JMAGroundDataDownloader

The `JMAGroundDataDownloader` class is designed to download ground meteorological data from JMA's Automated Meteorological Data Acquisition System (AMEDAS). It supports both hourly and daily data downloads, which are translated from Japanese to English to facilitate analysis.

#### Key Features:
- Downloads hourly and daily AMEDAS data.
- Handles data conversion (e.g., compass directions to angles).
- Saves downloaded data as CSV files.

#### Constructor Parameters:

- **`output_path`** (`str`): Directory to save downloaded data.

#### Example Usage:
```python
from JMAGroundDataDownloader import JMAGroundDataDownloader
from datetime import datetime

# Initialize the downloader
downloader = JMAGroundDataDownloader(amedas_file='Amedas_list.csv', output_path='grounddata_download')

# Download hourly data for a specific station and date
data, url = downloader.download_amedas(point=12345, date=datetime(2023, 8, 1), dtype='hourly')
```

### JMAUpperAirDownloader

The `JMAUpperAirDownloader` class is used to download upper air data (sounding data) from JMA. It provides detailed meteorological information such as pressure, temperature, wind speed, and wind direction.

#### Key Features:
- Downloads sounding data from various upper air observation stations.
- Processes data for temperature, humidity, and wind speed at different pressure levels.

#### Constructor Parameters:
- **`output_path`** (`str`): Directory to save downloaded data.

#### Example Usage:
```python
from JMAUpperAirDownloader import JMAUpperAirDownloader
import pandas as pd

# Initialize the downloader
downloader = JMAUpperAirDownloader(output_path='upperair_download')

# Download upper air data for a specific station and date
data = downloader.download_sounding_data(point='47646', date=pd.Timestamp('2023-06-01 09:00'))
```

### JMADataPlotter

The `JMADataPlotter` class provides methods to visualize meteorological data, including sounding profiles, wind data, and temperature distributions.

#### Key Features:
- Plots upper air sounding data (e.g., Skew-T diagrams).
- Visualizes temperature and wind profiles.

#### Example Usage:
```python
from JMADataPlotter import JMADataPlotter

# Initialize the plotter
plotter = JMADataPlotter()

# Plot sounding data
plotter.plot_sounding(data)
```

### AmedasData

The `AmedasData` class provides tools to handle AMEDAS data, such as data loading, filtering, and processing. It helps in reading existing AMEDAS datasets and performing operations like calculating averages, extracting specific columns, or merging multiple datasets.

#### Key Features:
- Reads and processes AMEDAS data files.
- Supports data filtering and aggregation.

#### Example Usage:
```python
from amedas_data_class import AmedasData

# Initialize and load data
amedas = AmedasData(file_path='grounddata_download/hourly/12345/2023_08_01.csv')

# Process and analyze data
amedas.filter_data_by_date(start_date='2023-08-01', end_date='2023-08-31')
```

## Usage

1. **Download Ground Data**: Use the `JMAGroundDataDownloader` class to download AMEDAS data for specified stations and time periods.
2. **Download Upper Air Data**: Use the `JMAUpperAirDownloader` to get sounding data from upper air observation stations.
3. **Visualize Data**: Plot the downloaded data using the `JMADataPlotter` class.
4. **Process Existing Data**: Use `AmedasData` for reading and processing downloaded AMEDAS data.

## Examples

### Example 1: Download and Plot Sounding Data
```python
from JMAUpperAirDownloader import JMAUpperAirDownloader
from JMADataPlotter import JMADataPlotter
import pandas as pd

# Initialize downloader and plotter
downloader = JMAUpperAirDownloader(output_path='upperair_download')
plotter = JMADataPlotter()

# Download sounding data
data = downloader.download_sounding_data(point='47646', date=pd.Timestamp('2023-06-01 09:00'))

# Plot the sounding data
plotter.plot_sounding(data)
```

### Example 2: Download and Analyze AMEDAS Data
```python
from JMAGroundDataDownloader import JMAGroundDataDownloader
from amedas_data_class import AmedasData
from datetime import datetime

# Download AMEDAS hourly data
downloader = JMAGroundDataDownloader(amedas_file='Amedas_list.csv', output_path='grounddata_download')
data, url = downloader.download_amedas(point=12345, date=datetime(2023, 8, 1), dtype='hourly')

# Load and analyze the data
amedas = AmedasData(file_path='grounddata_download/hourly/12345/2023_08_01.csv')
average_temp = amedas.calculate_average('temp_C')
print(f"Average temperature: {average_temp} ℃")
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

This tutorial covers all the available classes in the JMA Weather Data Library, providing detailed usage instructions and examples for each one. Adjust any URLs or file paths as needed to match your environment.