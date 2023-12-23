from django.contrib import admin
from django.urls import path
from core.views import front, note, note_detail, query_min_pivot_view, query_tracker_pnl_view,\
    query_min_pivot_view, check_now_view, post_query_pivots, check_dangling, query_last20pnl_duration,\
    query_pivots_by_price_range_view, create_sell_order_view , cancel_order_view, resize_pivot_view, sql_query_view, update_repeat_pivot_view, \
    drift_report_pivot_distance_view, pivot_frequency_all_view, pivot_frequency_last7days_view, pivot_frequency_last3days_view, \
    pivot_frequency_last24hs_view, cancel_order_bulk_by_price_range_view, query_top_pivots_to_increase_view, resize_order_buy_view, create_pivot_buy_view, show_group_id_view, \
    update_group_id_view, rp_graph_view, zaraza_view, pivot_frequency_all_with_id_view
from core.views_zaraza import front_zaraza, note_zaraza, note_detail_zaraza

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", front, name="front"),
    #path("front_zaraza/", front_zaraza, name="front_zaraza"), # se rompe si uso este
    #path("notes_zaraza/", note_zaraza, name="note_zaraza"),
    #path("notes_zaraza/<int:pk>/", note_detail_zaraza, name="detail_zaraza"),
    path("notes/", note, name="note"),
    path("query_tracker_pnl/", query_tracker_pnl_view, name="query_tracker_pnl"),
    path("query_min_pivot/", query_min_pivot_view, name="query_min_pivot"),
    path("check_now/", check_now_view, name="check_now"),
    path("post_query_pivots/", post_query_pivots, name="post_query_pivots"),
    path("notes/<int:pk>/", note_detail, name="detail"),
    path("check_dangling/", check_dangling, name="check_dangling"),
    path("query_last20pnl_duration/", query_last20pnl_duration, name="query_last20pnl_duration"),
    path("query_pivots_by_price_range/", query_pivots_by_price_range_view, name="query_pivots_by_price_range_view"),
    path("create_sell_order/", create_sell_order_view, name="create_sell_order"),
    path("cancel_order/", cancel_order_view, name="cancel_order"),
    path("cancel_order_bulk_by_price_range/", cancel_order_bulk_by_price_range_view, name="cancel_order_bulk_by_price_range"),
    path("resize_pivot/", resize_pivot_view, name="resize_pivot"),
    path("resize_order_buy/", resize_order_buy_view, name="resize_order_buy"),
    path("create_pivot_buy/", create_pivot_buy_view, name="create_pivot_buy"),
    path("sql_query/", sql_query_view, name="sql_query"),
    path("update_repeat_pivot/", update_repeat_pivot_view, name="update_repeat_pivot"),
    path("drift_report_pivot_distance/", drift_report_pivot_distance_view, name="drift_report_pivot_distance"),
    path("pivot_frequency_all/", pivot_frequency_all_view, name="pf_all"),
    path("pivot_frequency_last7days/", pivot_frequency_last7days_view, name="pf_7"),
    path("pivot_frequency_last3days/", pivot_frequency_last3days_view, name="pf_3"),
    path("pivot_frequency_last24hs/", pivot_frequency_last24hs_view, name="pf_24hs"),
    path("query_top_pivots_to_increase/", query_top_pivots_to_increase_view, name="query_top_pivots_to_increase"),
    path("show_group_id/", show_group_id_view, name="show_group_id"),
    path("update_group_id/", update_group_id_view, name="update_group_id"),
    path("rp_graph/", rp_graph_view, name="rp_graph"),
    path("zaraza/", zaraza_view, name="zaraza"),
    path("with_id/", pivot_frequency_all_with_id_view , name="with_id")
]