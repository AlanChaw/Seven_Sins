var locate_data = $.ajax({
    url: "http://115.146.92.183:5984/geo_origin/geo_melb",

    dataType: "json",
    success: console.log("County data successfully loaded."),
    error: function(xhr) {
        alert(xhr.statusText)
    }
})
//var string = JSON.stringify(locate_data)
//console.log(string["features"][0])
var json_data = (function() {
    var json = null;
    $.ajax({
        async: false,
        url: "http://115.146.92.183:5984/geo_origin/geo_melb",
        dataType: "json",
        success: function (data) {
            json = data;
        }
    });
    return json;
})();
var json_mel = (function() {
    var json = null;
    $.ajax({
        async: false,
        url: "http://115.146.92.183:5984/aurin/_design/myDesign/_view/agg_by_region?group=true",
        dataType: "json",
        success: function (data) {
            json = data;
        }
    });
    return json;
})();
var dict_total = {};
for (j = 0; j < json_mel["rows"].length; j++) {
  dict_total[json_mel["rows"][j]["key"]] = json_mel["rows"][j]["value"]
}
var name_value = {};
for (j = 0; j < json_data["features"].length; j++) {
  if(dict_total[json_data["features"][j]["properties"]["SA2_NAME16"]] == null){
  name_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = 0
}else{
  name_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = dict_total[json_data["features"][j]["properties"]["SA2_NAME16"]]
}}
console.log(name_value)
// control that shows state info on hover
// get color depending on population density value
var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}
$.when(locate_data,json_mel).done(function() {
    var map = L.map('map')
        .setView([-37.8142, 144.9632], 12);
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
          '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
          'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
      }).addTo(map);
        var info = L.control();

        info.onAdd = function (map) {
          this._div = L.DomUtil.create('div', 'info');
          this.update();
          return this._div;
        };

        info.update = function (properties) {
          this._div.innerHTML = '<h4>Melbourne district</h4>' +  (properties ?
            '<b>' + properties.SA2_NAME16 + '</b><br />' + "Total: " + name_value[properties.SA2_NAME16]
            : 'Hover over a distrcit')

        }

        info.addTo(map);
        map.createPane('labels');
        map.getPane('labels').style.zIndex = 650;
        map.getPane('labels').style.pointerEvents = 'none';
        function style(feature) {
          return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: getColor(name_value[feature.properties.SA2_NAME16])
          };
        }
        function getColor(d) {
          return d > 200 ? '#E31A1C' :
              d > 100  ? '#FC4E2A' :
              d > 50  ? '#FD8D3C' :
                    '#FEB24C';
        }
        function highlightFeature(e) {
          var layer = e.target;

          layer.setStyle({
            weight: 3,
            color: '#668',
            dashArray: '',
            fillOpacity: 0.7
          });
          if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
          }

          info.update(layer.feature.properties);
        }

        var melb_poly;
        function resetHighlight(e) {
          melb_poly.resetStyle(e.target);
          info.update();
        }
        var pop_infor = L.popup()

        function onEachFeature(feature, layer) {
          layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,

          });
        }
    // Add requested external GeoJSON to map
    melb_poly = L.geoJSON(locate_data.responseJSON, {
      style: style,
      onEachFeature: onEachFeature
    }).addTo(map);

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

      var div = L.DomUtil.create('div', 'info legend'),
        count = [0, 50, 100, 200],
        labels = [],
        from, to;

      for (var i = 0; i < count.length; i++) {
        from = count[i];
        to = count[i + 1];

        labels.push(
          '<i style="background:' + getColor(from + 1) + '"></i> ' +
          from + (to ? '&ndash;' + to : '+'));
      }

      div.innerHTML = labels.join('<br>');
      return div;
    };
    legend.addTo(map);

});
