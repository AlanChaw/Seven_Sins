//LOAD GEOJSON DATA AND DETAIL DATA
var locate_data = $.ajax({
    url: "http://115.146.92.183:5984/geo_origin/geo_melb",

    dataType: "json",
    success: console.log("County data successfully loaded."),
    error: function(xhr) {
        alert(xhr.statusText)
    }
})
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
        url: "http://115.146.92.183:5984/analysed_twitters/_design/designs/_view/agg_by_region?group=true",
        dataType: "json",
        success: function (data) {
            json = data;
        }
    });
    return json;
})();
//CREAT DICTIONARY TO STORE DISTRICT NAME AND VALUE
var dict_total = {};
for (j = 0; j < json_mel["rows"].length; j++) {
  dict_total[json_mel["rows"][j]["key"]["name"]] = json_mel["rows"][j]["value"]["total"]

}
var total_value = {};
for (j = 0; j < json_data["features"].length; j++) {
  if(dict_total[json_data["features"][j]["properties"]["SA2_NAME16"]] == null){
  total_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = 0
}else{
  total_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = dict_total[json_data["features"][j]["properties"]["SA2_NAME16"]]
}}
var dict_posi = {};
for (j = 0; j < json_mel["rows"].length; j++) {
  dict_posi[json_mel["rows"][j]["key"]["name"]] = json_mel["rows"][j]["value"]["positive"]
}
var positive_value = {};
for (j = 0; j < json_data["features"].length; j++) {
  if(dict_posi[json_data["features"][j]["properties"]["SA2_NAME16"]] == null){
  positive_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = 0
}else{
  positive_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = dict_posi[json_data["features"][j]["properties"]["SA2_NAME16"]]
}}
var dict_neg = {};
for (j = 0; j < json_mel["rows"].length; j++) {
  dict_neg[json_mel["rows"][j]["key"]["name"]] = json_mel["rows"][j]["value"]["negative"]
}
var negative_value = {};
for (j = 0; j < json_data["features"].length; j++) {
  if(dict_neg[json_data["features"][j]["properties"]["SA2_NAME16"]] == null){
  negative_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = 0
}else{
  negative_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = dict_neg[json_data["features"][j]["properties"]["SA2_NAME16"]]
}}
var dict_neu = {};
for (j = 0; j < json_mel["rows"].length; j++) {
  dict_neu[json_mel["rows"][j]["key"]["name"]] = json_mel["rows"][j]["value"]["neutral"]
}
var neutral_value = {};
for (j = 0; j < json_data["features"].length; j++) {
  if(dict_neu[json_data["features"][j]["properties"]["SA2_NAME16"]] == null){
  neutral_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = 0
}else{
  neutral_value[json_data["features"][j]["properties"]["SA2_NAME16"]] = dict_neu[json_data["features"][j]["properties"]["SA2_NAME16"]]
}}
//CREAT MPA DATA Visualization

$.when(locate_data,json_mel).done(function() {
    var map = L.map('map')
        .setView([-37.8142, 144.9632], 12);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          id: 'mapbox.streets',
          accessToken: 'your.mapbox.access.token',
        }).addTo(map);
        var info = L.control();
        info.onAdd = function (map) {
          this._div = L.DomUtil.create('div', 'info');
          this.update();
          return this._div;
        };

        info.update = function (properties) {
          this._div.innerHTML = '<h4>victoria state</h4>' +  (properties ?
            '<b>' + properties.SA2_NAME16 + '</b><br />' + "Total: " + total_value[properties.SA2_NAME16] + ' posts' +
            '</b><br />' + "Positive: " + positive_value[properties.SA2_NAME16] + ' posts' + '</b><br />' + "Neutral: " + neutral_value[properties.SA2_NAME16] + ' posts'
            + '</b><br />' + "Negative: " + negative_value[properties.SA2_NAME16] + ' posts'
            : 'Hover over a distrcit');

        };
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
            fillColor: getColor(total_value[feature.properties.SA2_NAME16])
          };
        }
        function getColor(d) {
          return d > 1000 ? '#800026' :
              d > 500  ? '#BD0026' :
              d > 200  ? '#E31A1C' :
              d > 100  ? '#FC4E2A' :
              d > 50   ? '#FD8D3C' :
              d > 20   ? '#FEB24C' :
              d > 10   ? '#FED976' :
                    '#FFEDA0';
        }
        function highlightFeature(e) {
          var layer = e.target;

          layer.setStyle({
            weight: 5,
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
    }).addTo(map).bindPopup(chart);
    //markers.addLayer(melb_poly);
    //map.addLayer(markers);
    //map.fitBounds(markers.getBounds());
    //melb_poly.eachLayer(function (layer) {
        //layer.bindPopup(pos_example[layer.feature.properties.SA2_NAME16]  + '</b><br />' +
        //neu_example[layer.feature.properties.SA2_NAME16] + '</b><br />'
         //+ neg_example[layer.feature.properties.SA2_NAME16]);
    //});
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

      var div = L.DomUtil.create('div', 'info legend'),
        count = [0, 10, 20, 50, 100, 200, 500, 1000],
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
    function chart(d) {
      var feature = d.feature;
      var array1 = new Array(positive_value[feature.properties.SA2_NAME16], neutral_value[feature.properties.SA2_NAME16], negative_value[feature.properties.SA2_NAME16]);
      var data = array1;

      var width = 150;
      var height = 80;
      var margin = {left:20,right:15,top:40,bottom:40};

      var div = d3.create("div")
      var svg = div.append("svg")
        .attr("width", width+margin.left+margin.right)
        .attr("height", height+margin.top+margin.bottom);
      var g = svg.append("g")
        .attr("transform","translate("+[margin.left,margin.top]+")");

      var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d; }) ])
        .range([height,0]);

      var yAxis = d3.axisLeft()
        .ticks(0)
        .scale(y);
      g.append("g").call(yAxis);

      var x = d3.scaleBand()
        .domain(d3.range(3))
        .range([0,width]);
    var label_x = ["pos","neu","neg"]
      var xAxis = d3.axisBottom()
        .scale(x)
        .tickFormat(function(d) { return label_x[d]; });

      g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
          .selectAll("text")
          .attr("text-anchor","end")
          .attr("transform","rotate(-90)translate(-12,-15)")

      var rects = g.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("y",height)
        .attr("height",0)
        .attr("width", x.bandwidth()-2 )
        .attr("x", function(d,i) { return x(i); })
        .attr("fill","steelblue","negative")
        .transition()
        .attr("height", function(d) { return height-y(d); })
        .attr("y", function(d) { return y(d); })
        .duration(1000);

      var title = svg.append("text")
        .style("font-size", "15px")
        .text(feature.properties.SA2_NAME16)
        .attr("x", width/2 + margin.left)
        .attr("y", 30)
        .attr("text-anchor","middle");

      return div.node();

    }

});
