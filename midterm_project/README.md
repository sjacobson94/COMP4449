# Midterm Project: Player Salary Predictions

This midterm project focused on using machine learning to predict National Hockey League (NHL) player salaries based on data collected for 
the 2018-19 and 2019-20 seasons. Data for 2020-21 was available at the time of analysis, but the season was still 
underway and was this left out.

## Data

The data used in the project was player statistics scraped from the NHLs [statsapi](https://gitlab.com/dword4/nhlapi) 
while the salary data was scraped from a third party [website](https://www.spotrac.com/nhl/). The script that scrapes 
these data can be found in [/nhl/player.py](https://github.com/sjacobson94/COMP4449/blob/master/midterm_project/nhl/player.py).

Data for Goaltenders was intentionally not collected/used as the position collects and values completely different statistics and would require 
its own model and dataset. 

## Analysis

The analysis can be seen in [analysis.ipynb](https://github.com/sjacobson94/COMP4449/blob/master/midterm_project/analysis.ipynb). 
The predictions and analyses were broken into 3 sections: predicting all player salaries, predicting just forwards, and then just 
defensemen.
Those familiar with the sport will understand that different attributes and statistics are generally correlated 
with players in different positions. Lumping them all together proves to be a fruitless task.

The final report submitted for this project can be seen in [
NHL_Player_Analytics.pdf](https://github.com/sjacobson94/COMP4449/blob/master/midterm_project/NHL_Player_Analytics.pdf).
