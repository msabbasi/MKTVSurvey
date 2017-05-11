function showSliderValue(newValue, id) {
    //console.log(5+6);
    //document.getElementById("slider-value-"+name).innerHTML=newValue;
    document.getElementById(id).innerHTML=newValue;
}

function toggle(id) {
    var element = document.getElementById(id);

    if (element) {
        var display = element.style.display;

        if (display == "none") {
            element.style.display = "block";
        } else {
            element.style.display = "none";
        }
    }
}

/*
$(document).ready(function () {
    console.log('hi');
    $('#survey-form *').filter('.wrap-survey-question').each(function () {
        console.log('hi');
        question = $(this)
        if (question.find('.question-required').length) {
            console.log('yo');
            var text = question.find(':input:first').attr('required', true);
            var text = question.find(':input:first').attr('autofocus', true);
            question.find('.reveal-if-active').attr('required', false);
            console.log(text);
        }
    });
});
*/

$(document).on("click", ".wrap-radio", function (event) {
    var option = $(this)
    if (option.hasClass('checked')) {
    } else {
        console.log('added');
        var grandparent = option.parent().parent();
        grandparent.find('.wrap-radio').removeClass('checked');
        grandparent.find('.reveal-if-active').hide();
        grandparent.find('.reveal-if-active').attr('required', false);
        option.addClass('checked');
        var parent = option.parent();
        parent.find('.reveal-if-active').show();
        parent.find('.reveal-if-active').attr('required', true);
        var text = option.find('input[type="radio"]').trigger("click");
        console.log(text);

    }
});

$(document).on("click", ".wrap-checkbox", function (event) {
    var option = $(this)
    //
    if (option.hasClass('checked')) {
        option.removeClass('checked');
        var text = option.find('input[type="checkbox"]').prop('checked', false);

    } else {
        option.addClass('checked');
        var text = option.find('input[type="checkbox"]').prop('checked', true);

    }
    console.log(text);
});

//$( "#survey-form" ).validate({
//  rules: {
//    fruit: {
//      required: true
//    }
//  }
//});

//$('.btn-survey-submit').onClick(function(e) {
//
//})

$(document).on("click", ".btn-survey-submit", function (evt) {
    console.log('heyyy');

    $('#survey-form *').filter('.wrap-survey-question').each(function () {
        console.log('hi');
        question = $(this)
        if (question.find('.question-required').length) {
            if (question.find('.wrap-multiple-options').length) {
                if (question.find('input:checked').length < 1) {
                    evt.preventDefault();
                    $('html, body').animate({ scrollTop: question.offset().top }, 'slow');
                    question.find('.question-required').delay(1000).hide(0).delay(500).show(0).delay(500).hide(0).delay(500).show(0);
                    //question.addClass('blink').delay(2000).removeClass('blink');
                    //question.effect("highlight", {}, 3000);
                    //var originalBg = $(this).css("backgroundColor");
                    //question.stop().css("background-color", "#FFFF9C").animate({ backgroundColor: originalBg}, 1500);
                    //question.css('outline', 'none !important').attr("tabindex",-1).focus();
                }
            }
        }
    });
});