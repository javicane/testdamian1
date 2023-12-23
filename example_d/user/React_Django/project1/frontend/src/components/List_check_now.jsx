function List_check_now(props){
      function handleClick(){
    props.get_new_data(props.id)
  }
    return (
        <div className="note">
          <h1 >check_now</h1>
          <p>{props.date_now} </p>
          <p>timestamp: {props.timestamp_epoch} </p>
           <table>
            <tr>
              <td>next_pnl....</td>
              <td>next_in_position</td>
            </tr>
            <tr>
              <td>{props.nearest_pnl}</td>
              <td>{props.nearest_price_to_put_in_position}</td>
            </tr>
          </table>
          <button onClick={handleClick}>Refresh Data</button>
        </div>
    )
  }

export default List_check_now;


