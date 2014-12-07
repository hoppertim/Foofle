REM Update the database with current games/stats
python "E:\Python27\Scripts\nfldb-update"

REM Update the custom tables to reflect the new games/stats
psql --command="Select update_position()" --username nfldb --dbname=nfldb
psql --command="Select fantasy_restart()" --username nfldb --dbname=nfldb
python "E:\School\Fall 2014\CSCE 470\Project\Python\fantasy_prev_insert.py"

REM Update the Naive Bayes models based on the new tables
python "E:\xampp\htdocs\Python\QB Model\qb_model_query.py"
python "E:\xampp\htdocs\Python\RB Model\rb_model_query.py"
python "E:\xampp\htdocs\Python\WR Model\wr_model_query.py"
python "E:\xampp\htdocs\Python\TE Model\te_model_query.py"
python "E:\xampp\htdocs\Python\K Model\k_model_query.py"
python "E:\xampp\htdocs\Python\DEF Model\def_model_query.py"

python "E:\xampp\htdocs\Python\QB Model\generate_qb_model.py" "E:\xampp\htdocs\Python\QB Model\qb_model.json" > "E:\xampp\htdocs\Python\QB Model\qb_naive.json"
python "E:\xampp\htdocs\Python\RB Model\generate_rb_model.py" "E:\xampp\htdocs\Python\RB Model\rb_model.json" > "E:\xampp\htdocs\Python\RB Model\rb_naive.json"
python "E:\xampp\htdocs\Python\WR Model\generate_wr_model.py" "E:\xampp\htdocs\Python\WR Model\wr_model.json" > "E:\xampp\htdocs\Python\WR Model\wr_naive.json"
python "E:\xampp\htdocs\Python\TE Model\generate_te_model.py" "E:\xampp\htdocs\Python\TE Model\te_model.json" > "E:\xampp\htdocs\Python\TE Model\te_naive.json"
python "E:\xampp\htdocs\Python\K Model\generate_k_model.py" "E:\xampp\htdocs\Python\K Model\k_model.json" > "E:\xampp\htdocs\Python\K Model\k_naive.json"
python "E:\xampp\htdocs\Python\DEF Model\generate_def_model.py" "E:\xampp\htdocs\Python\DEF Model\def_model.json" > "E:\xampp\htdocs\Python\DEF Model\def_naive.json"