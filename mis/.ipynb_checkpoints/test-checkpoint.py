#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:29:19 2024

@author: doan
"""

# test_jma_data_tools.py

import pandas as pd
import sys
from jma_data_tools import JMAGroundDataDownloader, JMAUpperAirDownloader, JMADataPlotter

# Initialize the downloader and plotter classes
ground_downloader = JMAGroundDataDownloader(output_path='data_download')
upper_air_downloader = JMAUpperAirDownloader()
plotter = JMADataPlotter()

# Set up test parameters
point = '47646'  # Tsukuba station, for example
date = pd.Timestamp('2022-02-01 09:00')  # Test date for data download
output_dir = "test_output"  # Directory to save test output files

# Test ground data download
print("Testing ground data download...")
ground_data, url = ground_downloader.download_amedas(point, date, dtype='hourly')
print("Downloaded ground data:")
print(ground_data.head())


# Test upper air data download
print("Testing upper air data download...")
upper_air_data = upper_air_downloader.get_data_sonde(point, date)
print("Downloaded upper air data:")
print(upper_air_data)

# Test plotting functions
print("Testing plotting functions...")

# Plot the hourly temperature, humidity, and wind from ground data
if 'temp_C' in ground_data.columns and 'rh_percent' in ground_data.columns and 'wspd_ms' in ground_data.columns:
    print("Plotting ground data (temperature, humidity, and wind)...")
    plotter.plot_hourly_temp_hum_wind(ground_data)

# Plot the sounding data
if 'Temp(C)' in upper_air_data['noisuy'].columns:
    print("Plotting upper air sounding data...")
    plotter.plot_sounding(upper_air_data['noisuy'], date)

print("Testing complete. Check the 'test_output' directory for generated plots.")
