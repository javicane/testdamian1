//import Note from "./Notes"
//import Header from "./Header"
import Header2 from "./Header2"
//import Footer from "./Footer"
//import Q_tracker_pnl from "./Notes_tracker_pnl"
//import Q_min_pivot from "./Notes_min_pivot"
//import Q_check_now from "./Notes_check_now"
//import Timer from "./Timer"
import Q_min_pivot_auto from "./Notes_min_pivot_auto"
import Q_check_now_auto from "./Notes_check_now_auto"
import Q_tracker_pnl_auto from "./Notes_tracker_pnl_auto"
//import Query_pivots_in_range from "./Query_pivots_in_range"
import Check_dangling from "./Notes_dangling_auto"
import Query_last20pnl_duration_auto from "./Notes_query_last20pnl_duration_auto"
//import Query_pivots_by_price_range_auto from "./Notes_query_pivots_by_price_range_auto"
//import Tt from "./Notes_tt"
import Create_sell_order from "./Notes_create_sell_order"
import Cancel_order from "./Notes_cancel_order"
import Cancel_order_bulk_by_price_range from "./Notes_cancel_order_bulk_by_price_range"
import Resize_pivot from "./Notes_resize_pivot"
import Sql_query from "./Notes_sql_query"
import Update_repeat_pivot from "./Notes_update_repeat_pivot"
import Drift_report_pivot_distance from "./Notes_drift_report_pivot_distance"
import Pivot_frequency from "./Notes_pivot_frequency"
import Query_top_pivots_to_increase from "./Notes_query_top_pivots_to_increase"
import ToggleVisibility from "./ToggleVisibility"
import Resize_order_buy from "./Notes_resize_order_buy" 
import Create_Pivot_Buy from "./Notes_create_pivot_buy"
import Show_Group_Id from "./Notes_show_group_id"
import Update_Group_Id from "./Notes_update_group_id"
import LineChartComponent from "./Notes_graph"
import Rp_Graph from "./Notes_rp_graph"
import Damian from "./Damian"
//import Damian2 from "./MiniTest"
//import InputValidationExample from "./Damianinputvalidation"
//import Toggle from "./Notes_toggle"
//import D3 from "./Appd3"
//import WebImage from "./WebImage"
//import PublicImage from "./PublicImage"
//import pic from "../images/mercury.jpg"

function Titulo({children}) {

  return (
    <div className="note">
      {children}
    </div>
  );
}

function App() {

  const titulo = "hola";
  return (
      <div className='App'>
        <Header2 />
        {/* <D3 /> */}
        <Query_last20pnl_duration_auto />
        <Check_dangling />
        <Q_tracker_pnl_auto />
        <Q_check_now_auto />
        {/* <Query_pivots_by_price_range_auto /> */}
        <Titulo> 
          <h1>show_group_id | update_group_id</h1>
          <ToggleVisibility>
            <Show_Group_Id />
            <Update_Group_Id />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>create_sell_order | create_pivot_buy | cancel_order</h1>
          <ToggleVisibility>
            <Create_Pivot_Buy />
            <Create_sell_order />
            <Cancel_order />
            <Cancel_order_bulk_by_price_range />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>resize_pivot | update_repeat_pivot(toggle) | resize_order_buy</h1>
          <ToggleVisibility>
            <Resize_pivot />
            <Update_repeat_pivot />
            <Resize_order_buy />
          </ToggleVisibility>
        </Titulo>


        <Titulo> 
          <h1>sql_query</h1>
          <ToggleVisibility>
            <Sql_query />
          </ToggleVisibility>
        </Titulo>
       
        <Titulo> 
          <h1>drift_report_pivot_distance</h1>
          <ToggleVisibility>
            <Drift_report_pivot_distance />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>query_min_pivot | pivot frequency</h1>
          <ToggleVisibility>
            <Q_min_pivot_auto />
            <Pivot_frequency />
          </ToggleVisibility>
        </Titulo>


        <Titulo> 
          <h1>query_top_pivots_to_increase</h1>
          <ToggleVisibility>
            <Query_top_pivots_to_increase />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>LineChart</h1>
          <ToggleVisibility>
            <LineChartComponent />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>List_rp</h1>
          <ToggleVisibility>
            <Rp_Graph />
          </ToggleVisibility>
        </Titulo>

        <Titulo> 
          <h1>Damian</h1>
          <ToggleVisibility>
            <Damian />
          </ToggleVisibility>
        </Titulo>

        {/* <Toggle /> */}
        {/* <Tt /> */}
      </div>
  );
}
export default App;
