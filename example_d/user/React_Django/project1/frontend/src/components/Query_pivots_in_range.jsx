import {useState, useEffect} from "react";
import axios from "axios";
import List_pivots_in_range from "./List_pivots_in_range";
          //url:"/post_query_pivots/",

function Note() {

    const [notes , setNewNotes] = useState(null) 
    const [formNote, setFormNote] = useState({price_begin: "", price_end: ""})

    //useEffect(() => { etNotes() } ,[])

    function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
        axios({
          method: "POST",
          url:"/post_query_pivots/",
          data:{
            price_begin: formNote.price_begin,
            price_end: formNote.price_end
           }
        })
        .then((response) => {
          const data = response.data
          show_something(data)
        })

        //setFormNote(({
        //  price_begin: "",
        //  price_end: ""}))
        setFormNote(({
          price_begin: formNote.price_begin,
          price_end: formNote.price_end}))

        event.preventDefault() //cuando se hace un form submit, por default hace refresh de la pagina, no es de react,
                               // es el comportamiento esperado default de submitir un form
    }

    function show_something(data){ 
      console.log("data raw: ",data);
      setNewNotes(data)
  
  }

    function handleChange(event) { 
        const {value, name} = event.target
        setFormNote(prevNote => ({ ...prevNote, [name]: value}))
    }


  return (

     <div className='note'>
        <h1>query pivots in range</h1>
        { notes && notes.map(note => <List_pivots_in_range
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        pivots_list={note.pivots_list}
        />
        )}
        <div>
        <form className="note">
          <input onChange={handleChange}  name="price_begin" placeholder="high price pivot" value={formNote.price_begin} />
          <input onChange={handleChange} name="price_end" placeholder="low price pivot" value={formNote.price_end} />
          <button onClick={createNote}>Create Post</button>
        </form>
        </div>


    </div>

  );
}

        //sum_rp={note.sum_rp}
export default Note;