# Mathematical and Instrumental Methods in Economics

This repository contains Python code developed as part of a PhD thesis on **Mathematical Economics**, focusing on manipulating economic datasets and analyzing the **Cobb-Douglas production function**. The project evolved over time from basic Excel spreadsheets and VBA scripts to a more sophisticated Python implementation. While the code is still in an evolving state, it covers several areas of analysis, including elasticity, economic transformations, and complex dataset handling.

## Overview

This repository is organized to handle a variety of economic datasets, perform various calculations (such as elasticities), apply transformations to data (e.g., scaling, normalizing), and produce visualizations for analysis. The codebase contains individual scripts, tools for data manipulation, and utility functions for working with both simple and complex economic models.

The core functionality revolves around working with **Cobb-Douglas production functions** and related economic models, but also touches on other macroeconomic data like capital, commodities, and manufacturing.

## Key Functionalities

* **Data Handling & Collection**: Tools to download, unzip, and preprocess various economic datasets (e.g., U.S. Bureau of Economic Analysis data, U.S. Census data).
* **Transformations**: Functions for data normalization, scaling, and other preparatory transformations needed for analysis.
* **Elasticity & Economic Calculations**: Implementations of Cobb-Douglas functions and elasticities for various economic sectors and regions.
* **Visualization**: Includes plotting utilities for visualizing key results and economic relationships.
* **Testing & Validation**: Tools for ensuring that transformations and models are behaving as expected.

## Directory Structure

```
.
├── data/                # Raw datasets (zipped files) used in the analysis
├── metadata/            # Metadata for dataset files
├── src/                 # Python source code
│   ├── core/            # Core utility functions and classes
│   ├── data/            # Data preparation and dataset-specific scripts
│   ├── elasticity.py    # Cobb-Douglas elasticity and related calculations
│   ├── plot.py          # Visualization functions
│   ├── main.py          # Main entry point for running scripts
│   ├── usa_*.py         # Scripts specific to U.S. economic data and analysis
└── README.md            # This file
```

## Getting Started

### 1. Setup

To begin using this project, you’ll need Python 3.x and several dependencies. You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` file, you can manually install the necessary packages (e.g., `pandas`, `numpy`, `matplotlib`, `scipy`).

### 2. Data Preparation

Before running any analysis, you'll need the raw datasets. Download the required zipped files and place them in the `data/` folder. The scripts are designed to handle these files automatically.

* **dataset_douglas.zip**: Data specific to the Cobb-Douglas model.
* **dataset_usa_cobb-douglas.zip**: U.S. economic data for Cobb-Douglas functions.
* **dataset_usa_kendrick.zip**: U.S. economic data (Kendrick model).
* **dataset_uscb.zip**: Data from the U.S. Census Bureau.

### 3. Running the Code

To run the project, you can start with the main script:

```bash
python src/main.py
```


This will invoke various data processing, calculations, and visualizations based on the scripts in the `src/` directory.

### 4. Example Use Cases

Here are some common use cases you might be interested in:

* **Elasticity Calculation**: You can compute the elasticity of production for different regions and sectors.
* **Data Transformation**: Preprocess raw data and normalize values for further analysis.
* **Plotting Results**: Visualize key economic relationships (e.g., output vs. input, elasticity vs. time).

## Modules

### Core Modules

* **`src/core/backend.py`**: Contains backend functions for processing raw data, interfacing with external data sources, and handling I/O.
* **`src/core/classes.py`**: Defines key classes for representing economic models, datasets, and transformations.
* **`src/core/config.py`**: Configuration settings, including file paths and default parameters.
* **`src/core/transform.py`**: Functions for data normalization, scaling, and other transformations.

### Cobb-Douglas Models

* **`src/cobb_douglas_usa.py`**: Implementations of the Cobb-Douglas model specific to U.S. data.
* **`src/cobb_douglas_complex.py`**: More complex versions of the Cobb-Douglas model.

### U.S. Economic Data

* **`src/usa_bea.py`**: Scripts for working with data from the U.S. Bureau of Economic Analysis.
* **`src/usa_capital.py`**: Functions for analyzing U.S. capital data.
* **`src/usa_douglas.py`**: Functions for working with U.S. Cobb-Douglas data.
* **`src/uscb.py`**: Functions for working with U.S. Census Bureau data.

### Visualization and Plotting

* **`src/plot.py`**: Includes functions to generate plots of economic models and data (e.g., elasticity, production functions).

## Contributing

This project is still a work in progress. Contributions are welcome! If you have suggestions, bug fixes, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Some Notes:

1. **Refactoring Considerations**: Given the "unfinished" nature of the project, you might want to look into refactoring by modularizing certain functionalities. For example, separating out the economic models into distinct classes, and making the data transformations more flexible and reusable.

2. **Documentation**: As you mentioned, the README was outdated. Be sure to keep the documentation up to date as you refactor and improve the code. Clear documentation will help others (and yourself) understand the design of your code.

3. **Dependencies**: If you don't already have a `requirements.txt`, it might be worth generating one using:

   ```bash
   pip freeze > requirements.txt
   ```

4. **Versioning**: If you plan on working on this over time or sharing it with others, version control (e.g., using Git) can be really helpful for tracking progress and collaboration.
---
