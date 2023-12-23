import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_tracker_pnl_auto from './List_tracker_pnl_auto';

function Note() {
//const Timer = () => {
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [notes , func_for_state] = useState(null);

  function toggle() {
    setIsActive(!isActive);
  }

  function reset() {
    setSeconds(0);
    setIsActive(false);
  }

  function call_setSeconds() {
    setSeconds(seconds => seconds + 1); 
    const remainder = seconds % 5;
    //console.log(remainder);
    if (remainder == 0) {
      setSeconds(seconds => 1);
      getNotes();
    }
  }

  function getNotes() {
    axios({ //axios return a promise
        method: "GET",
        url:"/query_tracker_pnl/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
      }).then((response)=>{
        const data = response.data
        func_for_state(data); // When the GET request is made with axios, the data in the received response is assigned to the query_tracker_pnl function, 
        //console.log(notes);
        //console.log("estoy aca2");
        // When the GET request is made with axios, the data in the received response is assigned to the query_tracker_pnl function, 
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
      interval = setInterval(call_setSeconds, 1000);
    } else if (!isActive && seconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, seconds]);

  return (
  <div className="note">
        <h1>query_tracker_pnl</h1>
        { notes && notes.map(note => <List_tracker_pnl_auto
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        sum_rp={note.sum_rp} 
        rows={note.rows}
        balance={note.balance}
        sum_funding_fee={note.sum_funding_fee}
        rows_funding_fee={note.rows_funding_fee}
        entry_price={note.entry_price}
        sum_rp_last24hs={note.sum_rp_last24hs}
        count_rp_last24hs={note.count_rp_last24hs}
        sum_rp_last12hs={note.sum_rp_last12hs}
        count_rp_last12hs={note.count_rp_last12hs}
        sum_rp_last6hs={note.sum_rp_last6hs}
        count_rp_last6hs={note.count_rp_last6hs}
        sum_rp_last48hs={note.sum_rp_last48hs}
        count_rp_last48hs={note.count_rp_last48hs}
        sum_rp_last7days={note.sum_rp_last7days}
        count_rp_last7days={note.count_rp_last7days}
        />
        )} 
    <div className="app">
      <div className="time">
        {seconds}s
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

export default Note;