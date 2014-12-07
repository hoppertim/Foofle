<?php
    $position = '';
    if(isset($_GET['position'])){
        $position = strtoupper($_GET['position']);
    }
    $teamName = '';
    if(isset($_GET['team'])){
        $teamName = strtoupper($_GET['team']);
    }
    $dbconnect = pg_connect("host=localhost port=5432 dbname=nfldb user=nfldb password=TDHaug92");

    $query = "
            SELECT
                player.last_name,
                player.first_name,
                t0.*
            FROM
                (
                SELECT
                    fantasy.player_id,
                    fantasy.team_id,
                    fantasy.position,
                    sum(fantasy.pass_yds),
                    sum(fantasy.rush_yds),
                    sum(fantasy.rec_yds),
                    sum(fantasy.pass_tds),
                    sum(fantasy.td),
                    sum(fantasy.int),
                    sum(fantasy.fumble),
                    sum(fantasy.fg_50 + fantasy.fg_40 + fantasy.fg_0),
                    sum(fantasy.pat),
                    sum(fantasy.sack),
                    sum(fantasy.block_kick),
                    sum(fantasy.safety),
                    round(cast(avg(fantasy.pts_allowed) as numeric), 2),
                    sum(fantasy.points) as points
                FROM public.fantasy
                    JOIN public.game on fantasy.gsis_id = game.gsis_id
                WHERE season_year = 2014
                    and season_type = 'Regular'
        ";

    if($position != ''){
        $query .= " and fantasy.position = '$position'";
    }

    if($teamName != ''){
        $query .= " and fantasy.team_id = '$teamName'";
    }

    $query .= "
                GROUP BY fantasy.player_id, fantasy.team_id, fantasy.position
                ) as t0
                LEFT OUTER JOIN public.player on t0.player_id = player.player_id
            ORDER BY t0.points desc, player.last_name asc
        ";

    $players = pg_query($dbconnect, $query);
?>
<!DOCTYPE html>
<html>
<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

    <title>Foofle</title>

    <meta name="description" content="An interactive getting started guide for Brackets.">

    <script src="js/jquery-2.1.1.min.js"></script>
    <script src="js/jquery.tablesorter.min.js"></script>
    <script src="js/jquery.tablesorter.widgets.min.js"></script>
    <script src="js/playersearch.js"></script>

    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/jq.css">
    <link rel="stylesheet" href="css/theme.blue.css">
    <link href="css/playersearch.css" rel="stylesheet">

</head>

<body>
    <div class="background"></div>
    <div>
        <button id="home_button">Home</button>
    </div>
    <center><h3>Player Search</h3></center>
    <hr>
    <div class="table_div">
        <table id="myTable" class="tablesorter-blue center">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Team</th>
                    <th>Position</th>
                    <th>Pass Yds</th>
                    <th>Rush Yds</th>
                    <th>Rec Yds</th>
                    <th>Pass Td</th>
                    <th>Td</th>
                    <th>Int</th>
                    <th>Fumbles</th>
                    <th>FG Made</th>
                    <th>PAT</th>
                    <th>Sack</th>
                    <th>Block</th>
                    <th>Safety</th>
                    <th>Avg. Pts Allowed</th>
                    <th>Fantasy Pts</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    while($row = pg_fetch_row($players)){
                        echo "<tr>";
                        if($row[0] != ''){
                            echo "<td><a href=\"player.php?player=$row[1] $row[0]&team=$row[3]\">$row[0], $row[1]</a></td>";    
                        }
                        else {
                            echo "<td><a href=\"player.php?player=$row[4]&team=$row[3]\">DEF</a></td>";
                        }
                        echo "<td><a href=\"team.php?team=$row[3]\">$row[3]</a></td>";
                        echo "<td>$row[4]</td>";
                        echo "<td>$row[5]</td>";
                        echo "<td>$row[6]</td>";
                        echo "<td>$row[7]</td>";
                        echo "<td>$row[8]</td>";
                        echo "<td>$row[9]</td>";
                        echo "<td>$row[10]</td>";
                        echo "<td>$row[11]</td>";
                        echo "<td>$row[12]</td>";
                        echo "<td>$row[13]</td>";
                        echo "<td>$row[14]</td>";
                        echo "<td>$row[15]</td>";
                        echo "<td>$row[16]</td>";
                        echo "<td>$row[17]</td>";
                        echo "<td>$row[18]</td>";
                        echo "</tr>";
                    }
                ?>
            </tbody>
        </table>
    </div>

</body>

</html>