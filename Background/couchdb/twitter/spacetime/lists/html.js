function (head, req) {
  provides("html", function () {
    send("<table border='2'>");
    var row;
    while (row = getRow()) {
      send("<tr><td>" + JSON.stringify(row.key) + "</td><td><td>" + JSON.stringify(row.value) + "</td></tr>");
    }
    send("</table>");
  });
}