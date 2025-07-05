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

## 1/7

### Luke

Tried to compute the number of occurances of words in each file. The function works. Though, when giving the task to the cluster, the cluster crashes, even if given very few files. Don't know what is the reason for that

### UPDATE

I have a working counter in Assignment notebook. It can be improved (I guess). But it works


## 2/7

### Luke

Set up correctly the Assignment notebook for the word count task and grid search for best hyperparameters on speed of the task.

## 3/7

### Gigi

Solved issue of workers that would not work appropriately: I needed to specify the path to the python executable. Now is working. How to adapt:
`import ClusterManager as cm`

`client=cm.ClusterStarter()`

once you done remember: `client.close()`

You can find `ClusterManager` on `/home/ubuntu/ClusterManager.py`

Added NLP model to `/home/ubuntu/data`.

## 4/7 

### Gigi 

Yesterday and this morning i worked o task3. The goal is embedding every title with word-vectors from a model. I made a dataframe from the txt file that has 2.5million words and their vectors (6.1 GiB). The I extracted all the words that appear on our ensemble of paper titles, got the uniques and computed the Dataframe of word-vectors with just the words we need. This was the major challenge bc otherwise the model won't fit in the cluster memory. 

Also I learned that all intermediate variables end in unmanaged memory of the cluster so a good practice is to `del` them asap and sometimes run client.run(gc.collect) to free memory.

Now i have to map titles to model and viceversa.



## 4/7

### Cris 

I create a data frame from the json files. The data frame contains the column "affiliations" that is an object of lists. Each record has a list with the affiliation information for each author of the paper. 

What I made so far: 
- I make a function to load the .json filese
- Create a DASK bag 
- Convert the DASK bag into a Data Frame
 * To do that from a .json file, you need to specify what json obejct you need as a column. 
		* I choosed to get the paper_id, the paper title, the affiliation (the acctual field we need for this part of the project) and the first author. Altrough it is uneccesary to have the other fields besides the 'affiliation', I tought it will may be intereting and useful to extrapolate more information if necessary.
		* Also, the paper may have multiple authors. I choose to get the affiliation field as a list, that contains the information for each author for the paper.  


- The Affiliation section is a mess. The following is an example: 

	'	[{'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}, {'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}, {'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}][{'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}, {'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}, {'laboratory': '', 'institution': 'National Institute of Pharmaceutical Education and Research (NIPER)', 'location': {'postCode': 'Telangana-500037', 'settlement': 'Balanagar, Hyderabad', 'country': 'India'}}]'

	As you can see, the fields of interest (institution and country) are loacated in the midle of the text. So I made a function that grabs the information after the word institution and contry. Then it counts how many times it occours. 

	We apply this function to all partitions using map_partitions

		results = json_df.map_partitions(process_partition, meta={'institutions': object, 'countries': object})

	Then we count the occourens of each institution / country. (the null fields are dropped but they are a lot, my error or the dataset is a mess?)

	- Bar plot the results for top/bottom 20. 
	- Problem 1: China has like 3 different names. I need to unify them all under "China". Same for USA/UK
	- Problem 2: Many have a combination of countries instead of one. This may be due to the dataset. But it needs some clever refinition. 




