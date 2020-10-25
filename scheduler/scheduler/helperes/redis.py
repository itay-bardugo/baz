from redis import Redis
import os


def connect():
    return Redis(host=os.environ.get("REDIS-HOST"), port=os.environ.get("REDIS-PORT"))
