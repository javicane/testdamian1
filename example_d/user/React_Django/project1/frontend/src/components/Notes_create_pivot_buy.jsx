import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_create_pivot_buy from './List_create_pivot_buy';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
  const [formNote, setFormNote] = useState({confirm_custom: "N", price_tclose: "9999", price_tpos: "9999", price: "1", up_down: "DOWN", order_id: "", order_id_to_close: "", price_to_put_in_position: "", price_close: "", size: "1", repeat: "Y", resize: "1", factor_gain: "1.0012"})
  const columns = React.useMemo(
    () => [
      {
        Header: "up_down",
        accessor: "up_down",
      },
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
  const getData = () => [ {up_down: "-", result: "-", order_id: "-", order_id_to_close: "-", price_to_put_in_position: "-", price_close: "-", size: "-", repeat: "-", resize: "-", factor_gain: "-"} ];

  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/create_pivot_buy/",
      data:{
        factor_gain: formNote.factor_gain,
        up_down: formNote.up_down,
        price: formNote.price,
        size: formNote.size,
        repeat: formNote.repeat,
        resize: formNote.resize,
        price_tpos: formNote.price_tpos,
        price_tclose: formNote.price_tclose,
        confirm_custom: formNote.confirm_custom
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
      factor_gain: formNote.factor_gain,
      up_down: formNote.up_down,
      price: formNote.price,
      size: formNote.size,
      repeat: formNote.repeat,
      resize: formNote.resize,
      price_tpos: formNote.price_tpos,
      price_tclose: formNote.price_tclose,
      confirm_custom: formNote.confirm_custom
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
        <h1>create_pivot_buy</h1>
        <List_create_pivot_buy columns={columns} data={data} />
    
        <div>
            <br />
           <form className="note">
             <table>
               <tr>
                 <td>factor_gain</td>
                 <td>
                   <select 
                     id="factor_gain" 
                     value={formNote.factor_gain}
                     onChange={handleChange}
                     name="factor_gain"
                   >
                     <option value="1.04">1.04</option>
                     <option value="1.03">1.03</option>
                     <option value="1.02">1.02</option>
                     <option value="1.01">1.01</option>
                     <option value="1.005">1.005</option>
                     <option value="1.0025">1.0025</option>
                     <option value="1.0012">1.0012</option>
                     <option value="1.0011">1.0011</option>
                     <option value="1.0010">1.0010</option>
                     <option value="1.0009">1.0009</option>
                     <option value="1.0008">1.0008</option>
                     <option value="1.0007">1.0007</option>
                     <option value="1.0006">1.0006</option>
                     <option value="1.0003">1.0003</option>
                   </select>
                 </td>
               </tr>
              <tr>
                <td>pivot_side</td>
                <td>
                  <select id="up_down" value={formNote.up_down} onChange={handleChange} name="up_down" >
                    <option value="UP">UP</option>
                    <option value="DOWN">DOWN</option>
                  </select>
                </td>
              </tr>
              <tr><td></td></tr>
              <tr>
                <td>if pivot_side=UP put TCLOSE of nearest Inferior pivot</td>
                <td>if pivot_side=DOWN put TPOS of nearest Superior pivot</td>
              </tr>
              <tr>
                <td>price</td>
                <td>
                  <input onChange={handleChange}  name="price" placeholder="price" value={formNote.price} />
                </td>
              </tr>
              <tr>
                <td>size</td>
                <td>
                  <input onChange={handleChange}  name="size" placeholder="size" value={formNote.size} />
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
                  <input onChange={handleChange}  name="resize" placeholder="resize" value={formNote.resize} />
                </td>
              </tr>
              <tr><td colSpan="2">---- custom tpos/tclose price ----</td></tr>
              <tr>
                <td>price_tpos</td>
                <td>
                  <input onChange={handleChange}  name="price_tpos" placeholder="price_tpos" value={formNote.price_tpos} />
                </td>
              </tr>
              <tr>
                <td>price_tclose</td>
                <td>
                  <input onChange={handleChange}  name="price_tclose" placeholder="price_tclose" value={formNote.price_tclose} />
                </td>
              </tr>
              <tr>
                <td>confirm custom</td>
                <td>
                  <select id="confirm_custom" onChange={handleChange}  name="confirm_custom" placeholder="confirm_custom" value={formNote.confirm_custom} >
                    <option value="Y">Y</option>
                    <option value="N">N</option>
                  </select>
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