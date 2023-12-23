import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_create_sell_order from './List_create_sell_order';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({order_id: "", order_id_to_close: "", price_to_put_in_position: "99", price_close: "100", size: "1", repeat: "N", resize: "1", factor_gain: "1.0012"})
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
        Header: "order_id_to_close",
        accessor: "order_id_to_close",
      },
      {
        Header: "price_in_position",
        accessor: "price_to_put_in_position",
      },
      {
        Header: "price_close",
        accessor: "price_close",
      },
      {
        Header: "size",
        accessor: "size",
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
  const getData = () => [ {result: "-", order_id: "-", order_id_to_close: "-", price_to_put_in_position: "-", price_close: "-", size: "-", repeat: "-", resize: "-", factor_gain: "-"} ];

  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/create_sell_order/",
      data:{
        price_to_put_in_position: formNote.price_to_put_in_position,
        price_close: formNote.price_close,
        size: formNote.size,
        repeat: formNote.repeat,
        resize: formNote.resize,
        factor_gain: formNote.factor_gain
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
      price_to_put_in_position: formNote.price_to_put_in_position,
      price_close: formNote.price_close,
      size: formNote.size,
      repeat: formNote.repeat,
      resize: formNote.resize,
      factor_gain: formNote.factor_gain
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
        <h1>create_sell_order</h1>
        <List_create_sell_order columns={columns} data={data} />
    
        <div>
        <form className="note">
          <table>
            <tr>
              <td>price_to_put_in_position</td>
              <td> 
                <input onChange={handleChange}  name="price_to_put_in_position" placeholder="price_to_put_in_position" value={formNote.price_to_put_in_position} />
              </td>
            </tr>
            <tr>
              <td>price_close</td>
              <td> 
                <input onChange={handleChange}  name="price_close" placeholder="price_close" value={formNote.price_close} />
              </td>
            </tr>
            <tr>
              <td>size</td> 
              <td>
                <input onChange={handleChange} name="size" placeholder="size" value={formNote.size} />
              </td>
            </tr>
            <tr>
              <td>repeat</td> 
              <td>
                  <select id="repeat" onChange={handleChange}  name="repeat" placeholder="repeat" value={formNote.repeat} >
                    <option value="Y">Y</option>
                    <option value="N">N</option>
                  </select>
              </td>
            </tr>
            <tr>
              <td>resize</td> 
              <td>
                <input onChange={handleChange} name="resize" placeholder="resize" value={formNote.resize} />
              </td>
            </tr>
            <tr>
              <td>factor_gain</td> 
              <td>
                <input onChange={handleChange} name="factor_gain" placeholder="factor_gain" value={formNote.factor_gain} />
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