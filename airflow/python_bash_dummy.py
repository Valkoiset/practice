import datetime

from airflow import models
from airflow.operators import bash_operator
from airflow.operators import python_operator
from airflow.operators import dummy_operator

yesterday = datetime.datetime.combine(
  datetime.datetime.today() - datetime.timedelta(1),
  datetime.datetime.min.time()
)

default_dag_args = {
  'start_date': yesterday
}

with models.DAG(
  'running_python_and_dummy_operator',
  schedule_interval=datetime.timedelta(days=1),
  default_args=default_dag_args) as dag:

  def greeting():
    print('Greetings from SpikeySales! Happy shopping.')
    return 'Greeting successfully printed.'

  python_greeting = python_operator.PythonOperator(
    task_id='hello_python',
    python_callable=greeting
  )

  bash_greeting = bash_operator.BashOperator(
    task_id='bye_bash',
    bash_command='echo Goodbye! Hope to see you soon.'
  )

  end = dummy_operator.DummyOperator(task_id='dummy')

  python_greeting >> bash_greeting >> end
