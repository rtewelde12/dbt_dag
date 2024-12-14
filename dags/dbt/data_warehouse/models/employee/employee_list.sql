{{ 
  config(
    materialized = 'table',
    tags = ['my_tag']
  ) 
}}

with final as (
    select 
        "Employee_ID",
        "Full_Name",
        "Job_Title",
        "Department",
        "Business_Unit",
        "Gender",
        "Ethnicity",
        "Age",
        "Hire_Date",
        "Annual_Salary",
        "Bonus_percentages",
        "Country",
        "City",
        "Exit_Date"
    from {{ ref('employee_seed') }}
)

select * from final
