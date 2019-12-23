"""
Called at runtime by BackgrounderMixIn

This is WIP
"""
import sys
import pickle
import typing
import time
import presalytics.lib.widgets.backgrounder

backgrounder_instance: presalytics.lib.widgets.backgrounder.BackgrounderMixIn = None
process_identifier = None
sleep_interval = 300
keep_open = True
start_time = time.time()

while keep_open is True:
    new_data = sys.stdin.readlines()
    obj = pickle.load(new_data)
    if isinstance(obj, presalytics.lib.widgets.backgrounder.BackgrounderMixIn):
        backgrounder_instance = obj
    if isinstance(obj, dict): 
        if obj.get("keep_open", None):
            keep_open = obj.get("keep_open")
        if obj.get("process_identifer"

    if backgrounder_instance and process_identifier:
        backgrounder_instance.execute()
    else:
        runtime = time.time - start_time
        if runtime > sleep_interval:
            keep_open = False

        


        
