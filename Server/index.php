<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Foofle</title>
    <meta name="description" content="An interactive getting started guide for Brackets.">
    
    <link rel="stylesheet" href="css/bootstrap.min.css" media="screen">
    <link rel="stylesheet" href="css/jquery.autocomplete.css">
    <link rel="stylesheet" href="css/index.css">

    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/jquery.autocomplete.js"></script>
    <script src="js/index.js"></script>

    <script>
        $(document).ready(function(){
            <?php
                $dbconnect = pg_connect("host=localhost port=5432 dbname=nfldb user=nfldb password=TDHaug92");

                $result = pg_query($dbconnect, "
                        SELECT full_name || '-' || team
                        FROM
                            public.player
                        WHERE
                            team != 'UNK' and position in ('QB','RB','WR','TE','K')
                        ORDER BY
                            full_name asc
                    ");

                $row = pg_fetch_row($result);
                $player_list = "['$row[0]' ";

                while($row = pg_fetch_row($result)){
                    $name = str_replace("'", "\\'", $row[0]);
                    $player_list .= ",'$name' ";
                }

                $player_list .= "]";
            ?>
            var states = <?php echo $player_list; ?>

            $("#search-query").autocomplete({
                source: [states]
            });
        })
    </script>
</head>

<body>
    <div class="image">
        <center>
            <img src="img/Foofle.png" align="center" alt="Foofle">
        </center>
    </div>
    <div class="basic_search">
        <ul class="dropdown-menu position-button" role="menu" style="display:inline;">
            <li class="dropdown-submenu">
                <a>Position</a> 
                <ul class="dropdown-menu selections">
                    <li><a>QB</a>
                    </li>
                    <li><a>RB</a>
                    </li>
                    <li><a>WR</a>
                    </li>
                    <li><a>TE</a>
                    </li>
                    <li><a>K</a>
                    </li>
                    <li><a>DEF</a>
                    </li>
                </ul>
            </li>
        </ul>
        <form>
            <input id="search-query" type='text' class='input' placeholder='Enter Name of Player/Team' /> 
        </form>
        <ul class="dropdown-menu team-button" role="menu" style="display:inline;">
            <li class="dropdown-submenu">
                <a>Team</a>
                <ul class="dropdown-menu">
                    <li class="dropdown-submenu"><a>AFC</a>
                        <ul class="dropdown-menu">
                            <li class="dropdown-submenu"><a>East </a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="BUF">Bills</a></li>
                                    <li><a val="MIA">Dolphins</a></li>
                                    <li><a val="NYJ">Jets</a></li>
                                    <li><a val="NE">Patriots</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>North</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="CIN">Bengals</a></li>
                                    <li><a val="CLE">Browns</a></li>
                                    <li><a val="BAL">Ravens</a></li>
                                    <li><a val="PIT">Steelers</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>West</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="DEN">Broncos</a></li>
                                    <li><a val="SD">Chargers</a></li>
                                    <li><a val="KC">Chiefs</a></li>
                                    <li><a val="OAK">Raiders</a></li>

                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>South</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="IND">Colts</a></li>
                                    <li><a val="JAC">Jaguars</a></li>
                                    <li><a val="HOU">Texans</a></li>
                                    <li><a val="TEN">Titans</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown-submenu"><a>NFC</a>
                        <ul class="dropdown-menu">
                            <li class="dropdown-submenu"><a>East</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="DAL">Cowboys</a></li>
                                    <li><a val="PHI">Eagles</a></li>
                                    <li><a val="NYG">Giants</a></li>
                                    <li><a val="WAS">Redskins</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>North</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="CHI">Bears</a></li>
                                    <li><a val="DET">Lions</a></li>
                                    <li><a val="GB">Packers</a></li>
                                    <li><a val="MIN">Vikings</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>West</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="ARI">Cardinals</a></li>
                                    <li><a val="SEA">Seahawks</a></li>
                                    <li><a val="SF">49ers</a></li>
                                    <li><a val="STL">Rams</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu"><a>South</a>
                                <ul class="dropdown-menu teampage-links">
                                    <li><a val="TB">Buccaneers</a></li>
                                    <li><a val="ATL">Falcons</a></li>
                                    <li><a val="CAR">Panthers</a></li>
                                    <li><a val="NO">Saints</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
    <div style="width: 400px; margin:auto;">
    <div class="collapse-group advanced-div">
        <p><a id="advanced-icon" class="btn advanced-button" data-toggle="collapse" data-target="#demoout">Advanced Search <span>&#9759;</span></a>
        </p>
        <div class="collapse" id="demoout">
            <div class="btn-group advanced-position">
                <a class="btn dropdown-toggle position" data-toggle="dropdown" href="#"><div style="float:left;">Position</div><span class="caret" style="float:right;"></span></a>
                <ul id="player-position" class="dropdown-menu advanced-options">
                    <li><a href="#">Position</a>
                    </li>
                    <li><a href="#">QB</a>
                    </li>
                    <li><a href="#">RB</a>
                    </li>
                    <li><a href="#">WR</a>
                    </li>
                    <li><a href="#">TE</a>
                    </li>
                    <li><a href="#">K</a>
                    </li>
                    <li><a href="#">DEF</a>
                    </li>
                </ul>
            </div>
            <div class="btn-group">
                <a class="btn dropdown-toggle team" data-toggle="dropdown" href="#"><div style="float:left;">Team</div><span class="caret" style="float:right;"></span></a>
                <ul id="player-team" class="dropdown-menu scrollable-menu advanced-options">
                    <li><a href="#">Team</a>
                    </li>
                    <li><a href="#">ARI</a>
                    </li>
                    <li><a href="#">ATL</a>
                    </li>
                    <li><a href="#">BAL</a>
                    </li>
                    <li><a href="#">BUF</a>
                    </li>
                    <li><a href="#">CAR</a>
                    </li>
                    <li><a href="#">CHI</a>
                    </li>
                    <li><a href="#">CIN</a>
                    </li>
                    <li><a href="#">CLE</a>
                    </li>
                    <li><a href="#">DAL</a>
                    </li>
                    <li><a href="#">DEN</a>
                    </li>
                    <li><a href="#">DET</a>
                    </li>
                    <li><a href="#">GB</a>
                    </li>
                    <li><a href="#">HOU</a>
                    </li>
                    <li><a href="#">IND</a>
                    </li>
                    <li><a href="#">JAC</a>
                    </li>
                    <li><a href="#">KC</a>
                    </li>
                    <li><a href="#">MIA</a>
                    </li>
                    <li><a href="#">MIN</a>
                    </li>
                    <li><a href="#">NE</a>
                    </li>
                    <li><a href="#">NO</a>
                    </li>
                    <li><a href="#">NYG</a>
                    </li>
                    <li><a href="#">NYJ</a>
                    </li>
                    <li><a href="#">OAK</a>
                    </li>
                    <li><a href="#">PHI</a>
                    </li>
                    <li><a href="#">PIT</a>
                    </li>
                    <li><a href="#">SD</a>
                    </li>
                    <li><a href="#">SEA</a>
                    </li>
                    <li><a href="#">SF</a>
                    </li>
                    <li><a href="#">STL</a>
                    </li>
                    <li><a href="#">TB</a>
                    </li>
                    <li><a href="#">TEN</a>
                    </li>
                    <li><a href="#">WAS</a>
                    </li>
                </ul>
            </div>

            <div class="btn-group">
                <input id="advanced-submit" class="btn btn-default" type="submit" value="Submit">Submit</a> 
            </div>
        </div>
    </div>
    </div>
</body>
</html>
