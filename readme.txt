-- Initial setup of the database
To setup the database used in the algorithm follow the instructions for nfldb from https://github.com/BurntSushi/nfldb.
This sets up a local copy of a postgres database that is updated with nfl player and game data.

-- Setup the custom tables used in the fantasy calculation and predictions
Execute the fantasy_create.sql, fantasy_prev_create.sql, and season_rankings_create.sql script to create the custom tables.
Execute the player_pos_update_position.sql to update player's positions if they are unknown.
Execute the fantasy_restart.sql script to insert entries into the fantasy table.
Execute the fantasy_prev_insert.sql script to insert entries into the fantasy_prev table.
Execute the season_rankings_insert.sql script to insert entries into the season_rankings table.

-- Create the models used in the Naive Bayes classification
Execute "python qb_model_query.py" to get the previous averages for each game
Execute "python generate_qb_model.py qb_model.json > qb_naive.json" to create the Naive Bayes classification model
Execute "python predict_performance.py"