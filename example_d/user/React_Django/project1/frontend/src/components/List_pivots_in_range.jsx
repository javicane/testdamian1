function List_pivots_in_range(props){
    console.log("yyyy") 
    const pivots_list = props.pivots_list
    return (
        <div> 
          <p>{props.date_now} </p>
          <p>timestamp: {props.timestamp_epoch} </p>
          <table>
            <tr>
              <td>
                <table className="last20pnl">
                  <tr>
                    <td>pivots<>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</>size<>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</>resize</td>
                  </tr>
                    {pivots_list.map(pivot => <tr><td>{pivot}</td></tr>)}
                </table>
              </td>
            </tr>
          </table>
        </div>
    )
  }

export default List_pivots_in_range;