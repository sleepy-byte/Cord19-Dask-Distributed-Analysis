# Project journal

To improve communication within the team and make it easier to resume paused tasks, each member could briefly write down what they did each day and why.

## 26/06
### Gigi
Setting up cluster: to be decided between 2 config: 
 - 4 VMs: 1 scheduler + 3 workers
 - 4 VMs: 1 scheduler AND worker + 3 workers

Learning how to deal w/ cluster and client, how to deal with persistence of cluster when it is not closed.

More details about it on README.md.

Pushed zipped dataset on scheduler-vm.

# 27/06

### Gigi

Today I explored how to deal with the data, where to store the dataset, how is managed by mask. I tried streaming the dataset from my PC but discovered that the scheduler only gives orders to workers it does not pass data, so data streaming is unfeasible.

I settled in launching a dedicated VM as NFS (Network File System) and mounting it on all workers. Tomorrow after filling the NFS servers everything should be ready to go.