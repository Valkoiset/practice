import datetime

from airflow import models
from airflow.operators import bash_operator
from airflow.operators import python_operator
from airflow.utils import trigger_rule

yesterday = datetime.datetime.combine(
  datetime.datetime.today() - datetime.timedelta(1),
  datetime.datetime.min.time()
)

default_dag_args = {
  'start_date': yesterday,
  'retries': 1,
  'retry_delay': datetime.timedelta(minutes=2)
}


with models.DAG(
  'python_and_bash_with_all_success_trigger',
  schedule_interval=datetime.timedelta(days=1),
  default_args=default_dag_args) as dag:

  def hello_world():
    raise ValueError('Oops! Something went wrong.')
    print('Hello World!')
    return 1

  def greeting():
    print('Greetings from SpikeySales! Happy shopping.')
    return 'Greeting successfully printed.'

  hello_world_greeting = python_operator.PythonOperator(
    task_id='python_1',
    python_callable=hello_world
  )

  spikeysales_greeting = python_operator.PythonOperator(
    task_id='python_2',
    python_callable=greeting
  )

  bash_greeting = bash_operator.BashOperator(
    task_id='bye_bash',
    bash_command='echo Goodbye! Hope to see you soon.',
    # dure to this role bash operator will never be triggered in this DAG because it goes after task 'hello_world_greeting' which is not
    # executed successfully because we intentionaly put raise ValueError in it to demonstrate how all_success rule works
    trigger_rule=trigger_rule.TriggerRule.ALL_SUCCESS
  )

  hello_world_greeting >> spikeysales_greeting >> bash_greeting
