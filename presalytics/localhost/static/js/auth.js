$(document).ready(function () {
    function getUrlVars() {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return vars;
    }
    function shutdownServer() {
        $.ajax({
            url: "/shutdown",
            type: "POST",
        });
    };
    $('#closeButton').bind('click', function (e) {
        e.preventDefault();
        data = getUrlVars();
        $.ajax({
            url: "/auth/code",
            type: "POST",
            data: data,
            contentType: "application/json",
            dataType: "json",
            success: function() {
                shutdownServer();
                window.close();
            },
            error: function() {
                alert("An error occured.  Please restart script.")
            }
        })
    });
});