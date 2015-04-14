(function(sight) {
    
    var drawAlbumsByYear = function(parentdiv) {
        
        var data = sight.data['playcountbyalbumyear'];
        
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = 980 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;
        
        var x = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.year; }))
            .range([0, width]);
        
        var y = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.playCount; }))
            .range([height, 0]);
        
        var r = d3.scale.pow()
            .domain(d3.extent(data, function(d) { return d.albums.length; }))
            .range([2.5, 20]);
        
        var xAxis = d3.svg.axis()
            .scale(x)
            .tickFormat(d3.format("^4f"))
            .orient("bottom");
    
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");
            
        var svg = d3.select(parentdiv).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Play Count");
            
        svg.selectAll(".yeardot")
            .data(data)
          .enter().append("circle")
            .attr("class", "yeardot")
            .attr("r", function(d) { return r(d.albums.length); })
            .attr("cx", function(d) { return x(d.year); })
            .attr("cy", function(d) { return y(d.playCount); })
            .on("mouseover", function(d) {
                $("#labelyear-"+d.year).show();
            })
            .on("mouseout", function(d) {
                $("#labelyear-"+d.year).hide();
            });
        
        
        var textNodes = svg.selectAll("foreignObject").data(data);
        var foreignObjects = textNodes.enter().append("foreignObject")
            .attr("x", function(d) { return x(d.year) - 100; })
            .attr("y", function(d) { return y(d.playCount) - 100; })
            .attr("width", 200)
            .attr("height", 300)
            .attr("id", function(d) { return "labelyear-" + d.year; })
            .style("display", "none")
            .style("pointer-events", "none");
            
        var htmlDOMs = foreignObjects.append("xhtml:body")
            .style("margin", 0)
            .style("padding", 0)
            .style("height", 300);
            
        var htmlLabels = htmlDOMs.append("div")
            .attr("class", "htmlLabel")
            .style("border", "1px solid #777");
            
        htmlLabels.append("p")
            .html(function(d) {
                return d.albums.reduce(function(prev, cur, i, arr) {
                    return (prev ? prev + "<br/>" : '') + cur['Album'] + ' - ' + cur['Artist'];
                }, "");
            })
            .style("margin", 0);
    };
    
    
    
    var drawPlayCountByAlbumYear = function(parentdiv) {
        var data = sight.data['playcountbyalbumyear'];
        
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = 980 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;
    
        var x = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.year; }))
            .range([0, width]);
        
        var y = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.playCount; }))
            .range([height, 0]);
        
        var xAxis = d3.svg.axis()
            .scale(x)
            .tickFormat(d3.format("^4f"))
            .orient("bottom");
        
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");
        
        var line = d3.svg.line()
            .x(function(d) { return x(d.year); })
            .y(function(d) { return y(d.playCount); });
        
        var svg = d3.select(parentdiv).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
        
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Play Count");
        
        svg.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("d", line);
    
    };
    
    sight.init = function() {
        drawAlbumsByYear('#chart_albumsbyyear');
//            drawPlayCountByAlbumYear('#chart_playcountbyalbumyear');

        $(".td-album").click(function(evt) {
            window.open("/persistentid/" +
                        $(this).parent().attr('id').replace('pid-', '') +
                        "/artwork");
        });
        
        $(".albumtile").hover(
            function() {
                $(this).find("img").fadeTo(100, 1);
                $(this).find(".albumtimeoverlay").fadeTo(100, 0);
            },
            function() {
                $(this).find("img").fadeTo(250, 0.5);
                $(this).find(".albumtimeoverlay").fadeTo(250, 1);
            }
        );
    };
    
})(window.sight = window.sight || {});

$(sight.init);
