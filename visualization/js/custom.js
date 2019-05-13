(function ($) {

    "use strict";

        // PRE LOADER
        $(window).load(function(){
          $('.preloader').fadeOut(1000); // set duration in brackets
        });


        // navigation Section
        $('.navbar-collapse a').on('click',function(){
          $(".navbar-collapse").collapse('hide');
        });


        // smoothscroll js
        $(function() {
          $('#home a').bind('click', function(event) {
            var $anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 49
            }, 1000);
            event.preventDefault();
          });
        });


        // WOW Animation js
        new WOW({ mobile: false }).init();

})(jQuery);
