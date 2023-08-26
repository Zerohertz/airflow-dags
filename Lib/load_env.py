import json

from airflow.models.variable import Variable


class Environment:
    def __init__(self, ENV):
        ENV = Variable.get(ENV)
        ENV_data = json.loads(ENV)
        for key, value in ENV_data.items():
            setattr(self, key, value)
