import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_cancel_order_bulk_by_price_range from './List_cancel_order_bulk_by_price_range';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({price_high: "", price_low: ""})
  const columns = React.useMemo(
    () => [
      {
        Header: "result",
        accessor: "result",
      },
      {
        Header: "price_high",
        accessor: "price_high",
      },
      {
        Header: "price_low",
        accessor: "price_low",
      },
    ],
    []
  );
  const getData = () => [ {result: "-", price_high: "-", price_low: "-"} ];

  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/cancel_order_bulk_by_price_range/",
      data:{
        price_high: formNote.price_high,
        price_low: formNote.price_low
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
      price_high: formNote.price_high,
      price_low: formNote.price_low
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
        <h1>cancel_order_bulk_by_price_range</h1>
        <List_cancel_order_bulk_by_price_range columns={columns} data={data} />
    
        <div>
        <form className="note">
          <table>
            <tr>
              <td>price_high</td>
              <td> 
                <input onChange={handleChange}  name="price_high" placeholder="price_high" value={formNote.price_high} />
              </td>
            </tr>
            <tr>
              <td>price_low</td>
              <td> 
                <input onChange={handleChange}  name="price_low" placeholder="price_low" value={formNote.price_low} />
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