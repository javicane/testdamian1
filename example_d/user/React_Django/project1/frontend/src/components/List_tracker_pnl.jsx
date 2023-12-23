function List_tracker_pnl(props){
      function handleClick(){
    props.get_new_data(props.id)
  }
    return (
        <div className="note">
          <h1 >  tracker_pnl </h1>
          <p>{props.date_now} </p>
          <p>timestamp: {props.timestamp_epoch} </p>
          <table>
            <tr>
              <td>sum(rp)..........</td>
              <td>rows</td>
            </tr>
            <tr>
              <td>{props.sum_rp}</td>
              <td>{props.rows}</td>
            </tr>
          </table>
          <button onClick={handleClick}>Refresh Data</button>
        </div>
    )
  }

export default List_tracker_pnl;


