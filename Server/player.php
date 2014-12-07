<!DOCTYPE html>
<?php
	$player_id = '00-0023459';
	$playerName = 'Aaron Rodgers';
    if(isset($_GET['player'])){
        $playerName = str_replace("'", "''", strtoupper($_GET['player']));
    }
    $teamName = 'GB';
    if(isset($_GET['team'])){
        $teamName = strtoupper($_GET['team']);
    }
	$dbconnect = pg_connect("host=localhost port=5432 dbname=nfldb user=nfldb password=TDHaug92");
    if($playerName != 'DEF'){
		$result = pg_query($dbconnect, "
	            SELECT 
	            	player_id
	        	FROM
	        		public.player
				WHERE
					UPPER(full_name) = '$playerName'
						and team = '$teamName'
	        ");

		if($result and $row = pg_fetch_row($result)){
			$player_id = $row[0];
		}

	    $result = pg_query($dbconnect, "
	            SELECT 
	            	player.full_name,
	            	team.city || ' ' || team.name,
	            	player.position,
	            	player_projections.points
	        	FROM
	        		public.player
	        			join public.player_projections on player.player_id = player_projections.player_id
	        			join public.team on player.team = team.team_id
				WHERE
					player.player_id = '$player_id'
	        ");

	    $player = pg_fetch_row($result);
	    $position = $player[2];

	    $result = pg_query($dbconnect, "
	            SELECT DISTINCT(season_year)
	            FROM public.game
	            ORDER BY season_year DESC
	            LIMIT 1
	        ");

	    $season_year = pg_fetch_row($result)[0];

	    if ($position != 'K'){
		    $result = pg_query($dbconnect, "
		    		SELECT
		    			coalesce(sum(f.pass_att), 0),
		    			coalesce(sum(f.pass_cmp), 0),
		    			coalesce(sum(f.pass_yds), 0),
		    			coalesce(sum(f.pass_tds), 0),
		    			coalesce(sum(f.int), 0),
		    			coalesce(sum(f.rush_att), 0),
		    			coalesce(sum(f.rush_yds), 0),
		    			coalesce(sum(f.fumble), 0),
		    			coalesce(sum(f.rec), 0),
		    			coalesce(sum(f.rec_yds), 0),
		    			coalesce(sum(f.td), 0),
		    			coalesce(sum(ret_yds), 0)
					FROM
						public.fantasy as f
							join public.game on f.gsis_id = game.gsis_id
					WHERE
						game.season_year = $season_year
							AND f.player_id = '$player_id'
		        ");

		    $player_stats = pg_fetch_row($result);

		    $result = pg_query($dbconnect, "
		    		SELECT
		    			round(cast(avg(t0.pass_att) as numeric), 2),
		    			round(cast(avg(t0.pass_cmp) as numeric), 2),
		    			round(cast(avg(t0.pass_yds) as numeric), 2),
		    			round(cast(avg(t0.pass_tds) as numeric), 2),
		    			round(cast(avg(t0.int) as numeric), 2),
		    			round(cast(avg(t0.rush_att) as numeric), 2),
		    			round(cast(avg(t0.rush_yds) as numeric), 2),
		    			round(cast(avg(t0.fumble) as numeric), 2),
		    			round(cast(avg(t0.rec) as numeric), 2),
		    			round(cast(avg(t0.rec_yds) as numeric), 2),
		    			round(cast(avg(t0.td) as numeric), 2),
		    			round(cast(avg(t0.ret_yds) as numeric), 2)
		    		FROM
		    		(
		    			SELECT
			    			sum(f.pass_att) as pass_att,
			    			sum(f.pass_cmp) as pass_cmp,
			    			sum(f.pass_yds) as pass_yds,
			    			sum(f.pass_tds) as pass_tds,
			    			sum(f.int) as int,
			    			sum(f.rush_att) as rush_att,
			    			sum(f.rush_yds) as rush_yds,
			    			sum(f.fumble) as fumble,
			    			sum(f.rec) as rec,
			    			sum(f.rec_yds) as rec_yds,
			    			sum(f.td) as td,
			    			sum(f.ret_yds) as ret_yds
						FROM
							public.fantasy as f
								join public.game on f.gsis_id = game.gsis_id
						WHERE
							game.season_year = $season_year
								AND f.position = '$position'
						GROUP BY
							f.player_id
					) as t0
		        ");

		    $league_stats = pg_fetch_row($result);
		}
		else{
			$result = pg_query($dbconnect, "
		    		SELECT
	    				coalesce(sum(f.fg_50), 0),
	    				coalesce(sum(f.fg_40), 0),
	    				coalesce(sum(f.fg_0), 0),
	    				coalesce(sum(f.pat), 0),
	    				coalesce(sum(f.fg_miss), 0)
					FROM
						public.fantasy as f
							join public.game on f.gsis_id = game.gsis_id
					WHERE
						game.season_year = $season_year
							AND f.player_id = '$player_id'
		        ");

		    $player_stats = pg_fetch_row($result);

		    $result = pg_query($dbconnect, "
		    		SELECT
		    			round(cast(avg(t0.fg_50) as numeric), 2),
		    			round(cast(avg(t0.fg_40) as numeric), 2),
		    			round(cast(avg(t0.fg_0) as numeric), 2),
		    			round(cast(avg(t0.pat) as numeric), 2),
		    			round(cast(avg(t0.fg_miss) as numeric), 2)
		    		FROM
		    		(
		    			SELECT
			    			sum(f.fg_50) as fg_50,
			    			sum(f.fg_40) as fg_40,
			    			sum(f.fg_0) as fg_0,
			    			sum(f.pat) as pat,
			    			sum(f.fg_miss) as fg_miss
						FROM
							public.fantasy as f
								join public.game on f.gsis_id = game.gsis_id
						WHERE
							game.season_year = $season_year
								AND f.position = '$position'
						GROUP BY
							f.player_id
					) as t0
		        ");

		    $league_stats = pg_fetch_row($result);
		}

	    $result = pg_query($dbconnect, "
				(
				SELECT
					week,
					round(cast(coalesce(points, 0) as numeric), 2) as points
				FROM
					public.game
						left outer join public.fantasy
							on fantasy.gsis_id = game.gsis_id and fantasy.player_id = '$player_id'
				WHERE
					'$teamName' in (home_team, away_team)
						and season_year = $season_year
						and finished = 't'
						and season_type in ('Regular', 'Postseason')
				ORDER BY season_type, week
				)
				UNION
				(
					SELECT
						week,
						points
					FROM
						public.player_projections as pp
						join public.game on pp.gsis_id = game.gsis_id
					WHERE
						player_id = '$player_id'
					ORDER BY week desc
					LIMIT 1
				)
				ORDER BY week
	        ");

	    $points = "[";
	    $weeks = "[";

	    if($row = pg_fetch_row($result)){
	    	$weeks .= "$row[0]";
	    	$points .= "$row[1]";
	    }

	    while($row = pg_fetch_row($result)){
	    	$weeks .= ", $row[0]";
	    	$points .= ", $row[1]";
	    }

	    $points .= "]";
	    $weeks .= "]";
    }
    else {
    	$result = pg_query($dbconnect, "
	            SELECT DISTINCT(season_year)
	            FROM public.game
	            ORDER BY season_year DESC
	            LIMIT 1
	        ");

	    $season_year = pg_fetch_row($result)[0];
	    $position = "DEF";

	    $result = pg_query($dbconnect, "
	    		SELECT
	    			name,
	    			city,
	            	player_projections.points
				FROM
					public.team
					join public.player_projections on team.team_id = player_projections.player_id
				WHERE
					team.team_id = '$teamName'
	        ");

	    $team = pg_fetch_row($result);

	    $result = pg_query($dbconnect, "
	    		SELECT
	    			coalesce(sum(f.sack), 0),
	                coalesce(sum(f.int), 0),
	                coalesce(sum(f.fumble), 0),
	                coalesce(sum(f.td), 0),
	                coalesce(sum(f.block_kick), 0),
	                coalesce(sum(f.safety), 0),
	                round(cast(avg(f.pts_allowed) as numeric), 1)
				FROM
					public.fantasy as f
						join public.game on f.gsis_id = game.gsis_id
				WHERE
					game.season_year = $season_year
						AND f.team_id = '$teamName'
						AND f.position = 'DEF'
	        ");

	    $player_stats = pg_fetch_row($result);

	    $result = pg_query($dbconnect, "
	    		SELECT
	    			round(cast(avg(t0.sack) as numeric), 2),
	    			round(cast(avg(t0.int) as numeric), 2),
	    			round(cast(avg(t0.fumble) as numeric), 2),
	    			round(cast(avg(t0.td) as numeric), 2),
	    			round(cast(avg(t0.block_kick) as numeric), 2),
	    			round(cast(avg(t0.safety) as numeric), 2),
	    			round(cast(avg(t0.pts_allowed) as numeric), 2)
	    		FROM
	    		(
	    			SELECT
		    			sum(f.sack) as sack,
		    			sum(f.int) as int,
		    			sum(f.fumble) as fumble,
		    			sum(f.td) as td,
		    			sum(f.block_kick) as block_kick,
		    			sum(f.safety) as safety,
		    			avg(f.pts_allowed) as pts_allowed
					FROM
						public.fantasy as f
							join public.game on f.gsis_id = game.gsis_id
					WHERE
						game.season_year = $season_year
							AND f.position = '$position'
					GROUP BY
						f.team_id
				) as t0
	        ");

	    $league_stats = pg_fetch_row($result);

	    $result = pg_query($dbconnect, "
				(
				SELECT
					week,
					round(cast(coalesce(points, 0) as numeric), 2) as points
				FROM
					public.game
						left outer join public.fantasy
							on fantasy.gsis_id = game.gsis_id and fantasy.position = 'DEF' and fantasy.team_id = '$teamName'
				WHERE
					'$teamName' in (home_team, away_team)
						and season_year = $season_year
						and finished = 't'
						and season_type in ('Regular', 'Postseason')
				ORDER BY season_type, week
				)
				UNION
				(
					SELECT
						week,
						points
					FROM
						public.player_projections as pp
						join public.game on pp.gsis_id = game.gsis_id
					WHERE
						player_id = '$teamName'
					ORDER BY week desc
					LIMIT 1
				)
				ORDER BY week
	        ");

	    $points = "[";
	    $weeks = "[";

	    if($row = pg_fetch_row($result)){
	    	$weeks .= "$row[0]";
	    	$points .= "$row[1]";
	    }

	    while($row = pg_fetch_row($result)){
	    	$weeks .= ", $row[0]";
	    	$points .= ", $row[1]";
	    }

	    $points .= "]";
	    $weeks .= "]";
    }
	
?>

<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Foofle</title>
	
    <script src="js/jquery-2.1.1.min.js"></script>
    <script src="js/jquery.tablesorter.min.js"></script>
    <script src="js/jquery.tablesorter.widgets.min.js"></script>
    <script src="js/player.js"></script>
	<script src="Charts/Chart.js"></script>
	
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" href="tablesorter-master/docs/css/jq.css">
    <link rel="stylesheet" href="tablesorter-master/css/theme.blue.css">
    <link href="css/player.css" rel="stylesheet">
</head>

<body>
    <div class="background"></div>
	<div>
		<button id="home_button">Home</button>
	</div>
    <div id="player-description">
		<font size="8" face="impact">
			<?php 
				if($playerName != 'DEF'){
					echo $player[0];
				}
				else{
					echo "Defense";
				}
			?>
		</font>
		<font size="3" face="arial">
			<br>
				<?php
					if($playerName != 'DEF'){
						echo "<a href=\"team.php?team=$teamName\">$player[1]</a> - <a href=\"playersearch.php?position=$player[2]\">$player[2]</a> - Projection: $player[3]";
					}
					else{
						echo "<a href=\"team.php?team=$teamName\">$team[1] $team[0]</a> - <a href=\"playersearch.php?position=DEF\">DEF</a> - Projection: $team[2]";
					}
				?>
		</font>
    </div>
	<hr>
	<div style="height:350px; width:100%;">
		<div style="float:left; margin-left:20px; margin-right:20px; width:30%;">
			<font size="3" face="arial"><b>
				<div style="text-align:center;">Player Stats (G) vs. League Average (Y)</div>
			</b></font>
			<br>
			<canvas id="barChart" width="400" height="320"></canvas>
		</div>

		<div style="float:left; margin-left:20px; margin-right:20px; width:30%;">
			<font size="3" face="arial"><b>
				<div style="text-align:center;">Distribution of Fantasy Points</div>
			</b></font>
			<br>
			<canvas id="pieChart" width="375" height="300"></canvas>
		</div>

		<div style="float:left; margin-left:20px; margin-right:20px; width:30%;">
			<font size="3" face="arial"><b>
				<div style="text-align:center;">Fantasy Football Points Per Week</div>
			</b></font>
			<br>
			<canvas id="lineChart" width="400" height="300"></canvas>
		</div>
	</div>
	<hr>
	<?php
		if($playerName != 'DEF' and $position != 'K'){
			echo "
				<div class=\"stat_div\">
					<div id=\"stat-left\">
						<br><text class=\"stat\">Pass Attempts: </text><text class=\"info\">$player_stats[0]</text>
						<br><text class=\"stat\">Pass Completions: </text><text class=\"info\">$player_stats[1]</text>
						<br><text class=\"stat\">Pass Yards: </text><text class=\"info\">$player_stats[2]</text>
						<br><text class=\"stat\">Pass Touchdowns: </text><text class=\"info\">$player_stats[3]</text>
					</div>
					<div id=\"stat-middle\">
						<br><text class=\"stat\">Interceptions: </text><text class=\"info\">$player_stats[4]</text>
						<br><text class=\"stat\">Fumbles: </text><text class=\"info\">$player_stats[7]</text>
						<br><text class=\"stat\">Rush Attempts: </text><text class=\"info\">$player_stats[5]</text>
						<br><text class=\"stat\">Rush Yards: </text><text class=\"info\">$player_stats[6]</text>
					</div>
					<div id=\"stat-right\">
						<br><text class=\"stat\">Receptions: </text><text class=\"info\">$player_stats[8]</text>
						<br><text class=\"stat\">Reception Yards: </text><text class=\"info\">$player_stats[9]</text>
						<br><text class=\"stat\">Touchdowns: </text><text class=\"info\">$player_stats[10]</text>
						<br><text class=\"stat\">Return Yards: </text><text class=\"info\">$player_stats[11]</text>
					</div>
				</div>";
		}
		else if($playerName != 'DEF'){
			echo "
				<div class=\"stat_div\">
					<div id=\"stat-left\">
						<br><text class=\"stat\">FG Made 50+ Yds: </text><text class=\"info\">$player_stats[0]</text>
						<br><text class=\"stat\">FG Made 40-49 Yds: </text><text class=\"info\">$player_stats[1]</text>
					</div>
					<div id=\"stat-middle\">
						<br><text class=\"stat\">FG Made 0-39 Yds: </text><text class=\"info\">$player_stats[2]</text>
						<br><text class=\"stat\">PAT: </text><text class=\"info\">$player_stats[3]</text>
					</div>
					<div id=\"stat-right\">
						<br><text class=\"stat\">FG Miss: </text><text class=\"info\">$player_stats[4]</text>
					</div>
				</div>";
		}else{
			echo "
				<div class=\"stat_div\">
					<div id=\"stat-left\">
						<br><text class=\"stat\">Sacks: </text><text class=\"info\">$player_stats[0]</text>
						<br><text class=\"stat\">Interceptions: </text><text class=\"info\">$player_stats[1]</text>
						<br><text class=\"stat\">Fumbles: </text><text class=\"info\">$player_stats[2]</text>
					</div>
					<div id=\"stat-middle\">
						<br><text class=\"stat\">Touchdowns: </text><text class=\"info\">$player_stats[3]</text>
						<br><text class=\"stat\">Blocked Kicks: </text><text class=\"info\">$player_stats[4]</text>
					</div>
					<div id=\"stat-right\">
						<br><text class=\"stat\">Safeties: </text><text class=\"info\">$player_stats[5]</text>
						<br><text class=\"stat\">Avg. Points Allowed: </text><text class=\"info\">$player_stats[6]</text>
					</div>
				</div>";
		}
	?>
	<script>
		<!-- Bar Chart -->
		var barChartData = {
			labels : [
				<?php 
					if($position == 'QB'){
						echo '"PASS COMP","PASS ATT","YDS/10","PASS TD","RUSH ATT","RUSH YDS","TD","INT","FUMBLE"';
					}
					else if($position == 'RB' or $position == 'WR' or $position == 'TE'){
						echo '"RUSH ATT","RUSH YDS/10","REC","REC YDS/10","RETURN YDS/10","TD","FUMBLE"';
					}
					else if($position == 'K'){
						echo '"FG Made 50+","FG Made 40-49","FG Made 0-39","PAT","FG Miss"';
					}
					else{
						echo '"Sack","Int","Fumble","TD","Blocks","Safety","Pts Allowed"';
					}
				?>
				],
			datasets : [
				{
					fillColor : "rgba(32,71,49,0.8)",
					strokeColor : "rgba(220,220,220,0.8)",
					highlightFill: "rgba(220,220,220,0.75)",
					highlightStroke: "rgba(220,220,220,1)",
					data : [
						<?php
							if($position == 'QB'){
								echo "$player_stats[1],$player_stats[0],$player_stats[2]/10,$player_stats[3],$player_stats[5],$player_stats[6],$player_stats[10],$player_stats[4],$player_stats[7]";
							}
							else if($position == 'RB' or $position == 'WR' or $position == 'TE'){
								echo "$player_stats[5],$player_stats[6]/10,$player_stats[8],$player_stats[9]/10,$player_stats[11]/10,$player_stats[10],$player_stats[7]";
							}
							else if($position == 'K'){
								echo "$player_stats[0],$player_stats[1],$player_stats[2],$player_stats[3],$player_stats[4]";
							}
							else{
								echo "$player_stats[0],$player_stats[1],$player_stats[2],$player_stats[3],$player_stats[4],$player_stats[5],$player_stats[6]";
							}
						?>
						],
				},
				{
					fillColor : "rgba(255,182,18,0.8)",
					strokeColor : "rgba(151,187,205,0.8)",
					highlightFill : "rgba(151,187,205,0.75)",
					highlightStroke : "rgba(151,187,205,1)",
					data : [
						<?php
							if($position == 'QB'){
								echo "$league_stats[1],$league_stats[0],$league_stats[2]/10,$league_stats[3],$league_stats[5],$league_stats[6],$league_stats[10],$league_stats[4],$league_stats[7]";
							}
							else if($position == 'RB' or $position == 'WR' or $position == 'TE'){
								echo "$league_stats[5],$league_stats[6]/10,$league_stats[8],$league_stats[9]/10,$league_stats[11]/10,$league_stats[10],$league_stats[7]";
							}
							else if($position == 'K'){
								echo "$league_stats[0],$league_stats[1],$league_stats[2],$league_stats[3],$league_stats[4]";
							}
							else{
								echo "$league_stats[0],$league_stats[1],$league_stats[2],$league_stats[3],$league_stats[4],$league_stats[5],$league_stats[6]";
							}
						?>
						],
				}
			]
		}
		var barChart = document.getElementById("barChart").getContext("2d");
		new Chart(barChart).Bar(barChartData);
		
		<!-- Line Chart -->
		var lineChartData = {
			labels : <?php echo $weeks; ?>,
			datasets : [
				{
					label: "Fantasy Points",
					fillColor : "rgba(151,187,205,0.2)",
					strokeColor : "rgba(151,187,205,1)",
					pointColor : "rgba(151,187,205,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(151,187,205,1)",
					data : <?php echo $points; ?>
				}
			]
		}
		var lineChart = document.getElementById("lineChart").getContext("2d");
		new Chart(lineChart).Line(lineChartData);
		
		<!-- Pie Chart -->
		var pieChartData = [
			<?php
				if ($position == 'QB' or $position == 'RB' or $position == 'WR' or $position == 'TE'){
					echo "
							{
								value: $player_stats[2] / 25,
								color:'rgba(128,10,128,0.5)',
								highlight: '#FF5A5E',
								label: 'Passing Yards'
							},
							{
								value: $player_stats[3] * 4,
								color: 'rgba(0,10,255,0.5)',
								highlight: '#5AD3D1',
								label: 'Passing Tds'
							},
							{
								value: $player_stats[6] / 10,
								color: 'rgba(0,128,0,0.5)',
								highlight: '#FFC870',
								label: 'Rushing Yards'
							},
							{
								value: $player_stats[9] / 10,
								color: 'rgba(255,0,0,0.5)',
								highlight: '#A8B3C5',
								label: 'Receiving Yards'
							},
							{
								value: $player_stats[10] * 6,
								color: 'rgba(255,255,0,0.5)',
								highlight: '#616774',
								label: 'Touchdowns'
							},
							{
								value: $player_stats[11] / 10,
								color: 'rgba(250,128,20,0.5)',
								highlight: '#616774',
								label: 'Return Yards'
							}
						";
				}
				else if ($position == 'K'){
					echo "
							{
								value: $player_stats[0] * 5,
								color:'rgba(128,10,128,0.5)',
								highlight: '#FF5A5E',
								label: 'FG Made 50+ Yards'
							},
							{
								value: $player_stats[1] * 4,
								color: 'rgba(0,10,255,0.5)',
								highlight: '#5AD3D1',
								label: 'FG Made 40-49 Yards'
							},
							{
								value: $player_stats[2] * 3,
								color: 'rgba(0,128,0,0.5)',
								highlight: '#FFC870',
								label: 'FG Made 0-39 Yards'
							},
							{
								value: $player_stats[3],
								color: 'rgba(255,0,0,0.5)',
								highlight: '#A8B3C5',
								label: 'PAT'
							}
						";
				}
				else {
					echo "
							{
								value: $player_stats[0],
								color:'rgba(128,10,128,0.5)',
								highlight: '#FF5A5E',
								label: 'Sacks'
							},
							{
								value: $player_stats[1] * 2,
								color: 'rgba(0,10,255,0.5)',
								highlight: '#5AD3D1',
								label: 'Interceptions'
							},
							{
								value: $player_stats[2] * 2,
								color: 'rgba(0,128,0,0.5)',
								highlight: '#FFC870',
								label: 'Fumbles'
							},
							{
								value: $player_stats[3] * 6,
								color: 'rgba(255,0,0,0.5)',
								highlight: '#A8B3C5',
								label: 'Toudhdowns'
							},
							{
								value: $player_stats[4] * 2,
								color: 'rgba(255,255,0,0.5)',
								highlight: '#616774',
								label: 'Blocked Kicks'
							},
							{
								value: $player_stats[5] * 2,
								color: 'rgba(250,128,20,0.5)',
								highlight: '#34D08F',
								label: 'Safeties'
							}
						";
				}
			?>
		];
		var pieChart = document.getElementById("pieChart").getContext("2d");
		new Chart(pieChart).Pie(pieChartData);
	</script>
	
</body>
</html>