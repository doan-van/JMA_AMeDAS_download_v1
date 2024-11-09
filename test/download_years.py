
import pandas as pd
from jma_data_tools import JMAGroundDataDownloader
import time
import os

# Initialize the downloader
downloader = JMAGroundDataDownloader(amedas_file='../Amedas_list.csv')

# Set up parameters
point = '47646'  # Example: Tsukuba station
output_dir = "daily_data"  # Directory to save daily data files
start_date = pd.Timestamp('1990-01-01')
end_date = pd.Timestamp('2021-12-31')

# Generate date range for 30 years of daily data
date_range = pd.date_range(start=start_date, end=end_date, freq='M')

# Loop over each date to download daily data
for date in date_range[-1:]:

    print(f"Downloading data for {date.strftime('%Y-%m-%d')}...")
    # Download the daily data for the specified point and date
    daily_data = downloader.download_amedas(point, date, dtype='daily')
    
    time.sleep(0.5)

print("Download complete.")
