CREATE OR REPLACE FUNCTION fantasy_restart()
RETURNS void AS $$
BEGIN
	delete from public.fantasy;
	delete from public.fantasy_prev;

	/*
		Aggregates the offensive stats of individual players into their
		performance for each game and calculates the points that they earned

		Only should be run if fantasy table is empty or it will insert duplicate values
	*/

	with t0 as(
		--Selects all the plays and aggregates them based on the game and player
		--to get the total offensive stats for a player for each game
		select g.gsis_id
			, pp.team
			, p.player_id
			, case when p.position = 'FB' then cast('RB' as player_pos) else p.position end
			, sum(pp.passing_att) as pass_atm
			, sum(pp.passing_cmp) as pass_cmp
			, sum(pp.passing_yds) as pass_yds
			, sum(pp.passing_tds) as pass_tds
			, sum(pp.passing_int) as int
			, sum(pp.rushing_att) as rush_att
			, sum(pp.rushing_yds) as rush_yds
			, sum(pp.fumbles_lost) as fumble
			, sum(pp.receiving_tar) as  targets
			, sum(pp.receiving_rec) as rec
			, sum(pp.receiving_yds) as rec_yds
			, sum(pp.receiving_yac_yds) as yac
			, sum(pp.kickret_yds + pp.puntret_yds) as ret_yds
			, sum(pp.receiving_tds + pp.rushing_tds + pp.kickret_tds + pp.puntret_tds) as td
			, sum(case when pp.kicking_fgm_yds >= 50 then 1 else 0 end) as fg_50
			, sum(case when pp.kicking_fgm_yds < 50 and pp.kicking_fgm_yds >= 40 then 1 else 0 end) as fg_40
			, sum(case when pp.kicking_fgm_yds < 40 and pp.kicking_fgm_yds > 0 then 1 else 0 end) as fg_0
			, sum(pp.kicking_xpmade) as pat
			, sum(pp.kicking_fgmissed + pp.kicking_xpmissed) as fg_miss
		from public.player as p
			join public.play_player as pp
				on pp.player_id = p.player_id
			join public.game as g
				on pp.gsis_id = g.gsis_id
		where p.position in ('QB', 'WR', 'RB', 'TE', 'FB', 'K')
			and g.season_type != 'Preseason'
		group by p.player_id
			, g.gsis_id
			, pp.team
		order by p.full_name
			, g.season_year
			, g.season_type
			, g.week
	)
	insert into fantasy
	(
		gsis_id
		, team_id
		, player_id
		, position
		, pass_att
		, pass_cmp
		, pass_yds
		, pass_tds
		, int
		, rush_att
		, rush_yds
		, fumble
		, targets
		, rec
		, rec_yds
		, yac
		, ret_yds
		, td
		, fg_50
		, fg_40
		, fg_0
		, pat
		, fg_miss
		, points
	)
	select t0.gsis_id
		, t0.team
		, t0.player_id
		, t0.position
		, t0.pass_atm
		, t0.pass_cmp
		, t0.pass_yds
		, t0.pass_tds
		, t0.int
		, t0.rush_att
		, t0.rush_yds
		, t0.fumble
		, t0.targets
		, t0.rec
		, t0.rec_yds
		, t0.yac
		, t0.ret_yds
		, t0.td
		, t0.fg_50
		, t0.fg_40
		, t0.fg_0
		, t0.pat
		, t0.fg_miss
		--Calculation of offensive fantasy points
		, (
			t0.pass_yds / 25.0
			+ t0.pass_tds * 4.0
			- t0.int * 2.0
			+ t0.rush_yds / 10.0
			- t0.fumble * 2.0
			+ t0.rec_yds / 10.0
			+ t0.ret_yds / 10.0
			+ t0.td * 6.0
			+ t0.fg_50 * 5.0
			+ t0.fg_40 * 4.0
			+ t0.fg_0 * 3.0
			+ t0.pat * 1.0
			- t0.fg_miss * 1.0
		) as points
	from t0
	order by t0.gsis_id;

	/*
		Aggregates the defensive stats of individual players into the team's
		performance for each game and calculates the points that the defense earned

		Only should be run if fantasy table is empty or it will insert duplicate values
	*/
	with t0 as(
		--Selects all the plays and aggregates them based on the game and team
		--to get the total defensive stats for a team for each game
		select g.gsis_id
			, pp.team
			, cast('DEF' as player_pos) as position
			, g.season_year
			, g.season_type
			, g.week
			, sum(pp.defense_int) as int
			, sum(pp.defense_frec) as fumble
			, sum
			(
				pp.defense_frec_tds
				+ pp.defense_int_tds
				+ pp.defense_misc_tds
				+ pp.kicking_rec_tds
				+ pp.kickret_tds
				+ pp.puntret_tds
			)as td
			, sum(pp.defense_fgblk + pp.defense_xpblk + pp.defense_puntblk) as block_kick
			, sum(pp.defense_safe) as safety
			, sum(pp.defense_sk) as sack
			, case when pp.team = g.home_team then g.away_score else g.home_score end as pts_allowed
		from public.play_player as pp
			join public.game as g
				on pp.gsis_id = g.gsis_id
		where g.season_type != 'Preseason'
		group by g.gsis_id
			, pp.team
		order by pp.team
			, g.season_year
			, g.season_type
			, g.week
	)
	insert into public.fantasy
	(
		gsis_id
		, team_id
		, position
		, int
		, fumble
		, td
		, block_kick
		, safety
		, sack
		, pts_allowed
		, points
	)
	select t0.gsis_id
		, t0.team
		, t0.position
		, t0.int
		, t0.fumble
		, t0.td
		, t0.block_kick
		, t0.safety
		, t0.sack
		, t0.pts_allowed
		--Calculation of defensive fantasy points
		, (
			t0.int * 2.0
			+ t0.fumble * 2.0
			+ t0.td * 6.0
			+ t0.block_kick * 2.0
			+ t0.safety * 2.0
			+ t0.sack * 1.0
			+ case
				when t0.pts_allowed = 0 then 5
				when t0.pts_allowed < 7 then 4
				when t0.pts_allowed < 14 then 3
				when t0.pts_allowed < 18 then 1
				when t0.pts_allowed < 28 then 0
				when t0.pts_allowed < 35 then -1
				when t0.pts_allowed < 46 then -3
				else -5
			end
		)
	from t0
	order by gsis_id;
END;
$$ LANGUAGE plpgsql