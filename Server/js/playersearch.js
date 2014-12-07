$(function () {
    $("#myTable").tablesorter({
        widgets: ['uitheme', 'zebra'],
        headers: {
            0: {sortInitialOrder: 'asc'},
            1: {sortInitialOrder: 'desc'},
            2: {sortInitialOrder: 'desc'},
            3: {sortInitialOrder: 'desc'},
            4: {sortInitialOrder: 'desc'},
            5: {sortInitialOrder: 'desc'},
            6: {sortInitialOrder: 'desc'},
            7: {sortInitialOrder: 'desc'},
            8: {sortInitialOrder: 'desc'},
            9: {sortInitialOrder: 'desc'},
            10: {sortInitialOrder: 'desc'},
            11: {sortInitialOrder: 'desc'},
            12: {sortInitialOrder: 'desc'},
            13: {sortInitialOrder: 'desc'},
            14: {sortInitialOrder: 'desc'},
            15: {sortInitialOrder: 'desc'},
            16: {sortInitialOrder: 'desc'}
        },
        sortRestart: true
    });

    $('#myTable tbody tr').click(function () {
        $(this).siblings().removeClass('selected');
        $(this).toggleClass('selected');
    });

    $('#home_button').click(function(){
		window.location = 'index.php';
	});
});