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
   git clone https://github.com/doan-van/JMA_AMeDAS_download_v1.git
   ```

2. Install the necessary Python libraries:

   ```bash
   pip install pandas requests beautifulsoup4 numpy matplotlib
   ```
   
3. Install:

   ```bash
   cd JMA_AMeDAS_download_v1
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
from jma_data_tools import JMAGroundDataDownloader
import pandas as pd
# Initialize the downloader
downloader = JMAGroundDataDownloader(output_path='ground_data')
# Test Parameters
station_id = '47646'  # Example station ID (e.g., Tsukuba station)
test_date = pd.Timestamp('2022-02-01')  # Example date
hourly_data, url = downloader.download_amedas(station_id, test_date, dtype='hourly')
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
from jma_data_tools import JMAUpperAirDownloader
# Initialize the downloader
downloader = JMAUpperAirDownloader(output_path='upperair_data')
test_point = '47646'  # Example station code for Tsukuba
test_date = pd.Timestamp('2022-06-01 09:00')
data = downloader.download_sounding_data(test_point, test_date)
```

### JMADataPlotter

The `JMADataPlotter` class provides methods to visualize meteorological data, including sounding profiles, wind data, and temperature distributions.

#### Key Features:
- Plots upper air sounding data (e.g., Skew-T diagrams).
- Visualizes temperature and wind profiles.

#### Example Usage:
```python
from jma_data_tools import JMAUpperAirDownloader
downloader = JMAUpperAirDownloader(output_path='upperair_data')
from jma_data_tools import JMADataPlotter
test_point = '47646'  # Example station code for Tsukuba
test_date = pd.Timestamp('2022-06-01 09:00')
data = downloader.download_sounding_data(test_point, test_date)
plotter = JMADataPlotter()
plotter.plot_sounding(data, date)
```

### AmedasData

The `AmedasData` class provides tools to handle AMEDAS data, such as data loading, filtering, and processing. It helps in reading existing AMEDAS datasets and performing operations like calculating averages, extracting specific columns, or merging multiple datasets.

#### Key Features:
- Reads and processes AMEDAS data files.
- Supports data filtering and aggregation.

#### Example Usage:
```python
from jma_data_tools import AmedasData
# Test: Get information for a specific station ID
station_id = 47646  # Replace with actual station ID
print(AmedasData.get_station_info(station_id))
# Test: Get stations in a specific fuken_id
fuken_id = 11  # Replace with actual fuken_id
print(f"Stations in fuken_id {fuken_id}:")
stations_in_fuken = AmedasData.get_stations_by_fuken_id(fuken_id)
for station_id, info in stations_in_fuken.items():
    print(f"Station ID: {station_id}, Name: {info['station_name']}")
# Test: Get stations in a latitude and longitude range
lat_min, lat_max = 35.0, 37.0
lon_min, lon_max = 139.0, 141.0
stations_in_range = AmedasData.get_stations_by_location_range(lat_min, lat_max, lon_min, lon_max)
for station_id, info in stations_in_range.items():
    print(f"Station ID: {station_id}, Name: {info['station_name']}")
```

## Usage

1. **Download Ground Data**: Use the `JMAGroundDataDownloader` class to download AMEDAS data for specified stations and time periods.
2. **Download Upper Air Data**: Use the `JMAUpperAirDownloader` to get sounding data from upper air observation stations.
3. **Visualize Data**: Plot the downloaded data using the `JMADataPlotter` class.
4. **Process Existing Data**: Use `AmedasData` for reading and processing downloaded AMEDAS data.

## Examples

See test example in test/

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
