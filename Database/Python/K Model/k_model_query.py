from __future__ import division
import re
import json
import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
result = []
with nfldb.Tx(db) as c:
	c.execute('''
		SELECT fp.prev_amount
			, fp.fg_50
			, fp.fg_40
			, fp.fg_0
			, fp.pat
			, fp.fg_miss
			, fp.points
			, f.fg_50 as result_fg_50
			, f.fg_40 as result_fg_40
			, f.fg_0 as result_fg_0
			, f.pat as result_pat
			, f.fg_miss as result_fg_miss
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.player_id = f.player_id
		WHERE fp.position = 'K'
		''')
	result = c.fetchall()

f = open('E:\School\Fall 2014\CSCE 470\Project\Python\K Model\k_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')