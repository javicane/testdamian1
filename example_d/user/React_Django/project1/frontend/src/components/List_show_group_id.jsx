import React, { useState, useEffect } from 'react';
import { useTable } from "react-table";

function List_show_group_id({ columns, data }) {
  // Use the state and functions returned from useTable to build your UI
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({
      columns,
      data,
    });
  //var bgColor = "yellow";
  var bgColor = "";

//<div className="container" style={{ backgroundColor: bgColor }}></div>
  //console.log("colorcito:", colorcito)
  function damian_getRowStyle(row){
    bgColor = "#282c34";
    //console.log("soy damian_getRowStyle valor columna active: ", row.values.active_pivot);
    //console.log("bgColor incial:", bgColor)
    var value_of_column_active_pivot = row.values.active_pivot;
    //console.log("typeof value_of_column_active_pivot: ", typeof value_of_column_active_pivot);
    if ( value_of_column_active_pivot == 'active' ) {
      bgColor = "#336600"
    //console.log("bgColor nuevo:", bgColor)
    }; 
  } 
  // Render the UI for your table
      //<table className="app_not_center" {...getTableProps()} border="1"></table>
  return (
    <div>
      <table className="last20pnl" {...getTableProps()} border="1">
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, i) => {
            prepareRow(row);
            return (
//https://codesandbox.io/s/k3q43jpl47?file=/index.js:355-362
// https://stackoverflow.com/questions/62101561/how-can-i-automatically-style-in-each-cell-in-react-table-based-on-the-cell-valu
              <tr {...row.getRowProps()} {...damian_getRowStyle(row)} style={{ backgroundColor: bgColor }} >
                {row.cells.map((cell) => {
                  return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>  
  );
}
export default List_show_group_id;
