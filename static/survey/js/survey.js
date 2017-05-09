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

$(function(){
  $('input[type="radio"]').click(function(){
    if ($(this).is(':checked'))
    {
      alert($(this).val());
    }
  });
});
//
