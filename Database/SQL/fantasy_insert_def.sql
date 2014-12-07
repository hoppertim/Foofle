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