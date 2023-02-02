
# State of the Tech Labor Market
![Header](https://github.com/ntdoris/dsc-project-5/blob/main/images/header.png)

[Source: Capital Search](https://www.capitalsearch.com/2018-job-market/)


Since the beginning of this year, over 85,000 people in the tech industry have lost their jobs. Given these massive numbers, I thought it would be helpful to take a deeper look at the state of the industry to get a sense of what is really going on behind the scenes -- and to see whether there is hope for any of us out there who are looking for a job.

This dashboard is split into three sections - the first will give a general sense of economic conditions in the sector and more generally, the second will take a closer look at recent layoffs and predict whether companies will experience multiple rounds or just a one off, and the third will 
focus on job postings


## The Data

The data for this project came from several sources:
* [layoffs.fyi](https://layoffs.fyi/)
* [U.S. Census Bureau - API](https://api.census.gov/data/timeseries/eits/bfs.html)
* [Simply WallSt](https://simplywall.st/markets/us/tech)
* [Crunchbase](https://www.crunchbase.com/)
* [U.S. Bureau of Labor Statistics](https://www.bls.gov/)
* [Kaggle / Affinity / Lightcast)](https://www.kaggle.com/datasets/douglaskgaraujo/opportunity-insights-real-time-economic-tracker-us)
* [Indeed Hiring Lab](https://www.hiringlab.org/)
* [Yahoo Finance](https://finance.yahoo.com/)

## Modeling

I ran two types of models, the first a SARIMA Time Series Forecast for Job Postings, and the second a classification model predicting whether a company will need to do more than one round of layoffs.

### Job Postings Time Series Forecast

* The data showed a clear upward trend and 52-week seasonality:
![image]()

* The final model passed all assumptions, and resulted in a RMSE of ~ 0.1
![image]()

* Forecast:
![image]()

### Layoff Frequency Prediction - Classification Model

* The final model was an XG Boost Classifier, and included categorical data - industry, country, number of employees, status - as well as continuous data - revenue estimate, year of the first round of layoffs, amount raised in the first round of layoffs, Crunchbase trend score, number of acquisitions, number of funding rounds, total funding amount.

![image]()
![image]()

## Dashboard Demo

![image]()
![image]()
![image]()

## Conclusion / Next Steps

* THERE IS HOPE. Job postings should remain stable for the next year, meaning there are opportunities for laid off employees
* Larger companies tend to see more rounds of layoffs ? be proactive if you are an employee at one of these firms
* Potential next steps include: gathering more company data to feed into classification model, gathering data describing the specific roles laid off, salary, & types of jobs posted to match laid off employees with job postings that may fit their background, building out dashboard with more data on the industry and adding an interactive component to the layoff tab

## For More Information

* [Notebook]()
* [Presentation]()
* Reach me at ntdoris2@gmail.com

## Repository Structure

* Data
*  Assets <- image files
* Data Visualization & Dashboard Notebook
* Modeling Notebook
* Presentation Deck
* README.md