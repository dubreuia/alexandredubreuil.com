// Trims white space for code elements
$('.prettyprint').each(function () {
    $(this).html($(this).html().trim());
});
$('.prettyprint .code').each(function () {
    $(this).html($(this).html().trim());
});

const setBodyClass = function () {
    $("body").removeClass();
    const className = ("slide-" + Reveal.getState()["indexh"]
        + "-" + Reveal.getState()["indexv"])
    $("body").addClass(className)
};

Reveal.addEventListener('ready', function (event) {
    setBodyClass();
});

Reveal.addEventListener('slidechanged', function (event) {
    setBodyClass();
});
