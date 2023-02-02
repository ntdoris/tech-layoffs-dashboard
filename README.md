
# State of the Tech Labor Market
![Header](https://github.com/ntdoris/dsc-project-5/blob/main/images/header.png)

[Source: Capital Search](https://www.capitalsearch.com/2018-job-market/)


According to [layoffs.fyi](https://layoffs.fyi/), since the beginning of this year, over 85,000 people in the tech industry have lost their jobs. Given these massive numbers, I thought it would be helpful to take a deeper look at the state of the industry to get a sense of what is really going on behind the scenes -- and to see whether there is hope for any of us out there who are looking for a job.

To tackle this problem, I ran a classification model targeting whether a company will need to execute more than one round of layoffs as well as a time series model forecasting future job postings. To bring it all together, I created an interactive dashboard, split into three sections.

The first will give a general sense of economic conditions in the sector more generally, the second will take a closer look at recent layoffs and predict whether companies will experience multiple rounds or just a one off, and the third will focus on job postings. If you're just curious on what the state of the industry looks like, the first tab will be the most useful. If you're in the industry, and haven't been laid off, the layoff tab is where you can go to predict whether your company may be needing to do another round. If you've been laid off and are looking at a job, your focus will be the job postings forecast - will more jobs be available in the near future for you to apply to? 


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
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/seasonality.png)

* The final model passed all assumptions, and resulted in a RMSE of ~ 0.1
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/model_validation.png)

* Forecast:
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/feat_importance_final.png)

### Layoff Frequency Prediction - Classification Model

![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/layoffs_by_industry.png)

* The final model was an XG Boost Classifier, and included categorical data - industry, country, number of employees, status - as well as continuous data - revenue estimate, year of the first round of layoffs, amount raised in the first round of layoffs, Crunchbase trend score, number of acquisitions, number of funding rounds, total funding amount.

![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/feat_importance_final.png)
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/conf_matrix.png)

## Dashboard Demo

![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/dash1.png)
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/dash2.png)
![image](https://github.com/ntdoris/dsc-project-5/blob/main/images/dash3.png)

## Conclusion / Next Steps

* THERE IS HOPE. Job postings should remain stable for the next year, meaning there are opportunities for laid off employees
* Larger companies tend to see more rounds of layoffs ? be proactive if you are an employee at one of these firms
* Potential next steps include: gathering more company data to feed into classification model, gathering data describing the specific roles laid off, salary, & types of jobs posted to match laid off employees with job postings that may fit their background, building out dashboard with more data on the industry and adding an interactive component to the layoff tab

## For More Information

* [Notebook](https://github.com/ntdoris/dsc-project-5/blob/main/modeling.ipynb)
* [Presentation](https://github.com/ntdoris/dsc-project-5/blob/main/presentation.pdf)
* Reach me at ntdoris2@gmail.com

## Repository Structure

* Data
*  Assets <- image files
* Data Visualization & Dashboard Notebook
* Modeling Notebook
* Presentation Deck
* README.md