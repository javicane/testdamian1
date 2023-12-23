function List_dangling_auto(props){
    return (
        <div> 
          <p>{props.date_now} </p>
          {/*<p>timestamp: {props.timestamp_epoch} </p>*/}
          <table className={ props.dangling === 1 ? "app_red_small_font" : "app_not_center_small_font" }>
            <tr>
              <td>dangling</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.dangling === 1 ? "YES" : "NO" }</td>
            </tr>
            <tr>
              <td>partially_filled</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.partially_filled === 1 ? "YES" : "NO" }</td>
            </tr>
            <tr>
              <td>expired</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.expired === 1 ? "YES" : "NO" }</td>
            </tr>
            <tr>
              <td>flag_dangling_check1_only</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.flag_dangling_check1_only === 1 ? "YES" : "NO" }</td>
            </tr>
            <tr>
              <td>result_dangling_check1</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.result_dangling_check1 }</td>
            </tr>
            <tr>
              <td>flag_dangling_check2</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.flag_dangling_check2 }</td>
            </tr>
            <tr>
              <td>flag_dangling_check3</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.flag_dangling_check3 }</td>
            </tr>
            <tr>
              <td>flag_dangling_check4</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.flag_dangling_check4 }</td>
            </tr>
            <tr>
              <td>result_dangling_check4</td>
              <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
              <td>{ props.result_dangling_check4 }</td>
            </tr>
          </table>
        </div>
    )
  }

export default List_dangling_auto;


