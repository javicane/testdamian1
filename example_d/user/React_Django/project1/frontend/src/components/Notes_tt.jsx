import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_tt from './List_tt';
//https://www.samuelliedtke.com/blog/react-table-tutorial-part-1/

function Note() {
//const Timer = () => {
  //const [notes , setNewNotes] = useState(null) 
  const [formNote, setFormNote] = useState({price_begin: "", price_end: ""})
  const columns = React.useMemo(
    () => [
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
        Cell: (props) => {
            console.log(props.test)
            return (
              <p>hola</p>
            );
        }
      },
      {
        Header: "repeat",
        accessor: "repeat",
      },
      {
        Header: "tpos",
        accessor: "tp",
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
        Header: "Enable",
        id: "enable",
        accessor: "enable",
        Cell: (props) => {
            return (
              <input onChange={handleChange}  name="price_begin" placeholder="naver" value="myvalue" />
            );
        }
      },
    ],
    []
  );
  const getData = () => [ { pivot: "-", size: "-", resize: "-", repeat: "-" } ];

  // ok const [data, ff] = useState(getData);
  const [data, setNewNotes] = useState(getData);

  //const data = React.useMemo(() => getData(), []);

  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/test/",
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
        <h1>TT</h1>
        <List_tt columns={columns} data={data} />
    
        <div>
        <form className="note">
          <input onChange={handleChange}  name="price_begin" placeholder="high price pivot" value={formNote.price_begin} />
          <input onChange={handleChange} name="price_end" placeholder="low price pivot" value={formNote.price_end} />
          <button onClick={createNote}>Create Post</button>
        </form>
        </div>
  </div>
  );
};

export default Note;