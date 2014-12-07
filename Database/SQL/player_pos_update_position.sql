/*
	Updates the positions of players that are 'UNK' and have stats similar to 
	that of an offensive position (QB, RB, WR, TE, K)
*/

create or replace function update_position()
returns void as $$
begin
	--Temp Table to hold the players with UnknownPositions
	Create Temp Table UnknownPosition
	(
		player_id varchar(10)
		, position player_pos
		, full_name varchar(100)
		, uniform_number usmallint
		, weight usmallint
		, play_count bigint
		, off_pct bigint
		, pass_pct bigint
		, rush_pct bigint
		, rec_pct bigint
		, kick_pct bigint
		, ret_pct bigint
	) on commit drop;

	insert into UnknownPosition
	(
		player_id
		, position
		, full_name
		, uniform_number
		, weight
		, play_count
		, off_pct
		, pass_pct
		, rush_pct
		, rec_pct
		, kick_pct
		, ret_pct
	)
	select *
	from
	(
		--Narrow down the players by selecting the players with more than 40 plays
		select t0.player_id
			, t0.position
			, t0.full_name
			, t0.uniform_number
			, t0.weight
			, t0.play_count
			, (t0.pass_atm + t0.rush_att + t0.targets + t0.kick + t0.ret) * 100 / t0.play_count as off_pct
			, t0.pass_atm * 100 / t0.play_count as pass_pct
			, t0.rush_att * 100 / t0.play_count as rush_pct
			, t0.targets * 100 / t0.play_count as rec_pct
			, t0.kick * 100 / t0.play_count as kick_pct
			, t0.ret * 100 / t0.play_count as ret_pct
		from
		(
			--Select all the players with a position of unknown and aggregate their offensive stats
			select p.player_id
				, p.position
				, p.full_name
				, p.uniform_number
				, p.weight
				, count(*) as play_count
				, sum(pp.passing_att) as pass_atm
				, sum(pp.rushing_att) as rush_att
				, sum(pp.receiving_tar) as  targets
				, sum(pp.kickret_ret + pp.kickret_fair + puntret_tot) as ret
				, sum(case when pp.kicking_fgm_yds > 0 then 1 else 0 end) + sum(pp.kicking_xpmade) + sum(pp.kicking_fgmissed + pp.kicking_xpmissed) as kick
			from public.player as p
				join public.play_player as pp
					on pp.player_id = p.player_id
			where p.position = 'UNK'
				and p.full_name != ''
			group by p.player_id
			order by p.full_name
		) as t0
		where play_count > 40
	)as t1
	--Removes defensive players with unknown positions and
	--players that have a high offensive percentage due to return plays
	where t1.off_pct > 20
		and t1.ret_pct * 100 / t1.off_pct < 60;

	--Updates the position of kickers
	update UnknownPosition
	set position = 'K'
	where position = 'UNK'
		and kick_pct * 100 / off_pct > 10;

	--Updates the position of quarterbacks
	update UnknownPosition
	set position = 'QB'
	where position = 'UNK'
		and pass_pct * 100 / off_pct > 50
	;

	--Updates the position of running backs
	update UnknownPosition
	set position = 'RB'
	where position = 'UNK'
		and
		(
			rush_pct * 100 / (rush_pct + rec_pct) > 10
			and full_name not in ('Josh Cribbs', 'Arrelious Benn', 'Chad Hall', 'Jacoby Ford')
			or full_name in ('Dorin Dickerson', 'Korey Hall')
		)
	;

	--Updates the position of tight ends if they are
	--above 240 lbs or their number is a tight end's number
	update UnknownPosition
	set position = 'TE'
	where position = 'UNK'
		and
		(
			weight >= 240
			or (uniform_number >= 20 and uniform_number < 50)
		)
	;

	--Assumes all remaining offensive players are wide receivers
	update UnknownPosition
	set position = 'WR'
	where position = 'UNK';



	--Commit the new player positions to the public.player table
	update public.player
	set position = up.position
	from UnknownPosition as up
	where player.position = 'UNK'
		and player.player_id = up.player_id;
end;
$$ language plpgsql