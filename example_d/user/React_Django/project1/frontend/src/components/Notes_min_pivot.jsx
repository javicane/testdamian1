import {useState, useEffect, Component} from "react";
import axios from "axios";
//import List from "./List"
import List_min_pivot from "./List_min_pivot"

function Note() {

    // con el useState genero variables globales, en este caso "notes" , el parametro (null) para useState solo es usado la primera vez que 
    // se usa el componente, se usa solo para ponerle un valor inicial   
    const [notes , func_query_min_pivot] = useState(null) // func_query_pnl_tracker es un nombre de fantasia, la variable "notes" tiene scope global, 
    // entonces la puedo usar en cualquier parte del Component , incluso en el render

    console.log(notes)
    useEffect(() => { // esto se ejecuta luego de cargar todo el component, sino lo pongo, no se ejecuta nunca la funcion getNotes
      getNotes()
        } ,[])

    function getNotes() {
      axios({ //axios return a promise
          method: "GET",
          url:"/query_min_pivot/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
        }).then((response)=>{
          const data = response.data
          func_query_min_pivot(data) // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
          //and this updates the GLOBAL state variable "notes"  with a new state.
          // Thus the value of the state variable changes from null to the data in the received response.
        }).catch((error) => {
          if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
            }
        })}



  return (

     <div className=''>

        { notes && notes.map(note => <List_min_pivot
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        min_pivot={note.min_pivot} 
        get_new_data={getNotes} // get_new_data contiene el nombre de una funcion (getNotes) que quiero pasar como parametro a List_min_pivot
        />
        )}
    </div>

  );
}

export default Note;