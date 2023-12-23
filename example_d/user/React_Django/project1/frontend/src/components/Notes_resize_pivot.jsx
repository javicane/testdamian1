import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_resize_pivot from './List_resize_pivot';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({order_id: "1", resize: "1"})
  const columns = React.useMemo(
    () => [
      {
        Header: "result",
        accessor: "result",
      },
      {
        Header: "order_id",
        accessor: "order_id",
      },
      {
        Header: "resize",
        accessor: "resize",
      },
    ],
    []
  );
  const getData = () => [ {result: "-", order_id: "-", resize: "-"} ];

  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/resize_pivot/",
      data:{
        order_id: formNote.order_id,
        resize: formNote.resize
       }
    })
    .then((response) => {
      //console.log("in function createNote sell_order axios POST");
      const data = response.data
      console.log("data: " + data)
      //ff(data);
      show_something(data)
    })

    setFormNote(({
      order_id: formNote.order_id,
      resize: formNote.resize
    }))

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
        <h1>resize_pivot</h1>
        <List_resize_pivot columns={columns} data={data} />
    
        <div>
        <form className="note">
          <table>
            <tr>
              <td>order_id</td>
              <td> 
                <input onChange={handleChange}  name="order_id" placeholder="order_id" value={formNote.order_id} />
              </td>
            </tr>
            <tr>
              <td>resize</td> 
              <td>
                <input onChange={handleChange} name="resize" placeholder="resize" value={formNote.resize} />
              </td>
            </tr>
          </table>
          <button onClick={createNote}>Create Post</button>
        </form>
        </div>
  </div>
  );
};
//p_price, p_size, repeat, resize
export default Note;