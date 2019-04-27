function (head, req) {

  provides("json", function() {

    send('{"type" : "FeatureCollection", "features" : [');
    var sep="";
    
    while (row = getRow()) {
      if (row.doc.coordinates) {
        var feat = {
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: row.doc.coordinates.coordinates
          },
          properties: {
            text: row.doc.text,
            user: row.doc.user.screen_name
          }
        };
        send(sep + JSON.stringify(feat));
        sep = ",";
      }
    }

    send("]}");
  });
}
