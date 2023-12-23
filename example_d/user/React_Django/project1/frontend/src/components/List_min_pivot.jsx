function List_min_pivot(props){
      function handleClick(){
    props.get_new_data(props.id)
  }
    return (
        <div className="note">
          <h1>min_pivot</h1>
          <p>{props.date_now} </p>
          <p>timestamp: {props.timestamp_epoch} </p>
          <table>
            <tr>
              <td>min_pivot</td>
            </tr>
            <tr>
              <td>{props.min_pivot}</td>
            </tr>
          </table>
          <button onClick={handleClick}>Refresh Data</button>
        </div>
    )
  }

export default List_min_pivot;


