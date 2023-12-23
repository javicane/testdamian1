import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_check_now_auto from './List_check_now_auto';

function Note() {
//const Timer = () => {
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [notes , setNotes] = useState(null);
  const [prevLastLineWebsocket, setPrevLastLineWebsocket] = useState(null);
  const [sameLastLineWebsocketCounter, setSameLastLineWebsocketCounter] = useState(0);
  const [prevActivePivot, setPrevActivePivot] = useState(null);
  const [sameActivePivotCounter, setSameActivePivotCounter] = useState(0);
  const [isRendered, setIsRendered] = useState(false);

  useEffect(() => {
  //console.log('rendering, Iam useEffect, prevActivePivot :', prevActivePivot);
  console.log('rendering, Iam useEffect, prevLastLineWebsocket :', prevLastLineWebsocket);
  setIsRendered(true);
}, [prevActivePivot]);


  function toggle() {
    setIsActive(!isActive);
  }

  function reset() {
    setSeconds(0);
    setIsActive(false);
  }

  function call_setSeconds() {
    setSeconds(seconds => seconds + 1); 
    const remainder = seconds % 2;
    console.log('I am call_setSeconds, remainder:', remainder);
    if (remainder == 0) {
      setSeconds(seconds => 1);
      getNotes();
    }
  }

  function getNotes() {
    axios({ //axios return a promise
        method: "GET",
        url:"/check_now/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
      }).then((response)=>{
        const data = response.data
        setNotes(data); // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
        //console.log(notes);
        //console.log("estoy aca2");
        // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
        //and this updates the GLOBAL state variable "notes"  with a new state.
        // Thus the value of the state variable changes from null to the data in the received response.

        console.log("-----------axios received", data)
        const newLastLineWebsocket = data[data.length - 1]?.last_line_websocket;
        //if (newLastLineWebsocket == prevLastLineWebsocket) {
        if (newLastLineWebsocket !== prevLastLineWebsocket) {
          console.log("not equal");
         // console.log("equal");
          setPrevLastLineWebsocket(newLastLineWebsocket);
          setSameLastLineWebsocketCounter(0);
        } else {
          console.log("equal , increase counter", sameLastLineWebsocketCounter);
        //  console.log("not equal , increase counter", sameLastLineWebsocketCounter);
          setPrevLastLineWebsocket(newLastLineWebsocket);
          setSameLastLineWebsocketCounter((count) => count + 1);
        }

        //const newActive_Pivot = data[data.length - 1]?.active_pivot;
        //if (newActive_Pivot !== prevActivePivot  ) {
         // console.log("not equal");
         // console.log("newActivePivot", newActive_Pivot);
         // console.log("prevActivePivot", prevActivePivot);
         // setPrevActivePivot(newActive_Pivot);
         // console.log("prevActivePivot after set", prevActivePivot);
         // setSameActivePivotCounter(0);
        //} else {
         // console.log("equal , increase counter", sameActivePivotCounter);
         // setSameActivePivotCounter((count) => count + 1);
          //if (sameActivePivotCounter == 10) {
          //console.log(" counter ==  10, set to 9", sameActivePivotCounter);
          //setSameActivePivotCounter(9);
          //} else { setSameActivePivotCounter((count) => count + 1);}
        //}
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
        <h1>check_now</h1>
        { notes && notes.map(note => <List_check_now_auto
        date_now={note.date_now}
        timestamp_epoch={note.timestamp_epoch}
        active_pivot_pnl={note.active_pivot_pnl} 
        nearest_price_to_put_in_position={note.nearest_price_to_put_in_position}
        active_pivot={note.active_pivot} 
        last_line_websocket={note.last_line_websocket}
        //same_active_pivot_counter={sameActivePivotCounter}
        same_last_line_websocket_counter={sameLastLineWebsocketCounter}
        size={note.size}
        resize={note.resize}
        repeat={note.repeat}
        pivots_to_entry={note.pivots_to_entry}
        to_goal={note.to_goal}
        pivot_count_in_position={note.pivot_count_in_position}
        pivot_count_total={note.pivot_count_total}
        markprice={note.markprice}
        check_run_fake_order={note.check_run_fake_order}
        prev_pivot_tp={note.prev_pivot_tp}
        next_pivot_list_of_dicts={note.next_pivot_list_of_dicts}
        entry_price={note.entry_price}
        position_size={note.position_size}
        />
        )} 
    <div className="app">
      <div className="time">
        {seconds}s
       {/*<p>-------------------rendered </p>
       <p>Same last line websocket counter: {sameLastLineWebsocketCounter}</p>
       <p>Same active_pivot_counter: {sameActivePivotCounter}</p>
        {isRendered && <p>Component was rendered at {new Date().toLocaleString()}</p>}*/}
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