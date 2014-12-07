$(function () {
    $("#qbTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#qbTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $("#rbTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#rbTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $("#wrTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#wrTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $("#teTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#teTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $("#kTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#kTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $("#defTable").tablesorter({
        widgets: ['uitheme', 'zebra']
    });

    $('#defTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $('#home_button').click(function(){
		window.location = 'index.php';
	});
});