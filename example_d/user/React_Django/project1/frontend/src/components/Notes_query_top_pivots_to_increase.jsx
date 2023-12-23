import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_query_top_pivots_to_increase from './List_query_top_pivots_to_increase';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({b_tc: "", b_tp: ""})
  const columns = React.useMemo(
    () => [
      {
        Header: "order_id",
        accessor: "order_id",
      },
      {
        Header: "order_status",
        accessor: "order_status",
      },
      {
        Header: "order_id_to_close",
        accessor: "order_id_to_close",
      },
      {
        Header: "trigger_price_to_put_in_position",
        accessor: "trigger_price_to_put_in_position",
      },
      {
        Header: "trigger_price_to_close",
        accessor: "trigger_price_to_close",
      },
      {
        Header: "original_quamtity",
        accessor: "original_quantity",
      },
      {
        Header: "clientorderid",
        accessor: "clientorderid",
      },
      {
        Header: "repeat",
        accessor: "repeat",
      },
      {
        Header: "resize",
        accessor: "resize",
      },
      {
        Header: "factor_gain",
        accessor: "factor_gain",
      },
    ],
    []
  );

  const getData = () => [ {order_id: "-", order_status: "-", order_id_to_close: "-", trigger_price_to_put_in_position: "-", trigger_price_to_close: "-", original_quantity: "-", clientorderid: "-",
                           repeat: "-", resize: "-", factor_gain: "-"} ];
  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/query_top_pivots_to_increase/",
      data:{
        b_tc: formNote.b_tc,
        b_tp: formNote.b_tp
       }
    })
    .then((response) => {
      //console.log("in function createNote axios POST");
      const data = response.data
      //console.log("data: " + data)
      //ff(data);
      show_something(data)
    })

    setFormNote(({
      b_tc: formNote.b_tc,
      b_tp: formNote.b_tp}))

    event.preventDefault() //cuando se hace un form submit, por default hace refresh de la pagina, no es de react,
                               // es el comportamiento esperado default de submitir un form
  }
  
  function show_something(data){ 
      //console.log("in show_something data raw: ",data);
      setNewNotes(data)
  
  }
  function handleChange(event) { 
      const {value, name} = event.target
      setFormNote(prevNote => ({ ...prevNote, [name]: value}))
  }


  return (
  <div className="note">
        <h1>query_top_pivots_to_increase</h1>
        <List_query_top_pivots_to_increase columns={columns} data={data} />
    
        <div>
        <form className="note">
          <table>
            <tr>
              <td>baseline_pivot_t_close</td>
              <td>
                <input onChange={handleChange}  name="b_tc" placeholder="baseline_tc" value={formNote.b_tc} />
              </td>
            </tr>
            <tr>
              <td>baseline_pivot_t_put_in_position</td>
              <td>
                <input onChange={handleChange} name="b_tp" placeholder="baseline_tp" value={formNote.b_tp} />
              </td>
            </tr>
          </table>
          <button onClick={createNote}>Create Post</button>
        </form>
        </div>
  </div>
  );
};

export default Note;