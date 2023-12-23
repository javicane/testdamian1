import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_query_pivots_by_price_range from './List_query_pivots_by_price_range';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({price_begin: "", price_end: ""})
  const columns = React.useMemo(
    () => [
    //        res_dict = [{'pivot':a[0], 'size':a[1],'resize':a[2],'repeat':a[3], 'tc':a[4], 
   //                  'f_gain':a[5], 'active_pivot':a[6], 'order_id':a[7], 'order_id_to_close':a[8],
    //                  'previous_pivot':a[9], 'previous_pivot_distance':a[10]} for a in res_sql] #convert list of tuples in list of dicts
      {
        Header: "pivot",
        accessor: "pivot",
      },
      {
        Header: "size",
        accessor: "size",
      },
      {
        Header: "resize",
        accessor: "resize",
      },
      {
        Header: "repeat",
        accessor: "repeat",
      },
      {
        Header: "tclose",
        accessor: "tc",
      },
      {
        Header: "f_gain%",
        accessor: "f_gain",
      },
      {
        Header: "active",
        accessor: "active_pivot",
      },
      {
        Header: "order_id",
        accessor: "order_id",
      },
      {
        Header: "order_id_to_close",
        accessor: "order_id_to_close",
      },
      {
        Header: "previous_pivot",
        accessor: "previous_pivot",
      },
      {
        Header: "previous_pivot_distance%",
        accessor: "previous_pivot_distance",
      },
    ],
    []
  );

  const getData = () => [ {pivot: "-", size: "-", resize: "-", repeat: "-", tc: "-", f_gain: "-", active_pivot: "-",
                           order_id: "-", order_id_to_close: "-", previous_pivot: "-", previous_pivot_distance: "-"} ];
  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/query_pivots_by_price_range/",
      data:{
        price_begin: formNote.price_begin,
        price_end: formNote.price_end
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
      price_begin: formNote.price_begin,
      price_end: formNote.price_end}))

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
        <h1>query pivots by price range</h1>
        <List_query_pivots_by_price_range columns={columns} data={data} />
    
        <div>
        <form className="note">
          <table>
            <tr>
              <td>high price pivot</td>
              <td>
                <input onChange={handleChange}  name="price_begin" placeholder="high price pivot" value={formNote.price_begin} />
              </td>
            </tr>
            <tr>
              <td>low price pivot</td>
              <td>
                <input onChange={handleChange} name="price_end" placeholder="low price pivot" value={formNote.price_end} />
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