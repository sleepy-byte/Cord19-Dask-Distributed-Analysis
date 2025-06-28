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

## 27/06

### Gigi

Today I explored how to deal with the data, where to store the dataset, how is managed by mask. I tried streaming the dataset from my PC but discovered that the scheduler only gives orders to workers it does not pass data, so data streaming is unfeasible.

I settled in launching a dedicated VM as NFS (Network File System) and mounting it on all workers. Tomorrow after filling the NFS servers everything should be ready to go.

## 28/06

### Gigi

After acknowlegding the only feasible (and compatible with the horizontal scalability logic) way of setting up data locality, I set up and filled NFS server. Today I will experiment a bit with how the cluster actually access the data. 

I filled the nfs server (`10.67.22.227`) with two version of the dataset, v30 and v50. 

Also, forgot to mention that since our VMs are single core I thought that the structure 4VMs : 1 Scheduler and worker + 3 worker, is not that good bc we would have a machine that struggles in doing both tasks.

