import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import requests


def download_dataset(url, output_path):
    if not os.path.exists(output_path):
        print("Downloading dataset...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(output_path, 'wb') as file, tqdm(
            desc="Downloading",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                bar.update(len(data))
    else:
        print("Dataset already exists.")


def plot_global_temperature(file_path):
    data = pd.read_csv(file_path, delimiter=',', skiprows=4)

    font_size = 20

    data['5-Year Mean'] = data['Anomaly'].rolling(window=5).mean()

    plt.figure(figsize=(12, 8))
    plt.plot(data['Year'], data['Anomaly'], label='Teplotní Anomálie', linewidth=3, color='navy')
    plt.plot(
        data['Year'],
        data['5-Year Mean'],
        label='5-letý průměr',
        color='red',
        linewidth=3)
    plt.xlabel('Rok', fontsize=font_size)
    plt.ylabel('Teplotní Anomálie (°C)', fontsize=font_size)
    plt.tick_params(axis='both', which='major', labelsize=font_size - 5)  # Increase tick label font size
    plt.legend(fontsize=font_size)
    plt.grid()
    plt.show()


def main():
    dataset_url = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/tavg/land_ocean/1/4/1850-2025/data.csv"
    dataset_folder = "datasets"
    dataset_file = os.path.join(dataset_folder, "data.csv")

    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    download_dataset(dataset_url, dataset_file)
    plot_global_temperature(dataset_file)


if __name__ == "__main__":
    main()
