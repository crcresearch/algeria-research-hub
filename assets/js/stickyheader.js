$(document).ready(function(){
    $(window).scroll(function(){
        var topnav = document.getElementById('topnav').getBoundingClientRect();
        var header = document.getElementById('titleheader').getBoundingClientRect();
        var distance = header.bottom - topnav.bottom;
        
        if(distance <= 0){
            // then our nav bar has hit the bottom of the header
            // so let's make it stay there by setting it to the header's bottom
            // value and subtracting the height of the nav
            $('#topnav').css('top', (header.bottom - 85) + 'px');
        }
        else{
            $('#topnav').css('top', '0px')
        }
    });
});