
var selector = 'div#' + id;

d3.select('.right-window').append("p").text(data.right_text);

d3.select('.left-window').append("p").text(data.left_text);