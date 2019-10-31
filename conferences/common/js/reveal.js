// Trims white space for code elements
$('.prettyprint').each(function () {
    $(this).html($(this).html().trim());
});
$('.prettyprint .code').each(function () {
    $(this).html($(this).html().trim());
});