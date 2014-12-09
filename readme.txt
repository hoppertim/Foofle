-- Folder Setup
All the files necessary for setting up and maintaining the database are located in the Database folder.
All the files necessary for hosting on the web server are located in the Server folder.

-- Initial setup of the database
To setup the database used in the algorithm follow the instructions for nfldb from https://github.com/BurntSushi/nfldb.
This sets up a local copy of a postgres database that is updated with nfl player and game data.

-- Setup the custom tables and functions used in the fantasy calculation and predictions
Execute the fantasy_create.sql, fantasy_prev_create.sql, season_rankings_create.sql, and player_projections_create.sql script to create the custom tables.
Execute fantasy_prev_insert.sql, fantasy_restart.sql, player_pos_update_position.sql, and prev_games.sql to create the custom functions used.

-- Keeping the database and Naive Bayes models up-to-date
Execute update_nfldb.bat to update all the tables and create the new Naive Bayes models
*Note: file paths will need to be changed to reflect the folder structure

-- Server setup
Any web server that has support for connecting with a PostgreSQL database can be used to host the web pages
Simply copy over all the files in the Server folder to the web server
*Note: the folder structure within the Server folder can be changed but will require updating the paths in the .php files