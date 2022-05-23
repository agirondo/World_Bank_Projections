# World_Bank_Projections

The propose of this proyect is to use World Bank's data to measure the impact of shocks such as teh covid-19 epidemic in each country using autoregresion based projections as the baseline. We choose a target year, make projections based on historical data and compare the result with the real value.

1. Data: contains csv files with error in target year (shock impact) as well as the mean error for  previous years (as an aproximation of the model's accuracy)
2. src: contains functions to retreive and transform data form World Bank's API
3. tables.ipynb: specific instance of shock evaluation, saves results in Data folder.

Resources:

- World Bank API
- Python packages: pandas, requests, statmodels