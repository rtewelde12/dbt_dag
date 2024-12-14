{{ 
  config(
    tags = ['my_tag']
  ) 
}}

with final as (
    select
        "date",
        "meantemp",
        "humidity",
        "wind_speed",
        "meanpressure"
    from {{ ref('daily_delhi_climate_test_seed') }}
)

select * from final
