# SS HPC Integration Scripts


# Index


#### 0.0 Introduction
#### 0.1 Requirements
#### 1.0 Installation
#### 1.1 Acquiring the BLASTEasy Sequencesever2.0 Virtual Machine
#### 1.1.1 Setting up the Data directory part 1
#### 1.2 Setting up the HPC
#### 1.2.1 Setting up the Data directory part 2
#### 1.3 Adjusting the database paths
#### 1.4 seqInit.py
#### 2.0 Running SequenceServer with the HPC
#### 3.0 Testing


# 0.0 Introduction


#### This set of scripts allows the user to run Sequenceserver BLAST searches
#### using an HPC machine. Our work is based off the BLASTEasy Sequenceserver2.0 
#### Atmosphere  Virtual Machine (VM).


## 0.1 Requirements


#### A - CyVerse account with access to atmosphere
#### B - Access to the University of Arizona HPC


# 1.0 Installation


## 1.1 Acquiring the BLASTEasy Sequencesever2.0 Virtual Machine


#### Log into atmo.cyverse.com and launch a new instance.
#### Choose the TeamBLASTEasy SeqServer 2.0b3 image, with small or medium size.
#### Launch the instance and remember the IP address.


## 1.1.1 Setting up the Data directory part 1


#### Move Data directory from /root/ to /home/<USER>
mv /Data ~/


## 1.2 Setting up the HPC


#### Log into the Arizona HPC with
ssh <username>@hpc.arizona.edu


#### In your home directory get CCTools
wget http://ccl.cse.nd.edu/software/files/cctools-7.0.21-x86_64-centos7.tar.gz
#### uzip
gunzip ./cctools-7.0.21-x86_64-centos7.tar.gz
#### untar
tar -xvf ./cctools-7.0.21-x86_64-centos7.tar


#### Get the HPC.pbs file by
wget https://github.com/Midterm-Team-Star/SS_HPC_Integration_Scripts/blob/master/HPC.pbs


#### Access the HPC.pbs file using a text editor.
#### Modify the #PBS according to preference (e.g. group, number of nodes, cpus, RAM, walltime)
#### Modify line 12 with YOUR path to home (e.g. /home/u12/yourname)
#### Modify line 15 YOUR path;
#### Modify line 15 with the IP of your MASTER VM.


#### Run the HPC.pbs by 
qsub HPC.pbs


## 1.2.1 Setting up the Data directory part 2
#### in your HPC home directory create a Data folder
mkdir ~/Data && chmod 755 Data


#### get the Data directory from the Atmosphere VM
sftp <CYVERSE_USERNAME>@<ATMOSPHERE_VM_IP>
get Data/ Data/


#### Now the database directory on the HPC should be set.


## 1.3 Adjusting the database paths


#### The Database paths on the MASTER and WORKER NEED to be the same.
#### In your Atmosphere VM create the same path by looking at where the Data folder is on the HPC.
mkdir /<U_NAME>/
cd ./<U_NAME>/
mkdir ./<HPC_USERNAME>
cd ./<HPC_USERNAME>
mv ~/Data ./


#### your Data folder location on the MASTER VM should look like this
/home/<U_NAME>/<HPC_USERNAME>/Data/


#### Now the Database folder is set


# 1.4 seqInit.py


#### seqInit.py is the initiation script that sequenceserver calls when started.
#### seqInit.py is located in
/var/lib/gems/2.5.0/gems/sequenceserver-2.0.0.beta3/lib/seqInit.py


#### In any directory download our seqInit.py script
wget https://github.com/Midterm-Team-Star/Midterm/blob/master/seqInit.py
mv ./seqInit.py /var/lib/gems/2.5.0/gems/sequenceserver-2.0.0.beta3/lib/


#### With a text editor modify the variables at line 98 and 100


#### The MASTER VM is now ready.


# 2.0 Running SequenceServer with the HPC


#### Assuming that HPC.pbs was already submitted, 
#### it should now be waiting for the MASTER VM.


#### On the MASTER VM simply type
sequenceserver -d /home/<U_NAME>/<HPC_USERNAME>/Data/


#### This will turn on Sequencesever and WorkQueue MASTER.
#### In your browser, go to your IP address, port 4567.
<IP address>:4567 #e.g (128.192.35.12:4567)


#### Sequenceserver should appear.
#### The queries you enter will be processed in the HPC.


# 3.0 Testing


#### In our github we have included a few test sequences:
#### a Real gene from mouse (~3kb)
#### a 50kb random query
#### a 200kb random query


#### these can be used to test your setup of Sequenceserver with the HPC.
#### Note: 200kb will take a much longer time of 50kb.
####Happy Blasting!
