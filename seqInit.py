#!/usr/bin/env python

import os
import sys
import glob
import time
import work_queue as wq


opt = sys.argv
pid = opt[1]
port = int(opt[2])
wdir = opt[3]

## Read CMD file ##
def readCMD(file):
    froot = file.split('.')[0]

    f = open(file, 'r')
    cmd = f.read()
    f.close()

    return cmd.rstrip('\n')+' > '+froot+'.out'
##

## Delete CMD file ##
def removeCMD(file):
    os.remove(file)
##

## Parse CMD ##
def parseCMD(cmd): 
    cDict = {'sqCMD': {}, 'wqCMD': {}, 'wqIO': {}}
    opt = cmd.split()

    cDict['BLAST'] = opt[0]

    didx = opt.index('-db')+1
    qidx = opt.index('-query')

    cDict['wqCMD']['-db'] = ' '.join([x for x in opt[didx:qidx]])
    cDict['sqCMD']['SEQ'] = opt[qidx+1].strip("'")
    cDict['wqCMD']['-query'] = "'"+opt[qidx+1].split('/')[-1]
    infile=cDict['wqCMD']['-query']
    # oidx = opt.index('-outfmt')+1
    # cDict['wqCMD']['-outfmt'] = opt[oidx]

    tidx = opt.index('-num_threads')

    c1Opts = ''
    if qidx+2 != tidx:
        c1Opts = ' '.join(opt[qidx+2:tidx])

    cDict['wqCMD']['-num_threads'] = opt[tidx+1]

    ridx = opt.index('>')

    c2Opts = ''
    if tidx+2 != ridx:
        c2OPts = ' '.join(opt[tidx+2:ridx])

    cDict['sqCMD']['REP'] = opt[ridx+1]
    cDict['wqIO']['>'] = opt[ridx+1].split('/')[-1]

    # lidx = opt.index('2>')+1
    # cDict['sqCMD']['LOG'] = opt[lidx]
    # cDict['wqIO']['2>'] = opt[lidx].split('/')[-1]

    cDict['CMD'] = './'+cDict['BLAST']+' '+ \
                   ' '.join([k+' '+cDict['wqCMD'][k] \
                   for k in cDict['wqCMD'].keys()])+' '+ \
                   c1Opts+c2Opts+' '+' '.join([k+' '+cDict['wqIO'][k] \
                   for k in cDict['wqIO'].keys()])
    print(cDict)
    print("-"*100)
    return cDict
##


q = wq.WorkQueue(port)

while True:
    ts = q.wait(1)
    # ts = q.wait(wq.WORK_QUEUE_WAITFORTASK)

    time.sleep(2)

    seq = os.path.isdir('/proc/'+str(pid))
    if not seq:
        sys.exit()

    nfiles = glob.glob(wdir+'/*.cmd')

    for file in nfiles:
        command = readCMD(file)
        removeCMD(file)
        cmDict = parseCMD(command)
        cmDict['wqCMD']['-db'] = "'/home/<U_NUMBER>/<HPC_USERNAME>/Data/mouse.1.protein.faa'"
	#	cmDict['sqCMD']['SEQ'] = str(cmDict['sqCMD']['SEQ']).replace('/home/cosimichele/','/home/u12/cosi/')
	cmDict['CMD'] = cmDict['CMD'].replace("'/home/<username>/Data/mouse.1.protein.faa'","'/home/<U_NUMBER>/<HPC_USERNAME>/Data/mouse.1.protein.faa'") 
        print(cmDict)
        t = wq.Task(cmDict['CMD'])

        t.specify_cores(int(cmDict['wqCMD']['-num_threads']))
        t.specify_algorithm(wq.WORK_QUEUE_SCHEDULE_FILES)
        # t.specify_memory(mem)

        t.specify_file('/usr/local/bin/'+cmDict['BLAST'], cmDict['BLAST'], \
                       wq.WORK_QUEUE_INPUT, cache=True)
        t.specify_file(cmDict['sqCMD']['SEQ'], cmDict['wqCMD']['-query'].strip("'"), \
                       wq.WORK_QUEUE_INPUT, cache=True)

        t.specify_file(cmDict['sqCMD']['REP'], cmDict['wqIO']['>'], \
                       wq.WORK_QUEUE_OUTPUT, cache=True)
        # t.specify_file(cmDict['sqCMD']['LOG'], cmDict['wqIO']['2>'], \
        #                wq.WORK_QUEUE_OUTPUT, cache=False)
        
        tid = q.submit(t)
