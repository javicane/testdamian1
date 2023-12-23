function List_check_now_auto(props){
    const value = ((100 * props.active_pivot / props.prev_pivot_tp) - 100).toFixed(5)
    return (
        <div >
          <p>{props.date_now} | timestamp: {props.timestamp_epoch} </p>
          <table style={{ width: '750px' }} border={1} className="check_now_css">
            <tr>
              <td>Next PNL</td>
              <td colSpan={4} style={{ fontSize: '22px' }} className="app_not_center">{props.next_pivot_list_of_dicts}</td>
            </tr>
            <tr>
              <td>Next Pivot</td>
              <td colSpan={4} style={{ fontSize: '22px' }} className="app_not_center">{props.next_pivot_list_of_dicts}</td>
            </tr>
            <tr>
              <td></td>
              <td>TP</td>
              <td>TC</td>
              <td>Size</td>
              <td>Resize | Repeat</td>
            </tr>
            <tr>
              <td>Current</td>
              <td className="app_not_center">{props.active_pivot}</td>
              <td style={{backgroundColor:"#336699"}} className="app_not_center">{props.active_pivot_pnl}</td>
              <td>{props.size}</td>
              <td>{props.resize} | {props.repeat}</td>
            </tr>
            <tr>
              <td>Prev</td>
              <td colSpan={4} style={{ fontSize: '22px' }} className="app_not_center">{props.nearest_price_to_put_in_position}</td>
            </tr>
            <tr>
              <td>Mark</td>
              <td colSpan={2} style={{fontWeight:"bold"}} className="app_not_center">{props.markprice}</td>
              <td>EP(on last pnl)</td>
              <td colSpan={1} style={{fontWeight:"bold"}} className="app_not_center">{props.entry_price}</td>
            </tr>
            <tr>
              <td>Distance_To_Prev</td>
              <td>{ value } %</td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            {/*<tr>
              <td>distance_control_gap 0.125 + 5% delta</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ value >= 0.125*1.05 ? "gap_detected" : "gap_ok" }</td>
    </tr>*/}
            <tr >
              <td>To_Entry</td>
              <td>Deep</td>
              <td>Position_Size</td>
              <td>Pivot_Count_Total</td>
              <td>To_10.4K</td>
              <td></td>
            </tr>
            <tr className="app_not_center">
              <td className={props.pivots_to_entry > 0 ? "app_red" : "app_not_center"}>{props.pivots_to_entry}</td>
              <td className= "app_not_center" style={{ backgroundColor: props.pivot_count_in_position === 0 && "#b38f00"  }}>  {props.pivot_count_in_position}</td>
              <td>{props.position_size}</td>
              <td>{props.pivot_count_total}</td>
              <td>{props.to_goal}</td>
              <td></td>
            </tr>
            <tr>
              <td colSpan={1} style={{ fontSize: '18px', backgroundColor: props.markprice > props.active_pivot_pnl ? "#9e3030" : "#336600" }}>  {"OK if(Mark < TC)"}</td>
              <td colSpan={1} style={{ fontSize: '18px', backgroundColor: props.same_last_line_websocket_counter > 1 ? "#9e3030" : "#336600" }}>  {"WS_Counter: " + props.same_last_line_websocket_counter}</td>
              {/* <td colSpan={4} style={{ fontSize: '18px', backgroundColor: props.check_run_fake_order !== "OK" ? "#9e3030" : "#336600" }}>  {props.check_run_fake_order}</td> */}
              <td colSpan={3} style={{ fontSize: '18px', backgroundColor: props.check_run_fake_order !== "OK" ? "#9e3030" : "#336600" }}>
                {"Check_Run_Fake_Order: " + props.check_run_fake_order}
              </td>
            </tr>
            <tr>
              {/* <td colSpan={4} style={{ width: '950px', whiteSpace: 'normal' }} >{props.last_line_websocket}</td> */}
              <td colSpan={5} style={{ width: '500px', whiteSpace: 'normal', height: '100px', maxHeight: '500px', overflowY: 'auto' }} >{props.last_line_websocket}</td>
          </tr>
        </table>
               
        </div>
    )
  }

export default List_check_now_auto;


