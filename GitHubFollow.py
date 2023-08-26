import datetime as dt
import json
import time

import requests
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from lib import Environment

ENV = Environment("GITHUB-FOLLOW")
HEADER = f"--header 'Authorization: Bearer {ENV.TOKEN}'"


def _get_followers_from_github(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"Bearer {ENV.TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    time.sleep(2)
    return data["followers"]


def _check(followers, followings):
    data = {}
    result = {
        -1: [],
        0: [],
        1: [],
    }
    for follower in followers:
        data[follower["login"]] = [1, follower["html_url"]]
    for following in followings:
        if following["type"] == "Organization":
            continue
        if 1000 < _get_followers_from_github(following["login"]):
            continue
        try:
            data[following["login"]][0] -= 1
        except:
            data[following["login"]] = [-1, following["html_url"]]
    for id, val in data.items():
        result[val[0]].append((id, val[1]))
    return result


def _make_result(result):
    messages = []
    res = ""
    title = {
        -1: "Only Following",
        0: "Following & Follower",
        1: "Only Follwer",
    }
    for i in [-1, 1]:
        tmp = f"# :exclamation: {title[i]}\n"
        if len(res) + len(tmp) > 2000:
            messages.append(res)
            res = tmp
        else:
            res += tmp
        for j, k in enumerate(result[i]):
            id, url = k
            tmp = f"{j+1}. [{id}]({url})\n"
            if len(res) + len(tmp) > 2000:
                messages.append(res)
                res = tmp
            else:
                res += tmp
    messages.append(res)
    return messages


def _send_discord_message(webhook_url, content):
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response


def _check_follow(ti):
    result_from_git_followers = ti.xcom_pull(task_ids="git_followers")
    result_from_git_following = ti.xcom_pull(task_ids="git_following")
    result_from_git_followers = json.loads(result_from_git_followers)
    result_from_git_following = json.loads(result_from_git_following)
    result = _check(result_from_git_followers, result_from_git_following)
    messages = _make_result(result)
    for message in messages:
        _send_discord_message(ENV.WEBHOOK, message)
        time.sleep(2)


@dag(
    dag_id="GitHub-Follow",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 8 * * *",
    catchup=False,
    tags=["Discord", "GitHub"],
)
def github_follow():
    git_followers = BashOperator(
        task_id="git_followers",
        bash_command=(
            f"""result=$(curl {HEADER} -s 'https://api.github.com/users/{ENV.ID}/followers?per_page={ENV.PER_PAGE}'); """
            """echo \"$result\" | tr -d '\n'"""
        ),
    )

    git_following = BashOperator(
        task_id="git_following",
        bash_command=(
            f"""result=$(curl {HEADER} -s 'https://api.github.com/users/{ENV.ID}/following?per_page={ENV.PER_PAGE}'); """
            """echo \"$result\" | tr -d '\n'"""
        ),
    )

    check_follow = PythonOperator(
        task_id="check_follow", python_callable=_check_follow,
    )

    [git_followers, git_following] >> check_follow


DAG = github_follow()
