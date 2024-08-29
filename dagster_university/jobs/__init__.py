from dagster import AssetSelection, define_asset_job
from dagster_dbt import build_dbt_asset_selection

from ..partitions import monthly_partition, weekly_partition
from ..assets.dbt import dbt_analytics, incremental_dbt_models

trips_by_week = AssetSelection.assets("trips_by_week")
adhoc_request = AssetSelection.assets("adhoc_request")

# memo: stg_trips+ とは、stg_tripsモデルとそれに依存する全ての下流のモデルを指す
dbt_trips_selection = build_dbt_asset_selection([dbt_analytics], "stg_trips")
dbt_incremental_trips_selection = build_dbt_asset_selection([incremental_dbt_models])


trip_update_job = define_asset_job(
    name="trip_update_job",
    partitions_def=monthly_partition,
    selection=AssetSelection.all() - trips_by_week - adhoc_request - dbt_trips_selection - dbt_incremental_trips_selection
)

weekly_update_job = define_asset_job(
    name="weekly_update_job", partitions_def=weekly_partition, selection=trips_by_week
)

adhoc_request_job = define_asset_job(name="adhoc_request_job", selection=adhoc_request)