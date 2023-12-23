import React, { useState } from 'react';
import { useTable } from "react-table";
import axios from "axios";

function ListTableInputAll({ columns, data }) {
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({
      columns,
      data,
    });

  const [responses, setResponses] = useState({});

  async function callSecondAPI(row) {
    try {
      const response = await axios.post("/zaraza", {
        pivot: row.values.pivot,
        count: row.values.count,
        sum_total: row.values.sum_total,
        weight_percentage: row.values.weight_percentage,
        userInput: row.values.userInput,
      });
      setResponses((prevResponses) => ({
        ...prevResponses,
        [row.id]: response.data,
      }));
    } catch (error) {
      console.error("Error calling second API:", error);
    }
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
              <th>Input</th>
              <th>Action</th>
              <th>Response</th>
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <React.Fragment key={row.id}>
                <tr>
                  {row.cells.map((cell) => (
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                  ))}
                  <td>
                    <input
                      type="text"
                      value={row.values.userInput || ""}
                      onChange={(e) => {
                        row.values.userInput = e.target.value;
                        row.values.buttonClicked = false;
                      }}
                    />
                  </td>
                  <td>
                    <button
                      onClick={() => {
                        callSecondAPI(row);
                        row.values.buttonClicked = true;
                      }}
                      disabled={row.values.buttonClicked}
                    >
                      Call API
                    </button>
                  </td>
                  <td>{responses[row.id]}</td>
                </tr>
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default ListTableInputAll;
