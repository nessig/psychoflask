var svg = d3.select("body").append("svg")
    .attr("width", 500)
    .attr("height", 500);

var group = svg.append("g")
    .attr("transform", "translate(100,100)");

var r = 100;
var p = Math.PI * 2;



var arc = d3.svg.arc()
    .innerRadius(r - 20)
    .outerRadius(r)
    .startAngle(0)
    .endAngle(p - 1);

group.append("path")
    .attr("d", arc)
