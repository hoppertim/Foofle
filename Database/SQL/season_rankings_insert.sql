--Create temp table to hold offensive stats
create temp table season_off_rankings
(
  season_year smallint NOT NULL,
  team_id character varying(3) NOT NULL,
  avg bool,
  off_pts double precision NOT NULL,
  off_pass_yds double precision,
  off_pass_tds double precision,
  off_rush_yds double precision,
  off_rush_tds double precision,
  off_int double precision,
  off_fumble double precision,
  off_sack double precision
) on commit drop;

--Create temp table to hold defensive stats
create temp table season_def_rankings
(
	season_year smallint NOT NULL,
	team_id character varying(3) NOT NULL,
	avg bool,
	def_pts double precision NOT NULL,
	def_pass_att double precision,
	def_pass_cmp double precision,
	def_pass_yds double precision,
	def_pass_tds double precision,
	def_int double precision,
	def_rush_att double precision,
	def_rush_yds double precision,
	def_rush_tds double precision,
	def_fumble double precision,
	def_targets double precision,
	def_rec double precision,
	def_rec_yds double precision,
	def_rec_tds double precision,
	def_yac double precision,
	def_sack double precision,
	def_block double precision,
	def_safety double precision,
	def_tds double precision
) on commit drop;

--Insert season averages for each team into temp table
insert into season_off_rankings
(
	season_year,
	team_id,
	avg,
	off_pts,
	off_pass_yds,
	off_rush_yds,
	off_pass_tds,
	off_rush_tds,
	off_int,
	off_fumble,
	off_sack
)
--Aggregate offensive stats for each game and
--Take the average to find season average
select g.season_year
	, t0.team
	, True
	, 0
	, round(avg(t0.off_pass_yds), 2) as off_pass_yds
	, round(avg(t0.off_rush_yds), 2) as off_rush_yds
	, round(avg(t0.off_pass_tds), 2) as off_pass_tds
	, round(avg(t0.off_rush_tds), 2) as off_rush_tds
	, round(avg(t0.off_int), 2) as off_int
	, round(avg(t0.off_fumble), 2) as off_fumble
	, round(avg(t0.off_sack), 2) as off_sack
from
(
	--Aggregate offensive player stats for each game
	select pp.gsis_id
		, pp.team
		, sum(pp.passing_yds) as off_pass_yds
		, sum(pp.passing_tds) as off_pass_tds
		, sum(pp.rushing_yds) as off_rush_yds
		, sum(pp.rushing_tds) as off_rush_tds
		, sum(pp.passing_int) as off_int
		, sum(pp.fumbles_lost) as off_fumble
		, sum(pp.passing_sk) as off_sack
	from public.play_player as pp
	group by pp.gsis_id, pp.team
) as t0
join public.game as g on g.gsis_id = t0.gsis_id
where g.season_type != 'Preseason'
group by g.season_year, t0.team;

--Updates the offensive points for each team
update season_off_rankings
set off_pts = round(t0.pts, 4)
from (
	select g.season_year
		, t.team_id
		--Score can be either home or away
		, sum(case when t.team_id = g.home_team then g.home_score else g.away_score end) * 1.0 / count(*) as pts
	from public.team as t
	join public.game as g on g.home_team = t.team_id or g.away_team = t.team_id
	where g.finished = 't'
	group by g.season_year, t.team_id
) as t0
where season_off_rankings.season_year = t0.season_year and season_off_rankings.team_id = t0.team_id;

insert into season_def_rankings
(
	season_year
	, team_id
	, avg
	, def_pts
	, def_pass_att
	, def_pass_cmp
	, def_pass_yds
	, def_pass_tds
	, def_int
	, def_rush_att
	, def_rush_yds
	, def_rush_tds
	, def_fumble
	, def_targets
	, def_rec
	, def_rec_yds
	, def_rec_tds
	, def_yac
	, def_sack
	, def_block
	, def_safety
	, def_tds
)
select g.season_year
	, t.team_id
	, True
	, 0
	, round(avg(t0.def_pass_att), 2) as def_pass_att
	, round(avg(t0.def_pass_cmp), 2) as def_pass_cmp
	, round(avg(t0.def_pass_yds), 2) as def_pass_yds
	, round(avg(t0.def_pass_tds), 2) as def_pass_tds
	, round(avg(t1.def_int), 4) as def_int
	, round(avg(t0.def_rush_att), 2) as def_rush_att
	, round(avg(t0.def_rush_yds), 2) as def_rush_yds
	, round(avg(t0.def_rush_tds), 2) as def_rush_tds
	, round(avg(t1.def_fumble), 4) as def_fumble
	, round(avg(t0.def_targets), 2) as def_targets
	, round(avg(t0.def_rec), 2) as def_rec
	, round(avg(t0.def_rec_yds), 2) as def_rec_yds
	, round(avg(t0.def_rec_tds), 2) as def_rec_tds
	, round(avg(t0.def_yac), 2) as def_yac
	, round(cast(avg(t1.def_sack) as numeric), 4) as def_sack
	, round(avg(t1.def_block), 4) as def_block
	, round(avg(t1.def_safety), 4) as def_safety
	, round(avg(t1.def_tds), 4) as def_tds
from public.team as t
	join public.game as g on t.team_id = g.away_team or t.team_id = g.home_team
	join (
		select pp.gsis_id
			, pp.team
			, sum(pp.passing_att) as def_pass_att
			, sum(pp.passing_cmp) as def_pass_cmp
			, sum(pp.passing_yds) as def_pass_yds
			, sum(pp.passing_tds) as def_pass_tds
			, sum(pp.rushing_att) as def_rush_att
			, sum(pp.rushing_yds) as def_rush_yds
			, sum(pp.rushing_tds) as def_rush_tds
			, sum(pp.receiving_tar) as def_targets
			, sum(pp.receiving_rec) as def_rec
			, sum(pp.receiving_yds) as def_rec_yds
			, sum(pp.receiving_tds) as def_rec_tds
			, sum(pp.receiving_yac_yds) as def_yac
		from public.play_player as pp
		group by pp.gsis_id, pp.team
	) as t0 on g.gsis_id = t0.gsis_id
		and t0.team != t.team_id
	join (
		select pp.gsis_id
			, pp.team
			, sum(pp.defense_int) as def_int
			, sum(pp.defense_frec) as def_fumble
			, sum(pp.defense_sk) as def_sack
			, sum(pp.defense_fgblk + pp.defense_puntblk + pp.defense_xpblk) as def_block
			, sum(pp.defense_safe) as def_safety
			, sum(pp.defense_frec_tds + pp.defense_int_tds + pp.defense_misc_tds + pp.kickret_tds + pp.puntret_tds) as def_tds
		from public.play_player as pp
		group by pp.gsis_id, pp.team
	) as t1 on g.gsis_id = t1.gsis_id
		and t1.team = t.team_id
group by g.season_year, t.team_id;

--Updates the defensive points for each team
update season_def_rankings
set def_pts = round(t0.pts, 4)
from (
	select g.season_year
		, t.team_id
		--Score can be either home or away
		, avg(case when t.team_id = g.home_team then g.away_score else g.home_score end) as pts
	from public.team as t
	join public.game as g on g.home_team = t.team_id or g.away_team = t.team_id
	where g.finished = 't'
	group by g.season_year, t.team_id
) as t0
where season_def_rankings.season_year = t0.season_year and season_def_rankings.team_id = t0.team_id;

--Updates the offensive stats for each team to be the amount of standard deviations away from the average
--Calculated by ((team_average - league_average) / league_std_deviation)
--More negative numbers are worse performing teams and more positive numbers are better performing
insert into season_off_rankings
(
	season_year,
	team_id,
	avg,
	off_pts,
	off_pass_yds,
	off_pass_tds,
	off_rush_yds,
	off_rush_tds,
	off_int,
	off_fumble,
	off_sack
)
--Calculate offensive stats relative to league averages and standard deviations
select sor.season_year
	, sor.team_id
	, False
	, round(cast( (sor.off_pts - avg.pts ) / std.pts as numeric), 4) as pts
	, round(cast( (sor.off_pass_yds - avg.pass_yds ) / std.pass_yds as numeric), 4) as pass_yds
	, round(cast( (sor.off_pass_tds - avg.pass_tds ) / std.pass_tds as numeric), 4) as pass_tds
	, round(cast( (sor.off_rush_yds - avg.rush_yds ) / std.rush_yds as numeric), 4) as rush_yds
	, round(cast( (sor.off_rush_tds - avg.rush_tds ) / std.rush_tds as numeric), 4) as rush_tds
	, round(cast( (sor.off_int - avg.int ) / std.int as numeric), 4) as int
	, round(cast( (sor.off_fumble - avg.fumble ) / std.fumble as numeric), 4) as fumble
	, round(cast( (sor.off_sack - avg.sack ) / std.sack as numeric), 4) as sack
from season_off_rankings as sor
join (
	--Calculate the standard deviation for each season
	select season_year
		, 'UNK'
		, stddev(off_pts) as pts
		, stddev(off_pass_yds) as pass_yds
		, stddev(off_pass_tds) as pass_tds
		, stddev(off_rush_yds) as rush_yds
		, stddev(off_rush_tds) as rush_tds
		, stddev(off_int) as int
		, stddev(off_fumble) as fumble
		, stddev(off_sack) as sack
	from season_off_rankings
	group by season_year
) as std on sor.season_year = std.season_year
join (
	--Calculate the league average for each season
	select season_year
		, 'UNK'
		, avg(off_pts) as pts
		, avg(off_pass_yds) as pass_yds
		, avg(off_pass_tds) as pass_tds
		, avg(off_rush_yds) as rush_yds
		, avg(off_rush_tds) as rush_tds
		, avg(off_int) as int
		, avg(off_fumble) as fumble
		, avg(off_sack) as sack
	from season_off_rankings
	group by season_year
) as avg on sor.season_year = avg.season_year;

--Updates the offensive stats for each team to be the amount of standard deviations away from the average
--Calculated by ((team_average - league_average) / league_std_deviation)
--More negative numbers are worse performing teams and more positive numbers are better performing
insert into season_off_rankings
(
	season_year,
	team_id,
	avg,
	off_pts,
	off_pass_yds,
	off_pass_tds,
	off_rush_yds,
	off_rush_tds,
	off_int,
	off_fumble,
	off_sack
)
--Calculate the standard deviation for each season
select season_year
	, 'UNK'
	, False
	, round(cast(stddev(sor.off_pts) as numeric), 4)
	, round(cast(stddev(sor.off_pass_yds) as numeric), 4)
	, round(cast(stddev(sor.off_pass_tds) as numeric), 4)
	, round(cast(stddev(sor.off_rush_yds) as numeric), 4)
	, round(cast(stddev(sor.off_rush_tds) as numeric), 4)
	, round(cast(stddev(sor.off_int) as numeric), 4)
	, round(cast(stddev(sor.off_fumble) as numeric), 4)
	, round(cast(stddev(sor.off_sack) as numeric), 4)
from season_off_rankings as sor
where sor.avg = True
group by sor.season_year;


--Updates the defensive stats for each team to be relative to the league average for the season
--Calculated by ((team_average - league_average) / league_std_deviation)
--More negative numbers are worse performing teams and more positive numbers are better performing
insert into season_def_rankings
(
	season_year
	, team_id
	, avg
	, def_pts
	, def_pass_att
	, def_pass_cmp
	, def_pass_yds
	, def_pass_tds
	, def_int
	, def_rush_att
	, def_rush_yds
	, def_rush_tds
	, def_fumble
	, def_targets
	, def_rec
	, def_rec_yds
	, def_rec_tds
	, def_yac
	, def_sack
	, def_block
	, def_safety
	, def_tds
)
--Calculate defensive stats relative to league averages
select sdr.season_year
	, sdr.team_id
	, False
	, round(cast((sdr.def_pts - avg.pts) * 1.0 / std.pts as numeric), 4) as pts
	, round(cast((sdr.def_pass_att - avg.pass_att) * 1.0 / std.pass_att as numeric), 4) as pass_att
	, round(cast((sdr.def_pass_cmp - avg.pass_cmp) * 1.0 / std.pass_cmp as numeric), 4) as pass_cmp
	, round(cast((sdr.def_pass_yds - avg.pass_yds) * 1.0 / std.pass_yds as numeric), 4) as pass_yds
	, round(cast((sdr.def_pass_tds - avg.pass_tds) * 1.0 / std.pass_tds as numeric), 4) as pass_tds
	, round(cast((sdr.def_int - avg.int) * 1.0 / std.int as numeric), 4) as int
	, round(cast((sdr.def_rush_att - avg.rush_att) * 1.0 / std.rush_att as numeric), 4) as rush_att
	, round(cast((sdr.def_rush_yds - avg.rush_yds) * 1.0 / std.rush_yds as numeric), 4) as rush_yds
	, round(cast((sdr.def_rush_tds - avg.rush_tds) * 1.0 / std.rush_tds as numeric), 4) as rush_tds
	, round(cast((sdr.def_fumble - avg.fumble) * 1.0 / std.fumble as numeric), 4) as fumble
	, round(cast((sdr.def_targets - avg.targets) * 1.0 / std.targets as numeric), 4) as targets
	, round(cast((sdr.def_rec - avg.rec) * 1.0 / std.rec as numeric), 4) as rec
	, round(cast((sdr.def_rec_yds - avg.rec_yds) * 1.0 / std.rec_yds as numeric), 4) as rec_yds
	, round(cast((sdr.def_rec_tds - avg.rec_tds) * 1.0 / std.rec_tds as numeric), 4) as rec_tds
	, round(cast((sdr.def_yac - avg.yac) * 1.0 / std.yac as numeric), 4) as yac
	, round(cast((sdr.def_sack - avg.sack) * 1.0 / std.sack as numeric), 4) as sack
	, round(cast((sdr.def_block - avg.block) * 1.0 / std.block as numeric), 4) as block
	, round(cast((sdr.def_safety - avg.safety) * 1.0 / std.safety as numeric), 4) as safety
	, round(cast((sdr.def_tds - avg.tds) * 1.0 / std.tds as numeric), 4) as tds
from season_def_rankings as sdr
join (
	--Calculate the standard dev for each season
	select season_year
		, stddev(def_pts) as pts
		, stddev(def_pass_att) as pass_att
		, stddev(def_pass_cmp) as pass_cmp
		, stddev(def_pass_yds) as pass_yds
		, stddev(def_pass_tds) as pass_tds
		, stddev(def_int) as int
		, stddev(def_rush_att) as rush_att
		, stddev(def_rush_yds) as rush_yds
		, stddev(def_rush_tds) as rush_tds
		, stddev(def_fumble) as fumble
		, stddev(def_targets) as targets
		, stddev(def_rec) as rec
		, stddev(def_rec_yds) as rec_yds
		, stddev(def_rec_tds) as rec_tds
		, stddev(def_yac) as yac
		, stddev(def_sack) as sack
		, stddev(def_block) as block
		, stddev(def_safety) as safety
		, stddev(def_tds) as tds
	from season_def_rankings
	group by season_year
) as std on std.season_year = sdr.season_year
join (
	--Calculate the league average for each season
	select season_year
		, avg(def_pts) as pts
		, avg(def_pass_att) as pass_att
		, avg(def_pass_cmp) as pass_cmp
		, avg(def_pass_yds) as pass_yds
		, avg(def_pass_tds) as pass_tds
		, avg(def_int) as int
		, avg(def_rush_att) as rush_att
		, avg(def_rush_yds) as rush_yds
		, avg(def_rush_tds) as rush_tds
		, avg(def_fumble) as fumble
		, avg(def_targets) as targets
		, avg(def_rec) as rec
		, avg(def_rec_yds) as rec_yds
		, avg(def_rec_tds) as rec_tds
		, avg(def_yac) as yac
		, avg(def_sack) as sack
		, avg(def_block) as block
		, avg(def_safety) as safety
		, avg(def_tds) as tds
	from season_def_rankings
	group by season_year
) as avg on avg.season_year = sdr.season_year;

insert into season_def_rankings
(
	season_year
	, team_id
	, avg
	, def_pts
	, def_pass_att
	, def_pass_cmp
	, def_pass_yds
	, def_pass_tds
	, def_int
	, def_rush_att
	, def_rush_yds
	, def_rush_tds
	, def_fumble
	, def_targets
	, def_rec
	, def_rec_yds
	, def_rec_tds
	, def_yac
	, def_sack
	, def_block
	, def_safety
	, def_tds
)
select season_year
	, 'UNK'
	, False
	, round(cast(stddev(sor.def_pts) as numeric), 4)
	, round(cast(stddev(def_pass_att) as numeric), 4)
	, round(cast(stddev(def_pass_cmp) as numeric), 4)
	, round(cast(stddev(def_pass_yds) as numeric), 4)
	, round(cast(stddev(def_pass_tds) as numeric), 4)
	, round(cast(stddev(def_int) as numeric), 4)
	, round(cast(stddev(def_rush_att) as numeric), 4)
	, round(cast(stddev(def_rush_yds) as numeric), 4)
	, round(cast(stddev(def_rush_tds) as numeric), 4)
	, round(cast(stddev(def_fumble) as numeric), 4)
	, round(cast(stddev(def_targets) as numeric), 4)
	, round(cast(stddev(def_rec) as numeric), 4)
	, round(cast(stddev(def_rec_yds) as numeric), 4)
	, round(cast(stddev(def_rec_tds) as numeric), 4)
	, round(cast(stddev(def_yac) as numeric), 4)
	, round(cast(stddev(def_sack) as numeric), 4)
	, round(cast(stddev(def_block) as numeric), 4)
	, round(cast(stddev(def_safety) as numeric), 4)
	, round(cast(stddev(def_tds) as numeric), 4)
from season_def_rankings as sor
where sor.avg = True
group by sor.season_year;

insert into public.season_rankings
(
	season_year
	, team_id
	, avg
	, off_pts
	, off_pass_yds
	, off_pass_tds
	, off_rush_yds
	, off_rush_tds
	, off_int
	, off_fumble
	, off_sack
	, def_pts
	, def_pass_att
	, def_pass_cmp
	, def_pass_yds
	, def_pass_tds
	, def_int
	, def_rush_att
	, def_rush_yds
	, def_rush_tds
	, def_fumble
	, def_targets
	, def_rec
	, def_rec_yds
	, def_rec_tds
	, def_yac
	, def_sack
	, def_block
	, def_safety
	, def_tds
)
select sor.season_year
	, sor.team_id
	, sor.avg
	, sor.off_pts
	, sor.off_pass_yds
	, sor.off_pass_tds
	, sor.off_rush_yds
	, sor.off_rush_tds
	, sor.off_int
	, sor.off_fumble
	, sor.off_sack
	, sdr.def_pts
	, sdr.def_pass_att
	, sdr.def_pass_cmp
	, sdr.def_pass_yds
	, sdr.def_pass_tds
	, sdr.def_int
	, sdr.def_rush_att
	, sdr.def_rush_yds
	, sdr.def_rush_tds
	, sdr.def_fumble
	, sdr.def_targets
	, sdr.def_rec
	, sdr.def_rec_yds
	, sdr.def_rec_tds
	, sdr.def_yac
	, sdr.def_sack
	, sdr.def_block
	, sdr.def_safety
	, sdr.def_tds
from season_off_rankings as sor
	join season_def_rankings as sdr on sor.team_id = sdr.team_id and sor.season_year = sdr.season_year and sor.avg = sdr.avg