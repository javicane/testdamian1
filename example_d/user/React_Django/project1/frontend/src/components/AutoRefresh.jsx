import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_min_pivot_auto from './List_min_pivot_auto';

function AutoRefresh() {
//const Timer = () => {
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [notes , func_query_min_pivot] = useState(null)

  function toggle() {
    setIsActive(!isActive);
  }

  function reset() {
    setSeconds(0);
    setIsActive(false);
  }

  function call_setSeconds() {
    setSeconds(seconds => seconds + 3); 
    getNotes();
  }

  function getNotes() {
    axios({ //axios return a promise
        method: "GET",
        url:"/query_min_pivot/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
      }).then((response)=>{
        const data = response.data
        func_query_min_pivot(data); // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
        console.log(notes);
        console.log("estoy aca2");
        // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
        //and this updates the GLOBAL state variable "notes"  with a new state.
        // Thus the value of the state variable changes from null to the data in the received response.
      }).catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
          }
      })}

  useEffect(() => {
    let interval = null;
    if (isActive) {
      //interval = setInterval(() => {setSeconds(seconds => seconds + 1);}, 1000);
      interval = setInterval(call_setSeconds, 3000);
    } else if (!isActive && seconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, seconds]);

  return (
  <div className="note">
        <h1>min_pivot</h1>
        { notes && notes.map(note => <List_min_pivot_auto
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        min_pivot={note.min_pivot} 
        />
        )} 
    <div className="app">
      <div className="time">
        {seconds}s
      </div>
      <div className="row">
        <button className={`button button-primary button-primary-${isActive ? 'active' : 'inactive'}`} onClick={toggle}>
          {isActive ? 'Pause' : 'Start'}
        </button>
        <button className="button" onClick={reset}>
          Reset
        </button>
      </div>
    </div>
  </div>
  );
};

export default AutoRefresh;