import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './Appd3.css';

function Appd3() {
  const [data] = useState([(2,25), (1,50) ,(5,35), (6,15), (4,94), (3,10)]);
  //const [data] = useState([25, 50, 35, 15, 94, 10]);
  const svgRef = useRef();

  useEffect(() => {
    // setting up svg
    const w = 400;
    const h = 200;
    const svg = d3.select(svgRef.current) 
      .attr('width', w)
      .attr('height', h)
      .style('background', '#d3d3d3')
      .style('margin-top', '50')
      .style('overflow', 'visible');

    // setting the scaling
    const xScale = d3.scaleLinear()
        .domain([0, data.length -1])
        //.domain([0, 10])
        .range([0, w]);
    const yScale = d3.scaleLinear()
        .domain([0, h])
        .range([h, 0]);
    const generateScaledLine = d3.line()
        .x((d, i) => xScale(i))
        .y(yScale)
        .curve(d3.curveCardinal);

    // setting the axes
    const xAxis = d3.axisBottom(xScale)
      .ticks(data.length)
      //.tickFormat(i => i + 1);
    const yAxis = d3.axisLeft(yScale)
      .ticks(5);
    svg.append('g')
      .call(xAxis)
      .attr('transform', `translate(0, ${h})`);
    svg.append('g')
      .call(yAxis);
    


    // setting up the data for the svg
    svg.selectAll('.line')
      .data([data])
      .join('path')
        .attr('d', d => generateScaledLine(d))
        .attr('fill', 'none')
        .attr('stroke', 'black');
  }, [data]);

  

  return (
    <div className="Appd3">
      <svg ref={svgRef}></svg> 
    </div>
  );
}

export default Appd3;