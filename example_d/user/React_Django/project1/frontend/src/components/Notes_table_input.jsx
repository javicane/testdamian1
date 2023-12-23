import React, { useState } from 'react';
import axios from "axios";
import List_table_input_all from './List_table_input_all';

function NotesTableInput() {
  const columns = React.useMemo(() => [ 
    { Header: "all",
      columns: [
        { Header: "pivot", 
          accessor: "pivot",
          // ... (Cell styling)
        }, 
        { Header: "count", accessor: "count", }, 
        { Header: "sum_total", accessor: "sum_total", },
        { Header: "weight%", accessor: "weight_percentage", }
      ]  
    }, 
  ], []);

  const getData = () => [{ pivot: "-", count: "-" }];

  const [data, setNewNotes] = useState(getData);

  async function apiCallWithAxios(event) {
    try {
      const response = await axios.post("/pivot_frequency_all/");
      const newData = response.data;
      setNewNotes(newData);
    } catch (error) {
      console.error("Error calling API:", error);
    }

    event.preventDefault();
  }
  
  return (
    <div className="note">
      <h1>pivot frequency</h1>
      <table>
        <tr>
          <td>
            <List_table_input_all columns={columns} data={data} />
          </td>
        </tr>
      </table>
    
      <div>
        <form className="note">
          <button onClick={apiCallWithAxios}>Create Post</button>
        </form>
      </div>
    </div>
  );
};

export default NotesTableInput;
