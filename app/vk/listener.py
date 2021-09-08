from app.core.config import *
from os import path
import json
from typing import List, Dict, Callable
import threading
from fastapi import FastAPI
from settings import ROOT_PATH
import logging
from app.kafka.kafka_connect import produce_to_topic


def get_last_post() -> Dict:
    """Gets the last collected post if it exists, otherwise it creates new last_post.json file"""
    last_post = None  # json of the last post
    if path.exists(path.join(ROOT_PATH, "app/app_data/last_post.json")):
        last_post_file = open(path.join(ROOT_PATH, "app/app_data/last_post.json"), "r")
        try:
            last_post = json.loads(last_post_file.read())
            if not last_post or not last_post['date']:
                raise
        except:
            last_post_file = open(path.join(ROOT_PATH, "app/app_data/last_post.json"), "w")
            last_post_file.write(json.dumps({"date": 0}))
            last_post = json.loads("{\"date\":0}")
    else:
        last_post_file = open(path.join(ROOT_PATH, "app/app_data/last_post.json"), "w")
        last_post_file.write(json.dumps({"date": 0}))
        last_post = json.loads("{\"date\":0}")
    return last_post


def get_posts(vk_api_instance) -> List:
    """Collects all the posts from all the configured communities"""
    all_posts = []
    for community in communities:
        response = vk_api_instance.wall.get(domain=community, count=POSTS_NUMBER)
        all_posts += response["items"]
    return all_posts


def get_only_new_posts(all_posts, last_post) -> List:
    """Collects only posts, that are younger than the last post we collected"""
    new_posts = []
    last_post_date = last_post["date"]
    all_posts.sort(key=lambda x: x['date'])  # Sort by ascending order
    for post in all_posts:
        if last_post_date < post["date"]:
            new_posts.append(post)
            last_post_date = post["date"]
    with open(path.join(ROOT_PATH, "app/app_data/last_post.json"), "w") as last_post_file:
        last_post_file.write(json.dumps({"date": last_post_date}))
    return new_posts


def produce_posts(app: FastAPI) -> Callable:
    """Produces new posts after each iteration of posts collecting"""
    def produce():
        new_posts = get_only_new_posts(get_posts(app.state.api_vk), get_last_post())
        if not new_posts:
            # print("NO new posts this iteration!")
            logging.info("No new posts this iteration!")
        else:
            for post in new_posts:
                # print(i)
                produce_to_topic("posts", app, post)  # Produce post to kafka with topic "posts"
                logging.info('Post: ' + str(post['id']) + " was collected!")
    return produce


def repeat_every(seconds: int, func: Callable):
    """Repeat function each iteration with period of `seconds`"""
    timer_thread = threading.Timer(seconds, repeat_every, [seconds, func])
    timer_thread.setDaemon(True)
    timer_thread.start()
    func()


def start_listening(app: FastAPI):
    """Starts listening to the vk communities with configured period"""
    repeat_every(PERIOD, produce_posts(app))


# if __name__ == "__main__":
#     start_listening()
