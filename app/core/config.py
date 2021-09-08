import yaml
from settings import ROOT_PATH
import os
import math

with open(os.path.join(ROOT_PATH, "config.yml"), 'r') as config_file:
    data = yaml.load(config_file, Loader=yaml.FullLoader)

LOGIN = data['vk']['login']
PASSWORD = data['vk']['password']
communities = data['vk']['communities']

# period of the api requests (due to the limitations of the 5000 requests ber day)
PERIOD = math.ceil(len(communities)*((24*60*60)/5000))
# PERIOD = 4

# Number of posts to collect each iteration from each community
POSTS_NUMBER = int(data['vk']['number_of_posts'])
