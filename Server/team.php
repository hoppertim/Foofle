<!DOCTYPE html>
<?php
    $teamName = 'GB';
    if(isset($_GET['team'])){
        $teamName = strtoupper($_GET['team']);
    }

    $dbconnect = pg_connect("host=localhost port=5432 dbname=nfldb user=nfldb password=TDHaug92");

    $result = pg_query($dbconnect, "
            SELECT *
            FROM public.team
            WHERE team_id = '$teamName'
        ");
    $team = pg_fetch_row($result);

    $result = pg_query($dbconnect, "
            SELECT DISTINCT(season_year)
            FROM public.game
            ORDER BY season_year DESC
            LIMIT 1
        ");
    $season_year = pg_fetch_row($result)[0];

    $qb_result = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.last_name,
                    player.first_name,
                    player.team,
                    player.position,
                    sum(fantasy.pass_att),
                    sum(fantasy.pass_cmp),
                    sum(fantasy.pass_yds),
                    sum(fantasy.pass_tds),
                    sum(fantasy.int),
                    sum(fantasy.fumble),
                    sum(fantasy.rush_att),
                    sum(fantasy.rush_yds),
                    sum(fantasy.targets),
                    sum(fantasy.rec),
                    sum(fantasy.rec_yds),
                    sum(fantasy.yac),
                    sum(fantasy.td),
                    sum(fantasy.ret_yds),
                    max(COALESCE(player_projections.points, -100)) as points
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                    LEFT OUTER JOIN public.player_projections on player_projections.player_id = player.player_id
                WHERE player.position = 'QB'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.points desc
        ");
    if(!$qb_result){
        echo "an error occured";
        exit;
    }

    $rb_result = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.last_name,
                    player.first_name,
                    player.team,
                    player.position,
                    sum(fantasy.pass_att),
                    sum(fantasy.pass_cmp),
                    sum(fantasy.pass_yds),
                    sum(fantasy.pass_tds),
                    sum(fantasy.int),
                    sum(fantasy.fumble),
                    sum(fantasy.rush_att),
                    sum(fantasy.rush_yds),
                    sum(fantasy.targets),
                    sum(fantasy.rec),
                    sum(fantasy.rec_yds),
                    sum(fantasy.yac),
                    sum(fantasy.td),
                    sum(fantasy.ret_yds),
                    max(COALESCE(player_projections.points, -100)) as points
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                    LEFT OUTER JOIN public.player_projections on player_projections.player_id = player.player_id
                WHERE player.position = 'RB'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.points desc
        ");
    if(!$rb_result){
        echo "an error occured";
        exit;
    }

    $wr_result = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.last_name,
                    player.first_name,
                    player.team,
                    player.position,
                    sum(fantasy.pass_att),
                    sum(fantasy.pass_cmp),
                    sum(fantasy.pass_yds),
                    sum(fantasy.pass_tds),
                    sum(fantasy.int),
                    sum(fantasy.fumble),
                    sum(fantasy.rush_att),
                    sum(fantasy.rush_yds),
                    sum(fantasy.targets),
                    sum(fantasy.rec),
                    sum(fantasy.rec_yds),
                    sum(fantasy.yac),
                    sum(fantasy.td),
                    sum(fantasy.ret_yds),
                    max(COALESCE(player_projections.points, -100)) as points
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                    LEFT OUTER JOIN public.player_projections on player_projections.player_id = player.player_id
                WHERE player.position = 'WR'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.points desc
        ");
    if(!$wr_result){
        echo "an error occured";
        exit;
    }

    $te_result = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.last_name,
                    player.first_name,
                    player.team,
                    player.position,
                    sum(fantasy.pass_att),
                    sum(fantasy.pass_cmp),
                    sum(fantasy.pass_yds),
                    sum(fantasy.pass_tds),
                    sum(fantasy.int),
                    sum(fantasy.fumble),
                    sum(fantasy.rush_att),
                    sum(fantasy.rush_yds),
                    sum(fantasy.targets),
                    sum(fantasy.rec),
                    sum(fantasy.rec_yds),
                    sum(fantasy.yac),
                    sum(fantasy.td),
                    sum(fantasy.ret_yds),
                    max(COALESCE(player_projections.points, -100)) as points
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                    LEFT OUTER JOIN public.player_projections on player_projections.player_id = player.player_id
                WHERE player.position = 'TE'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.points desc
        ");
    if(!$te_result){
        echo "an error occured";
        exit;
    }

    $k_result = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.last_name,
                    player.first_name,
                    sum(fantasy.fg_50),
                    sum(fantasy.fg_40),
                    sum(fantasy.fg_0),
                    sum(fantasy.pat),
                    sum(fantasy.fg_miss),
                    max(COALESCE(player_projections.points, -100)) as points,
                    player.team
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                    LEFT OUTER JOIN public.player_projections on player_projections.player_id = player.player_id
                WHERE player.position = 'K'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.points desc
        ");
    if(!$k_result){
        echo "an error occured";
        exit;
    }

    $def_result = pg_query($dbconnect, "
            SELECT
                sum(fantasy.sack),
                sum(fantasy.int),
                sum(fantasy.fumble),
                sum(fantasy.td),
                sum(fantasy.block_kick),
                sum(fantasy.safety),
                round(cast(avg(fantasy.pts_allowed) as numeric), 1)
            FROM public.fantasy
                JOIN public.game on fantasy.gsis_id = game.gsis_id
            WHERE fantasy.position = 'DEF'
                AND team_id = '$teamName'
                AND game.season_year = $season_year
        ");
    if(!$def_result){
        echo "an error occured";
        exit;
    }
    $def_points = exec("E:/xampp/htdocs/Python/player_performance.py \"$teamName\"");

    $top_qb = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.full_name,
                    player.position,
                    sum(fantasy.pass_att),
                    sum(fantasy.pass_cmp),
                    sum(fantasy.pass_yds) as pass_yds,
                    sum(fantasy.pass_tds)
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                WHERE player.position = 'QB'
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.pass_yds desc
            LIMIT 1
        ");
    if(!$top_qb){
        echo "an error occured";
        exit;
    }
    $top_qb = pg_fetch_row($top_qb);

    $top_rb = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.full_name,
                    player.position,
                    sum(fantasy.rush_att),
                    sum(fantasy.rush_yds) as rush_yds,
                    sum(fantasy.td)
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                WHERE player.position in ('QB', 'RB', 'WR', 'TE')
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.rush_yds desc
            LIMIT 1
        ");
    if(!$top_rb){
        echo "an error occured";
        exit;
    }
    $top_rb = pg_fetch_row($top_rb);

    $top_wr = pg_query($dbconnect, "
            SELECT *
            FROM
            (
                SELECT
                    player.full_name,
                    player.position,
                    sum(fantasy.targets),
                    sum(fantasy.rec),
                    sum(fantasy.rec_yds) as rec_yds,
                    sum(fantasy.td)
                FROM public.player
                    LEFT OUTER JOIN public.fantasy ON player.player_id = fantasy.player_id
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                WHERE player.position in ('QB', 'RB', 'WR', 'TE')
                    AND team = '$teamName'
                    AND game.season_year = $season_year
                GROUP BY player.player_id
            ) as t0
            ORDER BY t0.rec_yds desc
            LIMIT 1
        ");
    if(!$top_wr){
        echo "an error occured";
        exit;
    }
    $top_wr = pg_fetch_row($top_wr);

    $record = pg_query($dbconnect, "
            SELECT
                sum(case when '$teamName' = away_team and away_score > home_score or '$teamName' = home_team and home_score > away_score then 1 else 0 end),
                sum(case when '$teamName' = away_team and away_score < home_score or '$teamName' = home_team and home_score < away_score then 1 else 0 end),
                sum(case when home_score = away_score then 1 else 0 end)
            FROM public.game
            WHERE '$teamName' in (game.away_team, game.home_team)
                and season_year = $season_year
                and finished = 't'
                and season_type in ('Regular', 'Postseason')
        ");
    if(!$record){
        echo "an error occured";
        exit;
    }
    $record = pg_fetch_row($record);
?>

<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="description" content="Team page that displays information about the page.">

    <title>Foofle</title>

    <script src="js/jquery-2.1.1.min.js"></script>
    <script src="js/jquery.tablesorter.min.js"></script>
    <script src="js/jquery.tablesorter.widgets.min.js"></script>
    <script src="js/team.js"></script>

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="css/jq.css">
    <link rel="stylesheet" href="css/theme.blue.css">
    <link rel="stylesheet" href="css/team.css">

</head>

<body>
    <div class="background"></div>
    <div>
        <button id="home_button">Home</button>
    </div>
    <div id="team-description">
        <div class="team_stats" style="padding:0px;">
            <center><img src="http://thescore-api-artifacts.s3.amazonaws.com/football/team/<?php echo $team[3];?>/small_logo.png" alt="" style="height:128px;"/></center>
            <center><b><?php echo "$team[1] $team[2]";?></b></center>
            <center><b><?php echo "$record[0] - $record[1] - $record[2]";?></b></center>
        </div>
        <div class="team_stats">
            <center style="border-bottom:solid black 1px;"><b>Passing Leader</b></center>
            <div style="width:36%;">
                <b>Name:</b><br>
                <b>Position:</b><br>
                <b>Pass Att:</b><br>
                <b>Pass Comp:</b><br>
                <b>Pass Yds:</b><br>
                <b>Pass Tds:</b><br>
            </div>
            <div style="width:60%;">
                    <?php echo $top_qb[0];?><br>
                    <?php echo $top_qb[1];?><br>
                    <?php echo $top_qb[2];?><br>
                    <?php echo $top_qb[3];?><br>
                    <?php echo $top_qb[4];?><br>
                    <?php echo $top_qb[5];?><br>
            </div>
        </div>
        <div class="team_stats">
            <center style="border-bottom:solid black 1px;"><b>Rushing Leader</b></center>
            <div style="width:36%;">
                <b>Name:</b><br>
                <b>Position:</b><br>
                <b>Rush Att:</b><br>
                <b>Rush Yds:</b><br>
                <b>Tds:</b><br>
            </div>
            <div style="width:60%;">
                    <?php echo $top_rb[0];?><br>
                    <?php echo $top_rb[1];?><br>
                    <?php echo $top_rb[2];?><br>
                    <?php echo $top_rb[3];?><br>
                    <?php echo $top_rb[4];?><br>
            </div>
        </div>
        <div class="team_stats">
            <center style="border-bottom:solid black 1px;"><b>Receiving Leader</b></center>
            <div style="width:36%;">
                <b>Name:</b><br>
                <b>Position:</b><br>
                <b>Targets:</b><br>
                <b>Receptions:</b><br>
                <b>Rec yds:</b><br>
                <b>Tds:</b><br>
            </div>
            <div style="width:60%;">
                    <?php echo $top_wr[0];?><br>
                    <?php echo $top_wr[1];?><br>
                    <?php echo $top_wr[2];?><br>
                    <?php echo $top_wr[3];?><br>
                    <?php echo $top_wr[4];?><br>
                    <?php echo $top_wr[5];?><br>
            </div>
        </div>
    </div>
    <hr>
    <h3><center>Quarterbacks</center></h3>
    <div class="table_div">
        <table id="qbTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>Pass Att.</th>
                    <th>Pass Comp.</th>
                    <th>Pass Yds</th>
                    <th>Pass Tds</th>
                    <th>Int.</th>
                    <th>Fumbles</th>
                    <th>Rush Att.</th>
                    <th>Rush Yds</th>
                    <th>Tds</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($qb_result)){
                        $points = $row[18];
                        if($points == -100){
                            $points = exec("E:/xampp/htdocs/Python/player_performance.py $row[18]");    
                        }
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=$row[1] $row[0]&team=$row[2]\">$row[0]</a></td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[4]</td>";
                        echo "<td>$row[5]</td>";
                        echo "<td>$row[6]</td>";
                        echo "<td>$row[7]</td>";
                        echo "<td>$row[8]</td>";
                        echo "<td>$row[9]</td>";
                        echo "<td>$row[10]</td>";
                        echo "<td>$row[11]</td>";
                        echo "<td>$row[16]</td>";
                        echo "<td>$points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <h3><center>Running Backs</center></h3>
    <div class="table_div">
        <table id="rbTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>Rush Att.</th>
                    <th>Rush Yds</th>
                    <th>Fumbles</th>
                    <th>Targets</th>
                    <th>Rec.</th>
                    <th>Rec. Yds</th>
                    <th>YAC</th>
                    <th>Tds</th>
                    <th>Return Yards</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($rb_result)){
                        $points = $row[18];
                        if($points == -100){
                            $points = exec("E:/xampp/htdocs/Python/player_performance.py $row[18]");    
                        }
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=$row[1] $row[0]&team=$row[2]\">$row[0]</a></td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[10]</td>";
                        echo "<td>$row[11]</td>";
                        echo "<td>$row[9]</td>";
                        echo "<td>$row[12]</td>";
                        echo "<td>$row[13]</td>";
                        echo "<td>$row[14]</td>";
                        echo "<td>$row[15]</td>";
                        echo "<td>$row[16]</td>";
                        echo "<td>$row[17]</td>";
                        echo "<td>$points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <h3><center>Wide Receivers</center></h3>
    <div class="table_div">
        <table id="wrTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>Rush Att.</th>
                    <th>Rush Yds</th>
                    <th>Fumbles</th>
                    <th>Targets</th>
                    <th>Rec.</th>
                    <th>Rec. Yds</th>
                    <th>YAC</th>
                    <th>Tds</th>
                    <th>Return Yards</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($wr_result)){
                        $points = $row[18];
                        if($points == -100){
                            $points = exec("E:/xampp/htdocs/Python/player_performance.py $row[18]");    
                        }
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=$row[1] $row[0]&team=$row[2]\">$row[0]</a></td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[10]</td>";
                        echo "<td>$row[11]</td>";
                        echo "<td>$row[9]</td>";
                        echo "<td>$row[12]</td>";
                        echo "<td>$row[13]</td>";
                        echo "<td>$row[14]</td>";
                        echo "<td>$row[15]</td>";
                        echo "<td>$row[16]</td>";
                        echo "<td>$row[17]</td>";
                        echo "<td>$points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <h3><center>Tight Ends</center></h3>
    <div class="table_div">
        <table id="teTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>Rush Att.</th>
                    <th>Rush Yds</th>
                    <th>Fumbles</th>
                    <th>Targets</th>
                    <th>Rec.</th>
                    <th>Rec. Yds</th>
                    <th>YAC</th>
                    <th>Tds</th>
                    <th>Return Yards</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($te_result)){
                        $points = $row[18];
                        if($points == -100){
                            $points = exec("E:/xampp/htdocs/Python/player_performance.py $row[18]");    
                        }
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=$row[1] $row[0]&team=$row[2]\">$row[0]</a></td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[10]</td>";
                        echo "<td>$row[11]</td>";
                        echo "<td>$row[9]</td>";
                        echo "<td>$row[12]</td>";
                        echo "<td>$row[13]</td>";
                        echo "<td>$row[14]</td>";
                        echo "<td>$row[15]</td>";
                        echo "<td>$row[16]</td>";
                        echo "<td>$row[17]</td>";
                        echo "<td>$points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <h3><center>Kickers</center></h3>
    <div class="table_div">
        <table id="kTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Last Name</th>
                    <th>First Name</th>
                    <th>FG, 50+ Yds</th>
                    <th>FG, 40-49 Yds</th>
                    <th>FG, 0-39 Yds</th>
                    <th>PAT</th>
                    <th>Missed FG</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($k_result)){
                        $points = $row[7];
                        if($points == -100){
                            $points = exec("E:/xampp/htdocs/Python/player_performance.py $row[18]");    
                        }
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=$row[1] $row[0]&team=$row[8]\">$row[0]</a></td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[2]</td>";
                        echo "<td>$row[3]</td>";
                        echo "<td>$row[4]</td>";
                        echo "<td>$row[5]</td>";
                        echo "<td>$row[6]</td>";
                        echo "<td>$points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <h3><center>Defense</center></h3>
    <div class="table_div">
        <table id="defTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Team</th>
                    <th>Sack</th>
                    <th>Interception</th>
                    <th>Fumble</th>
                    <th>Touchdown</th>
                    <th>Blocked Kick/Punt</th>
                    <th>Safety</th>
                    <th>Avg. Points Allowed</th>
                    <th>Proj. Points</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($def_result)){
                        echo '<tr>';
                        echo "<td class=\"last_name\"><a href=\"player.php?player=DEF&team=$teamName\">$teamName</a></td>";
                        echo "<td>$row[0]</td>";
                        echo "<td>$row[1]</td>";
                        echo "<td>$row[2]</td>";
                        echo "<td>$row[3]</td>";
                        echo "<td>$row[4]</td>";
                        echo "<td>$row[5]</td>";
                        echo "<td>$row[6]</td>";
                        echo "<td>$def_points</td>";
                        echo '</tr>';
                    }
                ?>
            </tbody>
        </table>
    </div>
    <div style="height:150px;"></div>
</body>
</html>