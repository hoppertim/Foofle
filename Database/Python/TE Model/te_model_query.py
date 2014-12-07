from __future__ import division
import re
import json
import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
result = []
with nfldb.Tx(db) as c:
	c.execute('''
		SELECT fp.prev_amount
			, fp.fumble
			, fp.targets
			, fp.rec
			, fp.rec_yds
			, fp.yac
			, fp.td
			, fp.points
			, f.fumble as result_fumble
			, f.targets as result_targets
			, f.rec as result_rec
			, f.rec_yds as result_rec_yds
			, f.yac as result_yac
			, f.td as result_td
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.player_id = f.player_id
		WHERE fp.position = 'TE'
		''')
	result = c.fetchall()

f = open('E:\School\Fall 2014\CSCE 470\Project\Python\TE Model\\te_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')