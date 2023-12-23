import {useState, useEffect} from "react";
import axios from "axios";
import List from "./List"

function Note() {

    const [notes , setNewNotes] = useState(null) // setNewNotes es un nombre de fantasia
    const [formNote, setFormNote] = useState({   //setFormNote es un nombre de fantasia
      title: "",
      content: ""
    })

    useEffect(() => {
      getNotes()
        } ,[])

    function getNotes() {
      axios({ //axios return a promise
          method: "GET",
          url:"/notes/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
        }).then((response)=>{
          const data = response.data
          setNewNotes(data) // When the GET request is made with axios, the data in the received response is assigned to the setNewNotes function, 
          //and this updates the state variable notes with a new state.
          // Thus the value of the state variable changes from null to the data in the received response.
        }).catch((error) => {
          if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
            }
        })}

    function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
        axios({
          method: "POST",
          url:"/notes/",
          data:{
            title: formNote.title,
            content: formNote.content
           }
        })
        .then((response) => {
          getNotes()
        })

        setFormNote(({
          title: "",
          content: ""}))

        event.preventDefault() //cuando se hace un form submit, por default hace refresh de la pagina, no es de react,
                               // es el comportamiento esperado default de submitir un form
    }

    function DeleteNote(id) {
        axios({
          method: "DELETE",
          url:`/notes/${id}/`,
        })
        .then((response) => {
          getNotes()
        })
    }

    function handleChange(event) { 
        const {value, name} = event.target
        setFormNote(prevNote => ({
            ...prevNote, [name]: value})
        )}


  return (

     <div className=''>

        <form className="create-note">
          <input onChange={handleChange} text={formNote.title} name="title" placeholder="Title" value={formNote.title} />
          <textarea onChange={handleChange} name="content" placeholder="Take a note..." value={formNote.content} />
          <button onClick={createNote}>Create Post</button>
        </form>

        { notes && notes.map(note => <List
        key={note.id}
        id={note.id}
        title={note.title}
        content={note.content} 
        deletion ={DeleteNote}
        />
        )}

    </div>

  );
}

export default Note;