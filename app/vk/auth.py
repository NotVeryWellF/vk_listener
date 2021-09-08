from app.core.config import *
import vk_api
from fastapi import FastAPI


def get_vk_api_session(app: FastAPI):
    """Create an vk api session instance and saves it to the app states"""
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    app.state.api_vk = vk
