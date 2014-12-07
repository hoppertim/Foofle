#!E:\Python27\python.exe

import nfldb
import sys
import predict_performance as p

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')


# with nfldb.Tx(_db) as c:
# 	c.execute('''
# 		SELECT
# 			player.player_id,
# 			player.team,
# 			min(game.gsis_id) as gsis_id
# 		FROM public.player
# 			JOIN public.game on player.team in (game.home_team, game.away_team)
# 		WHERE team != 'UNK'
# 			and position in ('QB', 'RB', 'WR', 'TE', 'K')
# 			and game.finished = 'f'
# 		GROUP BY player.player_id
# 		''')
# 	rows = c.fetchall()

# pred = p.Predictor()

# for row in rows:
# 	player_id = row['player_id']
# 	team_id = row['team']
# 	gsis_id = row['gsis_id']
# 	points = pred.predict(player_id)

# 	with nfldb.Tx(_db) as c:
# 		c.execute('''
# 			INSERT INTO public.player_projections
# 			VALUES ('%s', '%s','%s', %4.1f)
			# ''' %(player_id, team_id, gsis_id, points))

with nfldb.Tx(_db) as c:
	c.execute('''
		SELECT
			team.team_id as player_id,
			team.team_id,
			min(game.gsis_id) as gsis_id
		FROM public.team
			JOIN public.game on team.team_id in (game.home_team, game.away_team)
		WHERE team.team_id != 'UNK'
			and game.finished = 'f'
		GROUP BY team.team_id
		''')
	rows = c.fetchall()

pred = p.Predictor()

for row in rows:
	player_id = row['player_id']
	team_id = row['team_id']
	gsis_id = row['gsis_id']
	points = pred.predict(None, team_id)

	with nfldb.Tx(_db) as c:
		c.execute('''
			INSERT INTO public.player_projections
			VALUES ('%s', '%s','%s', %4.1f)
			''' %(player_id, team_id, gsis_id, points))