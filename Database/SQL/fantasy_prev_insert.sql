CREATE OR REPLACE FUNCTION fantasy_prev_insert()
RETURNS void AS $$
DECLARE fantasy_cursor_off cursor FOR
	SELECT fantasy.player_id
		, fantasy.gsis_id
		, game.season_year
	FROM public.fantasy
		join public.game on fantasy.gsis_id = game.gsis_id
	WHERE
		fantasy.position != 'DEF';
DECLARE fantasy_cursor_def cursor FOR
	SELECT fantasy.team_id
		, fantasy.gsis_id
		, game.season_year
	FROM public.fantasy
		join public.game on fantasy.gsis_id = game.gsis_id
	WHERE
		fantasy.position = 'DEF';
begin
	CREATE TEMP TABLE fantasy_prev_off
	(
		gsis_id gameid,
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

	CREATE TEMP TABLE fantasy_prev_def
	(
		gsis_id gameid,
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

	FOR fantasy_row in fantasy_cursor_off loop
		begin
			INSERT INTO fantasy_prev_off
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'prev2',
				fantasy.position,
				fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att,
				fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp,
				fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds,
				fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds,
				fantasy.int - sr1.def_int * sr2.def_int,
				fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att,
				fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds,
				fantasy.fumble - sr1.def_fumble * sr2.def_fumble,
				fantasy.targets - sr1.def_targets * sr2.def_targets,
				fantasy.rec - sr1.def_rec * sr2.def_rec,
				fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds,
				fantasy.yac - sr1.def_yac * sr2.def_yac,
				fantasy.ret_yds,
				fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds,
				fantasy.block_kick,
				fantasy.safety,
				fantasy.sack,
				fantasy.pts_allowed,
				fantasy.fg_50,
				fantasy.fg_40,
				fantasy.fg_0,
				fantasy.pat,
				fantasy.fg_miss,
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
			WHERE fantasy.player_id = fantasy_row.player_id
				AND fantasy.gsis_id < fantasy_row.gsis_id
			ORDER BY fantasy.gsis_id DESC
			LIMIT 2;

			INSERT INTO fantasy_prev_off
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'prev5',
				fantasy.position,
				fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att,
				fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp,
				fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds,
				fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds,
				fantasy.int - sr1.def_int * sr2.def_int,
				fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att,
				fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds,
				fantasy.fumble - sr1.def_fumble * sr2.def_fumble,
				fantasy.targets - sr1.def_targets * sr2.def_targets,
				fantasy.rec - sr1.def_rec * sr2.def_rec,
				fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds,
				fantasy.yac - sr1.def_yac * sr2.def_yac,
				fantasy.ret_yds,
				fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds,
				fantasy.block_kick,
				fantasy.safety,
				fantasy.sack,
				fantasy.pts_allowed,
				fantasy.fg_50,
				fantasy.fg_40,
				fantasy.fg_0,
				fantasy.pat,
				fantasy.fg_miss,
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
			WHERE fantasy.player_id = fantasy_row.player_id
				AND fantasy.gsis_id < fantasy_row.gsis_id
			ORDER BY fantasy.gsis_id DESC
			LIMIT 5;

			INSERT INTO fantasy_prev_off
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'season',
				fantasy.position,
				cast(avg(fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att) as real),
				cast(avg(fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp) as real),
				cast(avg(fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds) as real),
				cast(avg(fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds) as real),
				cast(avg(fantasy.int - sr1.def_int * sr2.def_int) as real),
				cast(avg(fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att) as real),
				cast(avg(fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds) as real),
				cast(avg(fantasy.fumble - sr1.def_fumble * sr2.def_fumble) as real),
				cast(avg(fantasy.targets - sr1.def_targets * sr2.def_targets) as real),
				cast(avg(fantasy.rec - sr1.def_rec * sr2.def_rec) as real),
				cast(avg(fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds) as real),
				cast(avg(fantasy.yac - sr1.def_yac * sr2.def_yac) as real),
				cast(avg(fantasy.ret_yds) as real),
				cast(avg(fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack) as real),
				cast(avg(fantasy.pts_allowed) as real),
				cast(avg(fantasy.fg_50) as real),
				cast(avg(fantasy.fg_40) as real),
				cast(avg(fantasy.fg_0) as real),
				cast(avg(fantasy.pat) as real),
				cast(avg(fantasy.fg_miss) as real),
				cast(avg(fantasy.points) as real)
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
			WHERE g.season_year = fantasy_row.season_year
				and fantasy.player_id = fantasy_row.player_id
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;

			INSERT INTO fantasy_prev_off
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'prevseason',
				fantasy.position,
				cast(avg(fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att) as real),
				cast(avg(fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp) as real),
				cast(avg(fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds) as real),
				cast(avg(fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds) as real),
				cast(avg(fantasy.int - sr1.def_int * sr2.def_int) as real),
				cast(avg(fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att) as real),
				cast(avg(fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds) as real),
				cast(avg(fantasy.fumble - sr1.def_fumble * sr2.def_fumble) as real),
				cast(avg(fantasy.targets - sr1.def_targets * sr2.def_targets) as real),
				cast(avg(fantasy.rec - sr1.def_rec * sr2.def_rec) as real),
				cast(avg(fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds) as real),
				cast(avg(fantasy.yac - sr1.def_yac * sr2.def_yac) as real),
				cast(avg(fantasy.ret_yds) as real),
				cast(avg(fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack) as real),
				cast(avg(fantasy.pts_allowed) as real),
				cast(avg(fantasy.fg_50) as real),
				cast(avg(fantasy.fg_40) as real),
				cast(avg(fantasy.fg_0) as real),
				cast(avg(fantasy.pat) as real),
				cast(avg(fantasy.fg_miss) as real),
				cast(avg(fantasy.points) as real)
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
			WHERE g.season_year = fantasy_row.season_year - 1
				and fantasy.player_id = fantasy_row.player_id
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;

			INSERT INTO fantasy_prev_off
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'career',
				fantasy.position,
				cast(avg(fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att) as real),
				cast(avg(fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp) as real),
				cast(avg(fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds) as real),
				cast(avg(fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds) as real),
				cast(avg(fantasy.int - sr1.def_int * sr2.def_int) as real),
				cast(avg(fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att) as real),
				cast(avg(fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds) as real),
				cast(avg(fantasy.fumble - sr1.def_fumble * sr2.def_fumble) as real),
				cast(avg(fantasy.targets - sr1.def_targets * sr2.def_targets) as real),
				cast(avg(fantasy.rec - sr1.def_rec * sr2.def_rec) as real),
				cast(avg(fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds) as real),
				cast(avg(fantasy.yac - sr1.def_yac * sr2.def_yac) as real),
				cast(avg(fantasy.ret_yds) as real),
				cast(avg(fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack) as real),
				cast(avg(fantasy.pts_allowed) as real),
				cast(avg(fantasy.fg_50) as real),
				cast(avg(fantasy.fg_40) as real),
				cast(avg(fantasy.fg_0) as real),
				cast(avg(fantasy.pat) as real),
				cast(avg(fantasy.fg_miss) as real),
				cast(avg(fantasy.points) as real)
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
			WHERE fantasy.player_id = fantasy_row.player_id
				and g.gsis_id < fantasy_row.gsis_id
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;
		end;
	end loop;
	FOR fantasy_row in fantasy_cursor_def loop
		begin
			INSERT INTO fantasy_prev_def
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				'',
				'prev2',
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
			WHERE fantasy.team_id = fantasy_row.team_id
				AND fantasy.position = 'DEF'
				AND fantasy.gsis_id < fantasy_row.gsis_id
			ORDER BY fantasy.gsis_id DESC
			LIMIT 2;

			INSERT INTO fantasy_prev_def
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'prev5',
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
			WHERE fantasy.team_id = fantasy_row.team_id
				AND fantasy.position = 'DEF'
				AND fantasy.gsis_id < fantasy_row.gsis_id
			ORDER BY fantasy.gsis_id DESC
			LIMIT 5;

			INSERT INTO fantasy_prev_def
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				fantasy.player_id,
				'season',
				fantasy.position,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.int - sr1.off_int * sr2.off_int) as real),
				0,
				0,
				cast(avg(fantasy.fumble - sr1.off_fumble * sr2.off_fumble) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.td) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack - sr1.off_sack * sr2.off_sack) as real),
				cast(avg(fantasy.pts_allowed - sr1.off_pts * sr2.off_pts) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.points) as real)
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
			WHERE fantasy.team_id = fantasy_row.team_id
				AND fantasy.position = 'DEF'
				AND g.season_year = fantasy_row.season_year
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;

			INSERT INTO fantasy_prev_def
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				'',
				'prevseason',
				fantasy.position,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.int - sr1.off_int * sr2.off_int) as real),
				0,
				0,
				cast(avg(fantasy.fumble - sr1.off_fumble * sr2.off_fumble) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.td) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack - sr1.off_sack * sr2.off_sack) as real),
				cast(avg(fantasy.pts_allowed - sr1.off_pts * sr2.off_pts) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.points) as real)
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
			WHERE fantasy.team_id = fantasy_row.team_id
				AND fantasy.position = 'DEF'
				AND g.season_year = fantasy_row.season_year - 1
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;

			INSERT INTO fantasy_prev_def
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
			SELECT fantasy_row.gsis_id,
				fantasy.team_id,
				'',
				'career',
				fantasy.position,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.int - sr1.off_int * sr2.off_int) as real),
				0,
				0,
				cast(avg(fantasy.fumble - sr1.off_fumble * sr2.off_fumble) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.td) as real),
				cast(avg(fantasy.block_kick) as real),
				cast(avg(fantasy.safety) as real),
				cast(avg(fantasy.sack - sr1.off_sack * sr2.off_sack) as real),
				cast(avg(fantasy.pts_allowed - sr1.off_pts * sr2.off_pts) as real),
				0,
				0,
				0,
				0,
				0,
				cast(avg(fantasy.points) as real)
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
			WHERE fantasy.team_id = fantasy_row.team_id
				AND fantasy.position = 'DEF'
				AND fantasy.gsis_id < fantasy_row.gsis_id
			GROUP BY fantasy.team_id, fantasy.player_id, fantasy.position;
		end;
	end loop;

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
	SELECT
		fantasy_prev_off.gsis_id,
		fantasy_prev_off.team_id,
		fantasy_prev_off.player_id,
		fantasy_prev_off.prev_amount,
		fantasy_prev_off.position,
		avg(fantasy_prev_off.pass_att),
		avg(fantasy_prev_off.pass_cmp),
		avg(fantasy_prev_off.pass_yds),
		avg(fantasy_prev_off.pass_tds),
		avg(fantasy_prev_off.int),
		avg(fantasy_prev_off.rush_att),
		avg(fantasy_prev_off.rush_yds),
		avg(fantasy_prev_off.fumble),
		avg(fantasy_prev_off.targets),
		avg(fantasy_prev_off.rec),
		avg(fantasy_prev_off.rec_yds),
		avg(fantasy_prev_off.yac),
		avg(fantasy_prev_off.ret_yds),
		avg(fantasy_prev_off.td),
		avg(fantasy_prev_off.block_kick),
		avg(fantasy_prev_off.safety),
		avg(fantasy_prev_off.sack),
		avg(fantasy_prev_off.pts_allowed),
		avg(fantasy_prev_off.fg_50),
		avg(fantasy_prev_off.fg_40),
		avg(fantasy_prev_off.fg_0),
		avg(fantasy_prev_off.pat),
		avg(fantasy_prev_off.fg_miss),
		avg(fantasy_prev_off.points)
	FROM fantasy_prev_off
	GROUP BY
		fantasy_prev_off.gsis_id,
		fantasy_prev_off.team_id,
		fantasy_prev_off.player_id,
		fantasy_prev_off.prev_amount,
		fantasy_prev_off.position;

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
	SELECT
		fantasy_prev_def.gsis_id,
		fantasy_prev_def.team_id,
		fantasy_prev_def.player_id,
		fantasy_prev_def.prev_amount,
		fantasy_prev_def.position,
		avg(fantasy_prev_def.pass_att),
		avg(fantasy_prev_def.pass_cmp),
		avg(fantasy_prev_def.pass_yds),
		avg(fantasy_prev_def.pass_tds),
		avg(fantasy_prev_def.int),
		avg(fantasy_prev_def.rush_att),
		avg(fantasy_prev_def.rush_yds),
		avg(fantasy_prev_def.fumble),
		avg(fantasy_prev_def.targets),
		avg(fantasy_prev_def.rec),
		avg(fantasy_prev_def.rec_yds),
		avg(fantasy_prev_def.yac),
		avg(fantasy_prev_def.ret_yds),
		avg(fantasy_prev_def.td),
		avg(fantasy_prev_def.block_kick),
		avg(fantasy_prev_def.safety),
		avg(fantasy_prev_def.sack),
		avg(fantasy_prev_def.pts_allowed),
		avg(fantasy_prev_def.fg_50),
		avg(fantasy_prev_def.fg_40),
		avg(fantasy_prev_def.fg_0),
		avg(fantasy_prev_def.pat),
		avg(fantasy_prev_def.fg_miss),
		avg(fantasy_prev_def.points)
	FROM fantasy_prev_def
	GROUP BY
		fantasy_prev_def.gsis_id,
		fantasy_prev_def.team_id,
		fantasy_prev_def.player_id,
		fantasy_prev_def.prev_amount,
		fantasy_prev_def.position;

	UPDATE public.fantasy_prev
	SET points = (
		t0.pass_yds / 25.0
		+ t0.pass_tds * 4.0
		- t0.int * 2.0
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.td * 6.0
	)
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'QB'
		and fantasy_prev.fantasy_id = t0.fantasy_id;

	UPDATE public.fantasy_prev
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'RB'
		and fantasy_prev.fantasy_id = t0.fantasy_id;


	UPDATE public.fantasy_prev
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'WR'
		and fantasy_prev.fantasy_id = t0.fantasy_id;

	UPDATE public.fantasy_prev
	SET points = (
		+ t0.rush_yds / 10.0
		- t0.fumble * 2.0
		+ t0.rec_yds / 10.0
		+ t0.ret_yds / 10.0
		+ t0.td * 6.0
	)
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'TE'
		and fantasy_prev.fantasy_id = t0.fantasy_id;

	UPDATE public.fantasy_prev
	SET points = (
		+ t0.fg_50 * 5.0
		+ t0.fg_40 * 4.0
		+ t0.fg_0 * 3.0
		+ t0.pat * 1.0
		- t0.fg_miss * 1.0
	)
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'K'
		and fantasy_prev.fantasy_id = t0.fantasy_id;

	UPDATE public.fantasy_prev
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
	FROM public.fantasy_prev as t0
	WHERE fantasy_prev.position = 'DEF'
		and fantasy_prev.fantasy_id = t0.fantasy_id;
end;
$$ LANGUAGE plpgsql;