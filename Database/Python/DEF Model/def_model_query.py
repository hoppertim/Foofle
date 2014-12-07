from __future__ import division
import re
import json
import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
result = []
with nfldb.Tx(db) as c:
	c.execute('''
		SELECT fp.prev_amount
			, fp.int
			, fp.fumble
			, fp.td
			, fp.block_kick
			, fp.safety
			, fp.sack
			, fp.pts_allowed
			, fp.points
			, f.int as result_int
			, f.fumble as result_fumble
			, f.td as result_td
			, f.block_kick as result_block_kick
			, f.safety as result_safety
			, f.sack as result_sack
			, f.pts_allowed as result_pts_allowed
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.position = f.position
		WHERE fp.position = 'DEF'
		''')
	result = c.fetchall()

f = open('E:\School\Fall 2014\CSCE 470\Project\Python\DEF Model\def_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')