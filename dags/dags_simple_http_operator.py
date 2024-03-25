# Package Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
import pendulum

with DAG(
    dag_id='dags_simple_http_operator',
    start_date=pendulum.datetime(2024, 3, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None
) as dag:

    '''서울시 버스노선 기본정보 항목정보'''
    tb_busRoute_info = SimpleHttpOperator(
        task_id='tb_busRoute_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/busRoute/1/20/',
        method='GET',
        headers={'Content-Type': 'application/json',
                        'charset': 'utf-8',
                        'Accept': '*/*'
                        }
    )

    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids='tb_busRoute_info')
        import json
        from pprint import pprint

        pprint(json.loads(rslt))
        
    tb_busRoute_info >> python_2()