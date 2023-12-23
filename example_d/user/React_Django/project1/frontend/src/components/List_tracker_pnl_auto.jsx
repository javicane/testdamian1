function List_tracker_pnl_auto(props){
    return (
        <div> 
          <p>{props.date_now} </p>
          {/* <p>timestamp: {props.timestamp_epoch} </p> */}
          <table className={props.sum_rp < 0 ? "app_red_small_font" : "app_not_center_snmall_font"}>
            <tr>
              <td>sum(rp)</td>
              <td>rows</td>
            </tr>
            <tr>
              <td>{props.sum_rp}</td>
              <td>{props.rows}</td>
            </tr>
          </table>
          <table className={"app_not_center_small_font"}>
            <tr>
              <td>rp_last48hs</td>
              <td>rows</td>
              <td>rp_last24hs</td>
              <td>rows</td>
              <td>12hs</td>
              <td>r</td>
              <td>6hs</td>
              <td>r</td>
            </tr>
            <tr>
              <td style={{ backgroundColor: props.sum_rp_last48hs < 0 ? "#9e3030" : "#336600" }}>  {props.sum_rp_last48hs}</td>
              <td>{props.count_rp_last48hs}</td>
              <td style={{ backgroundColor: props.sum_rp_last24hs < 0 ? "#9e3030" : "#336600" }}>  {props.sum_rp_last24hs}</td>
              <td>{props.count_rp_last24hs}</td>
              <td style={{ backgroundColor: props.sum_rp_last12hs < 0 ? "#9e3030" : "#336600" }}>  {props.sum_rp_last12hs}</td>
              <td>{props.count_rp_last12hs}</td>
              <td style={{ backgroundColor: props.sum_rp_last6hs < 0 ? "#9e3030" : "#336600" }}>  {props.sum_rp_last6hs}</td>
              <td>{props.count_rp_last6hs}</td>
            </tr>
            <tr>
              <td>rp_last_7days</td>
              <td>rows</td>
            </tr>
            <tr>
              <td style={{ backgroundColor: props.sum_rp_lastydays < 0 ? "#9e3030" : "#336600" }}>  {props.sum_rp_last7days}</td>
              <td>{props.count_rp_last7days}</td>
            </tr>
          </table>
          <table className="app_not_center_small_font">
            <tr>
              <td>sum(funding_fee)</td>
              <td>rows</td>
            </tr>
            <tr>
              <td>{props.sum_funding_fee}</td>
              <td>{props.rows_funding_fee}</td>
            </tr>
            <tr>
              <td>balance(on last pnl)</td>
              <td>{props.balance}</td>
            </tr>
            <tr>
              <td>entry_price(on last pnl)</td>
              <td>{props.entry_price}</td>
            </tr>
          </table>
        </div>
    )
  }

export default List_tracker_pnl_auto;


