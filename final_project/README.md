# Final Project: Using Machine Learning to Predict NHL Game Outcomes

The focus of this final portion of the project will be to analyze certain aspects of an NHL game and to create a model to predict 
the game outcome.

## Data

The data used in the project was player and team game statistics and game outcomes scraped from the NHLs [statsapi](https://gitlab.com/dword4/nhlapi).
The script that scrapes these data can be found in [/game/pull_games.py](https://github.com/sjacobson94/COMP4449/blob/master/final_project/game/pull_games.py).


## Analysis

The analysis can be seen in [analysis.ipynb](https://github.com/sjacobson94/COMP4449/blob/master/final_project/analysis.ipynb). 
Predictions of outcome were done by predicting whether the home team would win. The difference in home and away team statistics 
were used as features in this modeling process.

The final report submitted for this project can be seen in [
NHL_Game_Analytics.pdf](https://github.com/sjacobson94/COMP4449/blob/master/final_project/NHL_Game_Analytics.pdf).
