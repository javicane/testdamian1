import React, { useState, useRef } from "react";
import { useTable } from "react-table";

function List_tt({ columns, data }) {
  // Use the state and functions returned from useTable to build your UI
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({
      columns,
      data,
    });
  const inputEl = useRef("A");
  const [editable, setEditable] = useState(false);
  const [btnText, setBtnText] = useState("Edit");
  const [alpha, setAlpha] = useState("A");
  const onEdit = () => {
    const text = editable ? "Edit" : "Update";
    setBtnText(text);
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    if (editable) {
      setAlpha(e.target.alpha.value);
      inputEl.current = e.target.alpha.value;
    }
    onEdit();
    setEditable(!editable);
  };
  const handleCancel = () => {
    onEdit();
    setAlpha(inputEl.current);
    setEditable(false);
  };
  const handleChange = (e) => {
    setAlpha(e.target.value);
  };

  // Render the UI for your table
      //<table className="app_not_center" {...getTableProps()} border="1"></table>
  return (
    <div>
    <form onSubmit={handleSubmit}>
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
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => {
                  return <td {...cell.getCellProps()}>{cell.render("Cell", {test: 'this is a test }'})}</td>;
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </form>
    </div>  
  );
}
export default List_tt;
