# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id='dags_trigger_dag_run_operator',
    start_date=pendulum.datetime(2024,3,1, tz='Asia/Seoul'),
    schedule='30 9 * * *',
    catchup=False
) as dag:

    start_task = BashOperator(
        task_id='start_task',
        bash_command='echo "start!"',
    )

    trigger_dag_task = TriggerDagRunOperator(
        task_id='trigger_dag_task',                 # 필수값
        trigger_dag_id='dags_python_operator',      # 필수값
        trigger_run_id=None,                        # Run_id 값 직접 지정정
        execution_date='{{data_interval_start}}',   # manual__{{execution_date}} 로 수행
        reset_dag_run=True,                         # 이미 run_id 값이 있는 경우에도 재수행할 것인지
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=['success'],
        failed_states=None
        )

    start_task >> trigger_dag_task