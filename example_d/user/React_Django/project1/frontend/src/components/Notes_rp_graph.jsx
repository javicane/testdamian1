import React, { useState, useEffect } from 'react';
import axios from "axios";
import List_rp from './List_rp';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine } from 'recharts';


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
        url:"/rp_graph/", // in package.json see the pointer to django url "proxy": "http://localhost:8000",
      }).then((response)=>{
        const data = response.data
        func_for_state(data); // When the GET request is made with axios, the data in the received response is assigned to the query_pnl_tracker function, 
        //console.log(notes);
        //console.log("estoy aca2");
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
      interval = setInterval(call_setSeconds, 1000);
    } else if (!isActive && seconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, seconds]);

  return (
  <div className="note">
        <h1>rp_graph</h1>
    <LineChart width={800} height={400} data={notes}>
      <CartesianGrid strokeDasharray="3 3" />
      {/*<XAxis dataKey="timestamp" hide={true} />*/}
      <XAxis dataKey="timestamp_epoch" hide={true} />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="rp" stroke="#8884d8" dot={false} />
      <ReferenceLine y={0} stroke="red" label="0" />
    </LineChart>
      {/*<Line type="monotone" dataKey="rp" stroke="#8884d8" activeDot={{ r: 1 }} />*/}
      {/*<Line type="monotone" data={aggregatedData} dataKey="rp" stroke="#82ca9d" />*/}
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

export default Note;