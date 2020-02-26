// Trims white space for code elements
$('.prettyprint').each(function () {
    $(this).html($(this).html().trim());
});
$('.prettyprint .code').each(function () {
    $(this).html($(this).html().trim());
});

const setBodyClass = function () {
    let body = $("body");
    let indexh = Reveal.getState()["indexh"];
    let indexv = Reveal.getState()["indexv"];
    let firstSlide = Reveal.isFirstSlide();
    let lastSlide = Reveal.isLastSlide();
    body.removeClass();
    body.addClass(`slide-${indexh}-${indexv}`);
    if (firstSlide) {
        body.addClass(`slide-first`);
    }
    if (lastSlide) {
        body.addClass(`slide-last`);
    }
    if (indexv === 0) {
        body.addClass(`slide-first-vertical`);
    }
};

Reveal.addEventListener('ready', function (event) {
    setBodyClass();
});

Reveal.addEventListener('slidechanged', function (event) {
    setBodyClass();
});
