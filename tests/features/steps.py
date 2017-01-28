from aloe import *
import app
from app.kindle_sync import KindleSync

@step(r"I am using kindle-sync")
def load_kindle_sync(step):
    print('loading kindle-sync')
    world.kindle_sync = KindleSync()
    
@step('user credentials')
def load_config(step):
    print('loading config')
    world.user_name = app.config.kindle_user
    world.password = app.config.kindle_pwd
    
@step('log in to kindle cloud reader')
def login(step):
    print('logging into Kindle cloud reader')
    world.kindle_sync.login(world.user_name, world.password)
    