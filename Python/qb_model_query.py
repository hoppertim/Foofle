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
			, f.points as result_points
		FROM public.fantasy_prev as fp
			JOIN public.fantasy as f on fp.gsis_id = f.gsis_id and fp.player_id = f.player_id
		WHERE fp.position = 'QB'
		''')
	result = c.fetchall()

f = open('qb_model.json', 'w')

for row in result:
	f.write(json.dumps(row) + '\n')