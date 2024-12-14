import os
import logging
from datetime import datetime
from airflow.utils.email import send_email_smtp
from airflow.operators.dummy import DummyOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos import DbtTaskGroup
from cosmos.profiles import PostgresUserPasswordProfileMapping

# Define the profile configuration for the DBT project.
profile_config = ProfileConfig(
    profile_name="default",  # Name of the DBT profile
    target_name="dev",       # Target environment (dev, prod, etc.)
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_conn",  # Connection ID for PostgreSQL as configured in Airflow
        # Database and schema for DBT
        profile_args={"dbname": "Test", "schema": "dbt"},
    )
)

# Define a function to send an email notification after the DAG run


def notify_email(**context):
    subject = f"DAG {context['dag'].dag_id} Succeeded"
    body = f"Your DAG {context['dag'].dag_id} ran successfully on {context['data_interval_start']}."

    try:
        logging.info("Attempting to send email notification...")
        send_email_smtp(
            to="robel_tewelde@hotmail.com",
            subject=subject,
            html_content=body,
            conn_id="smtp_default"  # Ensure this matches the SMTP connection ID configured in Airflow
        )
        logging.info(f"Email notification sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")


# Define the main Airflow DAG
with DAG(
    dag_id="dbt_dag",
    schedule_interval="@daily",  # Schedule to run the DAG daily
    start_date=datetime(2023, 9, 10),  # The start date for the DAG's schedule
    catchup=False,  # Disable catching up on missed DAG runs
    # Call this function upon successful completion of the DAG
    on_success_callback=notify_email,
) as dag:

    # Start Dummy Task: Marks the start of the pipeline
    start_task = DummyOperator(
        task_id="start_pipeline"
    )

    # End Dummy Task: Marks the end of the pipeline
    end_task = DummyOperator(
        task_id="end_pipeline"
    )

    # Define the DBT tasks for PostgreSQL using DbtTaskGroup
    dbt_task_group = DbtTaskGroup(
        project_config=ProjectConfig(
            # Path to the DBT project in the Airflow DAG directory
            "/usr/local/airflow/dags/dbt/data_warehouse",
        ),
        # Additional operator arguments, like installing dependencies
        operator_args={"install_deps": True},
        profile_config=profile_config,  # Profile configuration defined earlier
        execution_config=ExecutionConfig(
            # Path to the DBT executable within a virtual environment
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
        ),
        render_config=RenderConfig(
            # Disable dataset emission to avoid issues with breaking changes in Airflow
            emit_datasets=False
        ),
    )

    # Define the send email notification task
    send_email_notification = PythonOperator(
        task_id='send_email_notification',
        python_callable=notify_email,
        provide_context=True,  # Ensure that context is passed to the Python callable
    )

    # Set up the dependency chain by linking tasks
    start_task >> dbt_task_group >> send_email_notification >> end_task
