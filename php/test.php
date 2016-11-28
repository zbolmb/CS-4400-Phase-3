<?php
$link = mysql_connect('academic-mysql.cc.gatech.edu', 'cs4400_Team_38', 'PTtMisGK');
if (!$link) {
	die('Could not connect: ' . mysql_error());
}
mysql_select_db('cs4400_Team_38');
echo 'Connected successfully';
mysql_close($link);
?>