from dask.distributed import Client, SSHCluster
import dask.bag as db
import dask.dataframe as dd
import numpy as np
import json
import os
import time
#import re
from IPython.display import clear_output


class ClusterError(Exception):
    pass



def ClusterStarter(nworkers=3):
    scheduler = "10.67.22.173" #  vm : mapdb-group9-2
    worker1 = "10.67.22.153" # vm : mapdb-group9-2
    worker2 = "10.67.22.150" # vm : mapdb-group9-3
    worker3 = "10.67.22.183" # vm : mapdb-group9-4
    number = nworkers+1
    lalistadeiworker = [scheduler,worker1,worker2, worker3][:number]

    try: ## This starts the cluster but if it was started and not closed, this will raise error, so
        cluster = SSHCluster(
        lalistadeiworker,
        connect_options={"known_hosts": None, "username": "ubuntu"},
        scheduler_options={"port": 8786, "dashboard_address":":8797"},
        worker_options={
            "local_directory": '/home/ubuntu/temp_files/',
            #'nthreads':1,
            "memory_limit":"auto",
            'memory_target_fraction':0.7,
            'memory_spill_fraction':0.8,
            'memory_pause_fraction':0.9#,
            #'max_spill':1e9
            },
        remote_python = '/home/ubuntu/miniconda3/bin/python'
        )
        client = Client(cluster)
    except RuntimeError: # this is how to resume the cluster
        clear_output()
        client = Client(scheduler + ':8786') # restarts the cluster, by simply recalling it

    display(client)
    time.sleep(3)
    if len(client.ncores())!=nworkers:
        raise ClusterError(f"ClusterError: The cluster is not properly set: n.{len(client.ncores())} instead of {nworkers} ")
    else:
        pass

    return client

