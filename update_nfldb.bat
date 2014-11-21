python "E:\Python27\Scripts\nfldb-update"
psql --command="Select update_position()" --username nfldb --dbname=nfldb
psql --command="Select fantasy_restart()" --username nfldb --dbname=nfldb
psql --command="Select fantasy_prev_insert()" --username nfldb --dbname=nfldb