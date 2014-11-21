import nfldb

db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')
with nfldb.Tx(db) as c:
	c.execute('''
		select player.last_name
		from public.player
			join public.play_player on play_player.player_id = player.player_id
		where player.full_name = '%s'
		and play_player.receiving_rec = 1
		and play_player.receiving_yds > 20
		and play_player.receiving_yac_yds < 10
		''' %('Dez Bryant'))
	result = c.fetchone()
	print result