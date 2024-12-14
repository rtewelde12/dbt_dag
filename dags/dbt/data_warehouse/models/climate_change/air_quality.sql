{{ 
  config(
    materialized = 'table',
    tags = ['my_tag']
  ) 
}}

with final as (
    select
        "Unique ID",
        "Indicator ID",
        "Name",
        "Measure",
        "Measure Info",
        "Geo Type Name",
        "Geo Join ID",
        "Geo Place Name",
        "Time Period",
        "Start_Date",
        "Data Value",
        "Message"

    from {{ ref('air_quality_seed') }}
)

select * from final
