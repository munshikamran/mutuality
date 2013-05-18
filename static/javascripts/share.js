
(function($) {

    function addMatchNumber() {
        var firstNumber = parseInt($('#share-friend-number-one').html());
        var secondNumber = parseInt($('#share-friend-number-two').html());
        var thirdNumber = parseInt($('#share-friend-number-three').html());
        var fourthNumber = parseInt($('#share-friend-number-four').html());

        var total = firstNumber + secondNumber + thirdNumber + fourthNumber;

        var totalConnectionsPossible = 10000;
        var baseNumberOfConnections = 4000;
        var totalNumberOfConnections = baseNumberOfConnections + total;
        var networkPercentage = Math.round((totalNumberOfConnections/totalConnectionsPossible)*100);

        //console.log(total);

        $('#share-friend-total').html(total);
        $('#network-percentage').html(networkPercentage);
    }

        /* End Helper functions */
    $(document).ready(function() {
         addMatchNumber();
    });
    /* Begin Account Main Code */

    $('.onoffswitch-checkbox').on('click', function(){
        var checkboxBoolean = $(this).is(':checked');
        if (checkboxBoolean === false) {
            $(this).closest('.row').find('.share-number').html("0");
        } else {
            $(this).closest('.row').find('.share-number').html("30");
        }
        addMatchNumber();
    });

    /* End Main Code */

})(jQuery);