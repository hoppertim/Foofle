$(document).ready(function () {
    /* Team and Position Button Clicks */
    $(".teampage-links li a").each(function(){
      $this = $(this);
      path = '/team.php?team=' + $this.attr('val')
      $this.attr('href', path);
    })

    $(".position-button ul.selections a").each(function(){
        $this = $(this)
        $this.attr('href', 'playersearch.php?position=' + $this.text());
    })

    /* Player Search Form */
    $("#search-query").keydown(function (event) {
        if (event.keyCode == 13) {
            $this = $(this);
            $val = $this.val().replace(' ', '%20')
            $found = $('.xdsoft_autocomplete_dropdown').find('div[data-value="' + $val + '"]')
            if($found.size() > 0){
                input = $this.val().split('-');
                window.location = 'player.php?player=' + input[0] + '&team=' + input[1];
            }
        }
    });

    /* Advanced Position and Team Dropdowns */
    $selectPosition = 'Position'
    $selectTeam = 'Team'

    function chooseOption() {
        var selText = $(this).text();
        if ($(this).parents('.btn-group').find('.dropdown-toggle').hasClass("position")) {
            $selectPosition = selText;
        } else {
            $selectTeam = selText;
        }

        $(this).parents('.btn-group').find('.dropdown-toggle').html('<div style="float:left;">' + selText + '</div><span class="caret" style="float:right;"></span>');
    };

    $(".advanced-options li a").click(chooseOption);

    $("#advanced-submit").click(function () {
        $location = 'playersearch.php?'
        if($selectPosition != 'Position'){
            $location += 'position=' + $selectPosition + '&';
        }
        if($selectTeam != 'Team'){
            $location += 'team=' + $selectTeam
        }
        window.location = $location

    });
});