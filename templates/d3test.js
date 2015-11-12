var dataset = [];
for (i = 0; i < 25; i++) {
    var newNumber = Math.random() * 30;
    dataset.push(newNumber);
}


d3.select("body").selectAll("p")
    .data(dataset)
    .enter()
    .append("div")
    .attr("class", "bar")
    .style("height", function(d) {
        var barheight = 5 * d;
        return barheight + "px";
    });

console.log("test")
