# What to do if cluster was not close 

and u get this error: `RuntimeError: Cluster failed to start: Worker failed to start`

### Why it happens:
 
To me happened bc i didn't close the cluster and client before closing the jupyter notebook/vs code/ ssh connection.

### How to deal w/ it

On terminal run:
 - ps aux | grep dask
 - pkill -f dask-scheduler
 - pkill -f dask-worker
 - sudo lsof -i :8786
 - sudo kill <PID>  (where the PID is the one on the extreme left)

Then you shoud be able to restart the cluster and client.

Alternative way, less elegant: you manually ssh into each vm and run #sudo reboot


# How to visualize dashboard

After starting the SSHCluster as defined, on your terminal, not the one of VSCode possibly, run

`ssh -L 8797:localhost:8797 scheduler`

and then on your browser open: `http://localhost:8797`

# General warnings:

- Be aware of warning messages of different dask/other packages' versions across VMs. To deal w/ it: Export conda environment from VMs w/ more recent packages and update conda env on other VMs.
-