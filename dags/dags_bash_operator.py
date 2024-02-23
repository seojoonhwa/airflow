from airflow import DAG
import datetime
import pendulum
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="dags_bash_operator", #dag_id는 airflow UI에서 보이는 DAG 이름 python 파일명과는 상관없지만, 일반적으로 Dag 파일명과 일치시킨다
    schedule="0 0 * * *", # cron 스케줄 (분 시 일 월 요일)
    start_date=pendulum.datetime(2024, 2, 1, tz="Asia/Seoul"), # dag이 언제부터 돌건지
    #catchup=False, 데이터 소급 적용 여부, 일반적으로는 False로 해놓음
    #dagrun_timeout=datetime.timedelta(minutes=60), timeout 값 설정
    #tags=["example", "example2"], # airflow UI에서 DAG 이름 밑에 하늘색 박스
    #params={"example_key": "example_value"},  task들에 공통적으로 적용할 params
) as dag:
    # [START howto_operator_bash]
    bash_t1 = BashOperator( # bash_t1 -> task 객체명
        task_id="bash_t1", # Graph에 나오는 이름 주로 객체명과 동일하게 한다
        bash_command="echo whoami", # 명령어 실행문
    )
    # [END howto_operator_bash]

    # [START howto_operator_bash]
    bash_t2 = BashOperator( # bash_t1 -> task 객체명
        task_id="bash_t2", # Graph에 나오는 이름 주로 객체명과 동일하게 한다
        bash_command="echo $HOSTNAME", # 명령어 실행문
    )
    # [END howto_operator_bash]

    bash_t1 >> bash_t2 # task 실행 순서