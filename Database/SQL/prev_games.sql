CREATE OR REPLACE FUNCTION prev_games(player varchar(10), game varchar(10), team varchar(3))
RETURNS TABLE
(
	gsis_id varchar(10),
	team_id character varying(3),
	player_id character varying(10),
	prev_amount character varying(10),
	"position" player_pos,
	pass_att real,
	pass_cmp real,
	pass_yds real,
	pass_tds real,
	"int" real,
	rush_att real,
	rush_yds real,
	fumble real,
	targets real,
	rec real,
	rec_yds real,
	yac real,
	ret_yds real,
	td real,
	block_kick real,
	safety real,
	sack real,
	pts_allowed real,
	fg_50 real,
	fg_40 real,
	fg_0 real,
	pat real,
	fg_miss real,
	points real
) AS $$
	DECLARE gsis_id_var varchar(10);
	DECLARE season_year_var int;
	DECLARE position_var player_pos;
BEGIN
	CREATE TEMP TABLE fantasy_prev_temp
	(
		gsis_id character varying(10),
		team_id character varying(3),
		player_id character varying(10),
		prev_amount character varying(10),
		"position" player_pos,
		pass_att real,
		pass_cmp real,
		pass_yds real,
		pass_tds real,
		"int" real,
		rush_att real,
		rush_yds real,
		fumble real,
		targets real,
		rec real,
		rec_yds real,
		yac real,
		ret_yds real,
		td real,
		block_kick real,
		safety real,
		sack real,
		pts_allowed real,
		fg_50 real,
		fg_40 real,
		fg_0 real,
		pat real,
		fg_miss real,
		points real
	) ON COMMIT DROP;
	
	IF player = '' and team = '' THEN
		RETURN QUERY SELECT * from fantasy_prev_temp;
	END IF;
	
	IF player != '' THEN
		SELECT t0.team, t0.position INTO team, position_var
		FROM public.player as t0
		WHERE t0.player_id = player;
	END IF;

	IF game = '' THEN
		SELECT t0.gsis_id, t0.season_year INTO gsis_id_var, season_year_var
		FROM public.game as t0
		WHERE team IN (t0.home_team, t0.away_team)
			AND finished = 'f'
		ORDER BY season_year, week
		LIMIT 1;
	ELSE
		SELECT t0.gsis_id, t0.season_year INTO gsis_id_var, season_year_var
		FROM public.game as t0
		WHERE t0.gsis_id = game
		ORDER BY season_year, week
		LIMIT 1;
	END IF;

	IF player != '' THEN
		INSERT INTO fantasy_prev_temp
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
		SELECT g.gsis_id,
			team,
			player,
			'',
			position_var,
			case when fantasy.gsis_id is not null then fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att else 0 end,
			case when fantasy.gsis_id is not null then fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp else 0 end,
			case when fantasy.gsis_id is not null then fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.int - sr1.def_int * sr2.def_int else 0 end,
			case when fantasy.gsis_id is not null then fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att else 0 end,
			case when fantasy.gsis_id is not null then fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.fumble - sr1.def_fumble * sr2.def_fumble else 0 end,
			case when fantasy.gsis_id is not null then fantasy.targets - sr1.def_targets * sr2.def_targets else 0 end,
			case when fantasy.gsis_id is not null then fantasy.rec - sr1.def_rec * sr2.def_rec else 0 end,
			case when fantasy.gsis_id is not null then fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.yac - sr1.def_yac * sr2.def_yac else 0 end,
			case when fantasy.gsis_id is not null then fantasy.ret_yds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds else 0 end,
			case when fantasy.gsis_id is not null then fantasy.block_kick else 0 end,
			case when fantasy.gsis_id is not null then fantasy.safety else 0 end,
			case when fantasy.gsis_id is not null then fantasy.sack else 0 end,
			case when fantasy.gsis_id is not null then fantasy.pts_allowed else 0 end,
			case when fantasy.gsis_id is not null then fantasy.fg_50 else 0 end,
			case when fantasy.gsis_id is not null then fantasy.fg_40 else 0 end,
			case when fantasy.gsis_id is not null then fantasy.fg_0 else 0 end,
			case when fantasy.gsis_id is not null then fantasy.pat else 0 end,
			case when fantasy.gsis_id is not null then fantasy.fg_miss else 0 end,
			case when fantasy.gsis_id is not null then fantasy.points else 0 end
		FROM public.fantasy
			RIGHT OUTER JOIN public.game as g on fantasy.gsis_id = g.gsis_id and fantasy.player_id = player
			JOIN public.season_rankings as sr1
				ON sr1.season_year = g.season_year
					AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
					AND sr1.avg = 'f'
			JOIN public.season_rankings as sr2
				ON sr2.season_year = g.season_year
					AND sr2.team_id = 'UNK'
					AND sr2.avg = 'f'
		WHERE g.gsis_id < gsis_id_var
			and (fantasy.gsis_id is not null or team in (g.home_team, g.away_team))
			and (fantasy.gsis_id is not null or g.season_year = (SELECT max(season_year) FROM public.game) and g.season_type != 'Preseason');

		INSERT INTO fantasy_prev_temp
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
		SELECT gsis_id_var,
			t0.team_id,
			t0.player_id,
			'prev2',
			t0.position,
			avg(t0.pass_att),
			avg(t0.pass_cmp),
			avg(t0.pass_yds),
			avg(t0.pass_tds),
			avg(t0.int),
			avg(t0.rush_att),
			avg(t0.rush_yds),
			avg(t0.fumble),
			avg(t0.targets),
			avg(t0.rec),
			avg(t0.rec_yds),
			avg(t0.yac),
			avg(t0.ret_yds),
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			avg(t0.fg_50),
			avg(t0.fg_40),
			avg(t0.fg_0),
			avg(t0.pat),
			avg(t0.fg_miss),
			avg(t0.points)
		FROM 
		(
			SELECT *
			FROM fantasy_prev_temp
			WHERE fantasy_prev_temp.gsis_id != gsis_id_var
			ORDER BY fantasy_prev_temp.gsis_id DESC
			LIMIT 2
		) as t0
		GROUP BY t0.team_id, t0.player_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			t0.player_id,
			'prev5',
			t0.position,
			avg(t0.pass_att),
			avg(t0.pass_cmp),
			avg(t0.pass_yds),
			avg(t0.pass_tds),
			avg(t0.int),
			avg(t0.rush_att),
			avg(t0.rush_yds),
			avg(t0.fumble),
			avg(t0.targets),
			avg(t0.rec),
			avg(t0.rec_yds),
			avg(t0.yac),
			avg(t0.ret_yds),
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			avg(t0.fg_50),
			avg(t0.fg_40),
			avg(t0.fg_0),
			avg(t0.pat),
			avg(t0.fg_miss),
			avg(t0.points)
		FROM 
		(
			SELECT *
			FROM fantasy_prev_temp
			WHERE fantasy_prev_temp.gsis_id != gsis_id_var
			ORDER BY fantasy_prev_temp.gsis_id DESC
			LIMIT 5
		) as t0
		GROUP BY t0.team_id, t0.player_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			t0.player_id,
			'season',
			t0.position,
			avg(t0.pass_att),
			avg(t0.pass_cmp),
			avg(t0.pass_yds),
			avg(t0.pass_tds),
			avg(t0.int),
			avg(t0.rush_att),
			avg(t0.rush_yds),
			avg(t0.fumble),
			avg(t0.targets),
			avg(t0.rec),
			avg(t0.rec_yds),
			avg(t0.yac),
			avg(t0.ret_yds),
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			avg(t0.fg_50),
			avg(t0.fg_40),
			avg(t0.fg_0),
			avg(t0.pat),
			avg(t0.fg_miss),
			avg(t0.points)
		FROM fantasy_prev_temp as t0
			JOIN public.game as g on t0.gsis_id = g.gsis_id
		WHERE t0.gsis_id != gsis_id_var
			and g.season_year = season_year_var
		GROUP BY t0.team_id, t0.player_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			t0.player_id,
			'prevseason',
			t0.position,
			avg(t0.pass_att),
			avg(t0.pass_cmp),
			avg(t0.pass_yds),
			avg(t0.pass_tds),
			avg(t0.int),
			avg(t0.rush_att),
			avg(t0.rush_yds),
			avg(t0.fumble),
			avg(t0.targets),
			avg(t0.rec),
			avg(t0.rec_yds),
			avg(t0.yac),
			avg(t0.ret_yds),
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			avg(t0.fg_50),
			avg(t0.fg_40),
			avg(t0.fg_0),
			avg(t0.pat),
			avg(t0.fg_miss),
			avg(t0.points)
		FROM fantasy_prev_temp as t0
			JOIN public.game as g on t0.gsis_id = g.gsis_id
		WHERE t0.gsis_id != gsis_id_var
			and g.season_year = season_year_var - 1
		GROUP BY t0.team_id, t0.player_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			t0.player_id,
			'career',
			t0.position,
			avg(t0.pass_att),
			avg(t0.pass_cmp),
			avg(t0.pass_yds),
			avg(t0.pass_tds),
			avg(t0.int),
			avg(t0.rush_att),
			avg(t0.rush_yds),
			avg(t0.fumble),
			avg(t0.targets),
			avg(t0.rec),
			avg(t0.rec_yds),
			avg(t0.yac),
			avg(t0.ret_yds),
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			avg(t0.fg_50),
			avg(t0.fg_40),
			avg(t0.fg_0),
			avg(t0.pat),
			avg(t0.fg_miss),
			avg(t0.points)
		FROM fantasy_prev_temp as t0
		WHERE t0.gsis_id != gsis_id_var
		GROUP BY t0.team_id, t0.player_id, t0.position;
	else
		INSERT INTO fantasy_prev_temp
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
		SELECT fantasy.gsis_id,
			fantasy.team_id,
			'',
			'',
			fantasy.position,
			0,
			0,
			0,
			0,
			fantasy.int - sr1.off_int * sr2.off_int,
			0,
			0,
			fantasy.fumble - sr1.off_fumble * sr2.off_fumble,
			0,
			0,
			0,
			0,
			0,
			fantasy.td,
			fantasy.block_kick,
			fantasy.safety,
			fantasy.sack - sr1.off_sack * sr2.off_sack,
			fantasy.pts_allowed - sr1.off_pts * sr2.off_pts,
			0,
			0,
			0,
			0,
			0,
			fantasy.points
		FROM public.fantasy
			JOIN public.game as g on fantasy.gsis_id = g.gsis_id
			JOIN public.season_rankings as sr1
				ON sr1.season_year = g.season_year
					AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
					AND sr1.avg = 'f'
			JOIN public.season_rankings as sr2
				ON sr2.season_year = g.season_year
					AND sr2.team_id = 'UNK'
					AND sr2.avg = 'f'
		WHERE fantasy.team_id = team
			AND fantasy.position = 'DEF'
			AND fantasy.gsis_id < gsis_id_var;

		INSERT INTO fantasy_prev_temp
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
		SELECT gsis_id_var,
			t0.team_id,
			'',
			'prev2',
			t0.position,
			0,
			0,
			0,
			0,
			avg(t0.int),
			0,
			0,
			avg(t0.fumble),
			0,
			0,
			0,
			0,
			0,
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			0,
			0,
			0,
			0,
			0,
			avg(t0.points)
		FROM
		(
			SELECT *
			FROM fantasy_prev_temp
			WHERE fantasy_prev_temp.gsis_id != gsis_id_var
			ORDER BY fantasy_prev_temp.gsis_id DESC
			LIMIT 2
		) as t0
		GROUP BY t0.team_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			'',
			'prev5',
			t0.position,
			0,
			0,
			0,
			0,
			avg(t0.int),
			0,
			0,
			avg(t0.fumble),
			0,
			0,
			0,
			0,
			0,
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			0,
			0,
			0,
			0,
			0,
			avg(t0.points)
		FROM 
		(
			SELECT *
			FROM fantasy_prev_temp
			WHERE fantasy_prev_temp.gsis_id !=gsis_id_var
			ORDER BY fantasy_prev_temp.gsis_id DESC
			LIMIT 5
		) as t0
		GROUP BY t0.team_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			'',
			'season',
			t0.position,
			0,
			0,
			0,
			0,
			avg(t0.int),
			0,
			0,
			avg(t0.fumble),
			0,
			0,
			0,
			0,
			0,
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			0,
			0,
			0,
			0,
			0,
			avg(t0.points)
		FROM fantasy_prev_temp as t0
			JOIN public.game as g on t0.gsis_id = g.gsis_id
		WHERE t0.gsis_id != gsis_id_var
			and g.season_year = season_year_var
		GROUP BY t0.team_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			'',
			'prevseason',
			t0.position,
			0,
			0,
			0,
			0,
			avg(t0.int),
			0,
			0,
			avg(t0.fumble),
			0,
			0,
			0,
			0,
			0,
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			0,
			0,
			0,
			0,
			0,
			avg(t0.points)
		FROM fantasy_prev_temp as t0
			JOIN public.game as g on t0.gsis_id = g.gsis_id
		WHERE t0.gsis_id != gsis_id_var
			and g.season_year = season_year_var - 1
		GROUP BY t0.team_id, t0.position
		UNION
		SELECT gsis_id_var,
			t0.team_id,
			'',
			'career',
			t0.position,
			0,
			0,
			0,
			0,
			avg(t0.int),
			0,
			0,
			avg(t0.fumble),
			0,
			0,
			0,
			0,
			0,
			avg(t0.td),
			avg(t0.block_kick),
			avg(t0.safety),
			avg(t0.sack),
			avg(t0.pts_allowed),
			0,
			0,
			0,
			0,
			0,
			avg(t0.points)
		FROM fantasy_prev_temp as t0
		WHERE t0.gsis_id != gsis_id_var
		GROUP BY t0.team_id, t0.position;
	end if;

	DELETE
	FROM fantasy_prev_temp as t0
	WHERE t0.prev_amount = '';

	UPDATE fantasy_prev_temp
	SET points = (
		t0.pass_yds / 25.0
		+ t0.pass_tds * 4.0
		- t0.int * 2.0
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.td * 6.0
	)
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'QB'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;

	UPDATE fantasy_prev_temp
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'RB'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;


	UPDATE fantasy_prev_temp
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'WR'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;

	UPDATE fantasy_prev_temp
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'TE'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;

	UPDATE fantasy_prev_temp
	SET points = (
		+ t0.fg_50 * 5.0
		+ t0.fg_40 * 4.0
		+ t0.fg_0 * 3.0
		+ t0.pat * 1.0
		- t0.fg_miss * 1.0
	)
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'K'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;

	UPDATE fantasy_prev_temp
	SET points = (
		+ t0.int * 2.0
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
	FROM fantasy_prev_temp as t0
	WHERE fantasy_prev_temp.position = 'DEF'
		and fantasy_prev_temp.prev_amount = t0.prev_amount;

	RETURN QUERY
	SELECT
		t0.gsis_id,
		t0.team_id,
		t0.player_id,
		t0.prev_amount,
		t0.position,
		t0.pass_att,
		t0.pass_cmp,
		t0.pass_yds,
		t0.pass_tds,
		t0.int,
		t0.rush_att,
		t0.rush_yds,
		t0.fumble,
		t0.targets,
		t0.rec,
		t0.rec_yds,
		t0.yac,
		t0.ret_yds,
		t0.td,
		t0.block_kick,
		t0.safety,
		t0.sack,
		t0.pts_allowed,
		t0.fg_50,
		t0.fg_40,
		t0.fg_0,
		t0.pat,
		t0.fg_miss,
		t0.points
	FROM fantasy_prev_temp as t0;
end;
$$ LANGUAGE plpgsql