from fastapi import FastAPI
from typing import Callable
from app.vk.auth import get_vk_api_session
from app.vk.listener import start_listening
from app.kafka.kafka_connect import connect_to_kafka, close_kafka_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    """Creates handler for the application startup"""
    def start_app() -> None:
        connect_to_kafka(app)
        get_vk_api_session(app)
        start_listening(app)
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Creates handler for the application shutdown"""
    def stop_app() -> None:
        close_kafka_connection(app)
    return stop_app
