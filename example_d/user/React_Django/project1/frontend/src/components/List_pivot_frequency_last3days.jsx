import React, { useState, useEffect } from 'react';
import { useTable } from "react-table";


function List_pivot_frequency_last3days({ columns, data }) {
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({
      columns,
      data,
    });
  var bgColor = "";

  function damian_getRowStyle(row){
    bgColor = "#282c34";
    var value_of_column_active_pivot = row.values.active_pivot;
    if ( value_of_column_active_pivot == 'active' ) {
      bgColor = "#336600"
    }; 
  } 
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
export default List_pivot_frequency_last3days;