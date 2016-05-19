var margin = {top: 20, right: 20, bottom: 100, left: 70},
    width = 800 - margin.left - margin.right,
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
    .ticks(10)
    .tickFormat(function(d) { return d + "%"; });

var svg = d3.select("#graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

d3.csv("data/sentiment_results.csv", function(error, data) {

    data.forEach(function(d) {
        d.label = d.candidate;
        d.tag = d.candidate.replace(/'/g,''); // tag is a label which omits O'Malley's apostrophe
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
        .attr("dx", "0em")
        .attr("dy", "0.7em")
        .attr("transform", "rotate(-30)");
    
    svg.append("g")
        .attr("class", "y axis")        
        .call(yAxis)
    .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 5 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", ".71em")
        .style("text-anchor", "middle")
        .text("Proportion of 'positive' sentences");

    // Create the bars
    svg.selectAll("bar")
        .data(data)
    .enter().append("rect")
        .style("fill", function(d) { return d.party == 'R' ? '#ff3333' : '#3399ff'; })
        .attr("x", function(d) { return x(d.label); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        // Darken the bar from 60% to 40% on mouseover
        .on("mouseover", function(d) {
            d3.select(this).style("fill", d.party == 'R' ? "#cc0000" : "#0073e6");
            d3.select(".barpic." + d.tag).attr("height", 100);
        })
        .on("mouseout", function(d) {
            d3.select(this).style("fill", d.party == 'R' ? '#ff3333' : '#3399ff');
            d3.select(".barpic." + d.tag).attr("height", 50);
        });


    // Data labels
    svg.selectAll(".bartext")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "bartext") 
        .attr("fill", "white")
        .attr("text-anchor", "middle")
        .text(function(d) {
            return d.value.toFixed(1) + '%';
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
        .attr("class", function(d) { return "barpic " + d.tag; })
        .attr("height", 50)
        .attr("width", x.rangeBand())
        .attr("y", 0)
        .attr("x", function(d, i) { return x(d.label); });

});
