import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_pivot_frequency_all from './List_pivot_frequency_all';
import List_pivot_frequency_last7days from './List_pivot_frequency_last7days';
import List_pivot_frequency_last3days from './List_pivot_frequency_last3days';
import List_pivot_frequency_last24hs from './List_pivot_frequency_last24hs';

function Note() {
  const [formNote, setFormNote] = useState({desired_factor_gain: ""})

  const columns = React.useMemo( () => [ 
    { Header: "all",
    columns: [
      { Header: "pivot", 
        accessor: "pivot",
        Cell: (props) => {
          return (
            <p style=
              {
                { backgroundColor: 

                    props.value >= 0.53 && props.value < 0.54 ? "#990090" : 
                    ( props.value >= 0.52 && props.value < 0.53 ? "#882281" : 
                      ( props.value >= 0.51 && props.value < 0.52 ? "#774472" : 
                        ( props.value >= 0.50 && props.value < 0.51 ? "#666663" :
                          ( props.value >= 0.49 && props.value < 0.50 ? "#558854" :
                            ( props.value >= 0.48 && props.value < 0.49 ? "#440045" : "#332236")
                          )
                        )  
                      ) 
                    ) 

                }
              }>{props.value}</p>
          );
        }
    }, 
      { Header: "count", accessor: "count", }, 
      { Header: "sum_total", accessor: "sum_total", },
      { Header: "weight%", accessor: "weight_percentage", }
    ]  
    }, 
  ], []);
  
  const columns_last7days = React.useMemo( () => [ 
    { Header: "last 7 days",
    columns: [
      { Header: "pivot", accessor: "pivot", }, 
      { Header: "count", accessor: "count", } , 
      { Header: "sum_total", accessor: "sum_total", },
      { Header: "weight%", accessor: "weight_percentage", }
    ]  
    }, 
  ], []);

  const columns_last3days = React.useMemo( () => [ 
    { Header: "last 3 days",
    columns: [
      { Header: "pivot", accessor: "pivot", }, 
      { Header: "count", accessor: "count", },
      { Header: "sum_total", accessor: "sum_total", },
      { Header: "weight%", accessor: "weight_percentage", }
    ]  
    }, 
  ], []);

  const columns_last24hs = React.useMemo( () => [ 
    { Header: "last 24 hs",
    columns: [
      { Header: "pivot", accessor: "pivot", }, 
      { Header: "count", accessor: "count", },
      { Header: "sum_total", accessor: "sum_total", },
      { Header: "weight%", accessor: "weight_percentage", }
    ]  
    }, 
  ], []);

  const getData = () => [ {pivot: "-", count: "-" } ];

  const [data, setNewNotes] = useState(getData);
  const [data_last7days, setNewNotes_last7days] = useState(getData);
  const [data_last3days, setNewNotes_last3days] = useState(getData);
  const [data_last24hs, setNewNotes_last24hs] = useState(getData);


  function createNote(event) { //event es el evento producido aca <button onClick={createNote}>Create Post</button>
    axios({
      method: "POST",
      url:"/pivot_frequency_all/",
      data:{
        desired_factor_gain: formNote.desired_factor_gain
       }
    })
    .then((response) => {
      const data = response.data
      show_something(data)
    })

    axios({
      method: "POST",
      url:"/pivot_frequency_last7days/",
      data:{
        desired_factor_gain: formNote.desired_factor_gain
       }
    })
    .then((response) => {
      const data = response.data
      show_something_last7days(data)
    })

    axios({
      method: "POST",
      url:"/pivot_frequency_last3days/",
      data:{
        desired_factor_gain: formNote.desired_factor_gain
       }
    })
    .then((response) => {
      const data = response.data
      show_something_last3days(data)
    })

    axios({
      method: "POST",
      url:"/pivot_frequency_last24hs/",
      data:{
        desired_factor_gain: formNote.desired_factor_gain
       }
    })
    .then((response) => {
      const data = response.data
      show_something_last24hs(data)
    })

    setFormNote(({ desired_factor_gain: formNote.desired_factor_gain}))
    event.preventDefault() //cuando se hace un form submit, por default hace refresh de la pagina, no es de react,
                               // es el comportamiento esperado default de submitir un form
  }
  
  function show_something(data){ setNewNotes(data) }
  function show_something_last7days(data){ setNewNotes_last7days(data) }
  function show_something_last3days(data){ setNewNotes_last3days(data) }
  function show_something_last24hs(data){ setNewNotes_last24hs(data) }

  return (
  <div className="note">
        <h1>pivot frequency</h1>
        <table>
          <tr>
            <td>
              <List_pivot_frequency_all columns={columns} data={data} />
            </td>
            <td>
              <List_pivot_frequency_last7days columns={columns_last7days} data={data_last7days} />
            </td>
            <td>
              <List_pivot_frequency_last3days columns={columns_last3days} data={data_last3days} />
            </td>
            <td>
              <List_pivot_frequency_last24hs columns={columns_last24hs} data={data_last24hs} />
            </td>
          </tr>
        </table>
    
        <div>
        <form className="note">
          <button onClick={createNote}>Create Post</button>
        </form>
        </div>
  </div>
  );
};

export default Note;
//                { /* <input onChange={handleChange} name="desired_factor_gain" placeholder="desired_factor_gain" value={formNote.desired_factor_gain} /> */}