function List_rp(props){
    const rp = props.rp
    const timestamp_epoch = props.timestamp_epoch
    return (
        <div>
          <p>{props.date_now} </p>
                   {/* {last20.map(pnl_duration => <tr><td>{pnl_duration}</td></tr>)}
                    {last20rp.map(rp => <tr><td>{rp}</td></tr>)} */}
        </div>
    )
  }

export default List_rp; 


