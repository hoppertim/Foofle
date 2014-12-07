<?php
	$dbconnect = pg_connect("host=localhost port=5432 dbname=nfldb user=nfldb password=TDHaug92");
	$result = pg_query($dbconnect, "
			Select *
			from public.team
		");
	if(!$result){
		echo "An error occured.\n";
		exit;
	}
?>

<html>
<head>
	<title>TEST</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
	<script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
	<script src="./index.js"></script>
</head>
<body>
	This is a test page.
	<?php
		while($row = pg_fetch_row($result)){
			echo "<div>Team ID: $row[0], City: $row[1], Name: $row[2]</div>";
		}
	?>
</body>
</html>