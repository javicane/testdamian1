function List_min_pivot_auto(props){
   return (
      <div >
        <p>{props.date_now} </p>
        <p>timestamp: {props.timestamp_epoch} </p>
         <table className="app_not_center">
          <tr>
            <td>min_pivot</td>
          </tr>
          <tr>
            <td>{props.min_pivot}</td>
          </tr>
        </table>
      </div>
  ) 
  }
export default List_min_pivot_auto;

         //<table className={props.min_pivot < 0.5 ? "app_red" : "app_not_center"}>