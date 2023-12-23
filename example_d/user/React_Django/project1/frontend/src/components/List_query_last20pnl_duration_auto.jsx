function List_query_last20pnl_duration_auto(props){
    const count_7days = props.count_7days
    const count_24hs = props.count_24hs
    const last20 = props.last20pnl_list
    const last20rp = props.last20rp_list
    const seconds_since_last_pnl = props.seconds_since_last_pnl
    return (
        <div>
          <p>{props.date_now} </p>
          {/* <p>timestamp: {props.timestamp_epoch} </p> */}
          <table>
            <tr>
              <td>
                <table className="last20pnl">
                  <tr>
                    <td>count ( last24hs )<br /> count ( avg daily of last 7days )</td>
                  </tr>
                  <tr>
                    <td>seconds_since_last_pnl</td>
                  </tr>
                </table>
              </td>
              <td>
                <table className="last20pnl">
                  <tr>
                    <td>{count_24hs} <br />{count_7days}</td>
                  </tr>
                  <tr>
                    <td>{seconds_since_last_pnl}</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td>
                <table className="last20pnl">
                  <tr>
                    <td>time btw pnls<br />new..old</td>
                  </tr>
                    {last20.map(pnl_duration => <tr><td>{pnl_duration}</td></tr>)}
                </table>
              </td>
              <td>
                <table className="last20pnl">
                  <tr>
                    <td>rp<br />new..old</td>
                  </tr>
                    {last20rp.map(rp => <tr><td>{rp}</td></tr>)}
                </table>

              </td>
            </tr>
          </table>
        </div>
    )
  }

export default List_query_last20pnl_duration_auto; 


