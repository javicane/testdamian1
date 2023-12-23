import {useState, useEffect, Component} from "react";
import axios from "axios";
import List_check_now from "./List_check_now"

function Note() {

    // con el useState genero variables globales, en este caso "notes" , el parametro (null) para useState solo es usado la primera vez que 
    // se usa el componente, se usa solo para ponerle un valor inicial   
    const [notes , func_for_state] = useState(null) // func_query_pnl_tracker es un nombre de fantasia, la variable "notes" tiene scope global, 
    // entonces la puedo usar en cualquier parte del Component , incluso en el render

    console.log(notes)
    useEffect(() => { // esto se ejecuta luego de cargar todo el component, sino lo pongo, no se ejecuta nunca la funcion getNotes
      getNotes()
        } ,[])

    function getNotes() {
      axios({ //axios return a promise
          method: "GET",
          url:"/check_now/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
        }).then((response)=>{
          const data = response.data
          func_for_state(data) // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
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

        { notes && notes.map(note => <List_check_now
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        nearest_pnl={note.nearest_pnl} 
        nearest_price_to_put_in_position={note.nearest_price_to_put_in_position} 
        size={note.size}
        resize={note.resize}
        get_new_data={getNotes}
        />
        )}
    </div>

  );
}

export default Note;