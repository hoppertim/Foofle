#!E:\Python27\python.exe

import nfldb
import sys
import predict_performance as p

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')

player = sys.argv[1]
points = 0
pred = p.Predictor()

with nfldb.Tx(_db) as c:
	c.execute('''
		select team_id
		from public.team
		where team_id = '%s'
		''' %(player))
	top_row = c.fetchone()

if top_row == None:
	with nfldb.Tx(_db) as c:
		c.execute('''
			select player_id
				, team
			from public.player
			where player_id = '%s'
			''' %(player))
		top_row = c.fetchone()

	if top_row == None:
		with nfldb.Tx(_db) as c:
			c.execute('''
				select player_id
					, team
				from
				(
					select player_id
						, team
						, levenshtein(lower(full_name), lower('%s'),1,1,2) as similarity
					from public.player
					where position in ('QB', 'RB', 'WR', 'TE', 'K')
				) as t0
				order by similarity asc
				limit 5
				''' %(player))
			top_row = c.fetchone()

	player_id = top_row['player_id']
	team_id = top_row['team']

	points = pred.predict(player_id)

else:
	team_id = top_row['team_id']
	points = pred.predict(None,team_id)

print '%3.1f' %(points)