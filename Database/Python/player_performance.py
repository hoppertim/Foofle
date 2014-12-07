import nfldb
import sys
import predict_performance as p

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')

if __name__ == '__main__':

	player = sys.argv[1]

	with nfldb.Tx(_db) as c:
		c.execute('''
			select player_id
			from public.player
			where player_id = '%s'
			''' %(player))
		top_row = c.fetchone()

	if top_row == None:
		with nfldb.Tx(_db) as c:
			c.execute('''
				select player_id
					, full_name
					, team
				from
				(
					select player_id
						, full_name
						, team
						, levenshtein(lower(full_name), lower('%s'),1,1,2) as similarity
					from public.player
					where position in ('QB', 'RB', 'WR', 'TE', 'K')
				) as t0
				order by similarity asc
				limit 5
				''' %(player))
			top_row = c.fetchone()

	full_name = top_row['full_name']
	player_id = top_row['player_id']
	team_id = top_row['team']
	pred = p.Predictor()

	print "Player: %s" %(full_name)

	points = pred.predict(player_id)

	print 'Predicted points: %3.1f' %(points)