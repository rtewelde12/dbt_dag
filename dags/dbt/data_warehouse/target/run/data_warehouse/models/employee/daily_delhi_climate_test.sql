
  create view "Test"."dbt"."daily_delhi_climate_test__dbt_tmp"
    
    
  as (
    

with final as (
    select 
        "date",
        "meantemp",
        "humidity",
        "wind_speed",
        "meanpressure"

    from "Test"."dbt"."daily_delhi_climate_test_seed"
)

select * from final
  );