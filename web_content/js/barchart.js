var margin = {top: 20, right: 20, bottom: 100, left: 40},
    width = 700 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var headshots = {
    TRUMP: "img/trump_headshot.jpg",
    KASICH: "img/kasich_headshot.png",
    CRUZ: "img/cruz_headshot.png",
    CHRISTIE: "img/christie_headshot.png",
    CARSON: "img/carson_headshot.png",
    BUSH: "img/bush_headshot.png",
    "O'MALLEY": "img/omalley_headshot.png",
    CLINTON: "img/clinton_headshot.png",
    SANDERS: "img/sanders_headshot.png"
};
var yMin = 40,
    yMax = 70;

var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.05);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(d3.scale.linear()
        .domain([yMin, yMax])
        .range([height, 0]))
    .orient("left")
    .ticks(10);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

d3.csv("data/sentiment_results.csv", function(error, data) {

    data.forEach(function(d) {
        d.label = d.candidate;
        d.value = +d["positive %"];
    });

    x.domain(data.map(function(d) { return d.label; }));
    y.domain([yMin, yMax]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
    .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)");
    
    svg.append("g")
        .attr("class", "y axis")        
        .call(yAxis)
    .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", ".71em")
        .style("text-anchor", "middle")
        .text("Proportion of postive sentences");

    // Create the bars
    svg.selectAll("bar")
        .data(data)
    .enter().append("rect")
        .style("fill", function(d) { return d.party == 'R' ? '#ff3333' : '#3399ff'; })
        .attr("x", function(d) { return x(d.label); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); });

    // Data labels
    svg.selectAll(".bartext")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "bartext")
        .attr("fill", "white")
        .attr("text-anchor", "middle")
        .text(function(d) {
            return d.value + '%';
        })
        .attr("x", function(d, i) {
            return x(d.label) + 35;
        })
        .attr("y", function(d) {
            return y(d.value) + 15;
        });

    // hovering images
    svg.selectAll(".barpic")
        .data(data)
        .enter()
        .append("svg:image")
        .attr("xlink:href", function(d) {return headshots[d.label];})
        .attr("height", 60)
        .attr("width", x.rangeBand())
        .attr("y", 0)
        .attr("x", function(d, i) { return x(d.label); });

});
