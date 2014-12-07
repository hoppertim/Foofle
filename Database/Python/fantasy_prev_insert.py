import nfldb

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')

if __name__ == '__main__':

	with nfldb.Tx(_db) as c:
		c.execute('''
			SELECT fantasy.player_id
				, fantasy.gsis_id
			FROM public.fantasy
				join public.game on fantasy.gsis_id = game.gsis_id
			WHERE
				fantasy.position != 'DEF'
			''')
		rows = c.fetchall()

	for row in rows:
		with nfldb.Tx(_db) as c:
			c.execute('''
				INSERT INTO public.fantasy_prev
				(
					gsis_id,
					team_id,
					player_id,
					prev_amount,
					"position",
					pass_att,
					pass_cmp,
					pass_yds,
					pass_tds,
					"int",
					rush_att,
					rush_yds,
					fumble,
					targets,
					rec,
					rec_yds,
					yac,
					ret_yds,
					td,
					block_kick,
					safety,
					sack,
					pts_allowed,
					fg_50,
					fg_40,
					fg_0,
					pat,
					fg_miss,
					points
				)
				SELECT * from prev_games('%s','%s','')
				''' %(row['player_id'], row['gsis_id']))

	with nfldb.Tx(_db) as c:
		c.execute('''
			SELECT fantasy.team_id
				, fantasy.gsis_id
			FROM public.fantasy
				join public.game on fantasy.gsis_id = game.gsis_id
			WHERE
				fantasy.position = 'DEF'
			''')
		rows = c.fetchall()

	for row in rows:
		with nfldb.Tx(_db) as c:
			c.execute('''
				INSERT INTO public.fantasy_prev
				(
					gsis_id,
					team_id,
					player_id,
					prev_amount,
					"position",
					pass_att,
					pass_cmp,
					pass_yds,
					pass_tds,
					"int",
					rush_att,
					rush_yds,
					fumble,
					targets,
					rec,
					rec_yds,
					yac,
					ret_yds,
					td,
					block_kick,
					safety,
					sack,
					pts_allowed,
					fg_50,
					fg_40,
					fg_0,
					pat,
					fg_miss,
					points
				)
				SELECT * from prev_games('','%s','%s')
				''' %(row['gsis_id'], row['team_id']))