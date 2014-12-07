from __future__ import division
import re
import json
import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
result = []
with nfldb.Tx(db) as c:
	c.execute('''
		SELECT fp.prev_amount
			, fp.rush_att
			, fp.rush_yds
			, fp.fumble
			, fp.targets
			, fp.rec
			, fp.rec_yds
			, fp.yac
			, fp.td
			, fp.points
			, f.rush_att as result_rush_att
			, f.rush_yds as result_rush_yds
			, f.fumble as result_fumble
			, f.targets as result_targets
			, f.rec as result_rec
			, f.rec_yds as result_rec_yds
			, f.yac as result_yac
			, f.td as result_td
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.player_id = f.player_id
		WHERE fp.position = 'RB'
		''')
	result = c.fetchall()

f = open('E:\School\Fall 2014\CSCE 470\Project\Python\RB Model\\rb_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')