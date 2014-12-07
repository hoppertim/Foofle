from __future__ import division
import re
import json
import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
result = []
with nfldb.Tx(db) as c:
	c.execute('''
		SELECT fp.prev_amount
			, fp.pass_att
			, fp.pass_cmp
			, fp.pass_yds
			, fp.pass_tds
			, fp.int
			, fp.rush_att
			, fp.rush_yds
			, fp.fumble
			, fp.td
			, fp.points
			, f.pass_att as result_pass_att
			, f.pass_cmp as result_pass_cmp
			, f.pass_yds as result_pass_yds
			, f.pass_tds as result_pass_tds
			, f.int as result_int
			, f.rush_att as result_rush_att
			, f.rush_yds as result_rush_yds
			, f.fumble as result_fumble
			, f.td as result_td
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.player_id = f.player_id
		WHERE fp.position = 'QB'
			and f.pass_att > 4
			and f.pass_cmp > 1
		''')
	result = c.fetchall()

f = open('E:\School\Fall 2014\CSCE 470\Project\Python\QB Model\qb_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')