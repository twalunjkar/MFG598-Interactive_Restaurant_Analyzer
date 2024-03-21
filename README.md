# Interactive Restaurant Analyzer

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Results](#results)
- [Installation and Setup](#Installation-and-Setup)
- [Project Proposal](Documents/ProjectProposal.pdf)

## Overview

The Interactive Restaurant Analyzer is a Python-based application designed to provide comprehensive analysis of restaurant data obtained from sources like Zomato. Leveraging various Python libraries, including Tkinter, Pandas, Folium, and Matplotlib, this tool offers an intuitive graphical interface for exploring and analyzing restaurant information. Users can select a country and city to access a range of analytical features such as mapping restaurant locations, comparing restaurant details, listing cuisines, visualizing rating distributions, and filtering restaurants based on reviews.

## Key Features

- **Map View**: Plot restaurant locations on an interactive map using Folium.
- **Compare View**: Analyze two restaurants side by side to compare metrics like price range, rating, and service availability.
- **Cuisine List**: Explore restaurants serving specific cuisines, enhancing culinary diversity.
- **Rating Distribution**: Visualize the distribution of restaurant ratings using a nested pie chart, providing insights into aggregate ratings based on rating colors.
- **Review Filter**: Refine restaurant searches by filtering options based on aggregate ratings.

## Project Structure

- **`restaurant_analysis_code.py`**: Main Python script containing the GUI implementation using Tkinter.
- **`country-code.xlsx`**: Excel file containing country codes and names.
- **`zomato.csv`**: CSV file containing restaurant data obtained from Zomato.
- **`cityscape.png`**: Background image for the GUI interface.
- **`mapView.png`**, **`compareView.png`**, **`listView.png`**, **`chartView.png`**, **`reviewView.png`**: Image icons used for GUI buttons.

## Results

The Interactive Restaurant Analyzer provides users with an intuitive interface to explore and analyze restaurant data effectively. Users can visualize restaurant locations, compare details of individual restaurants, explore various cuisines, analyze rating distributions, and filter restaurant options based on reviews. The tool facilitates informed decision-making by presenting comprehensive insights into dining options, thereby enhancing the overall dining experience.

## Installation and Setup

Before running the code, ensure that all necessary libraries are installed and they support the version of the Python platform being used. You can refer to the `requirements.txt` file for a list of required libraries and their versions. You can install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

Also, make sure to place all the input datasets, images, and the Python code file in the same directory to avoid any errors.

## Citation

- **All images**: Microsoft 365 Excel, Microsoft Corporation, 2022, Insert Icons > Images
- **Input datasets**: [Zomato Restaurants Data](https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data) from Kaggle