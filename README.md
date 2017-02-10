#readcounter : generate segment files from the titan output (IGV compatible)   

```
Development information

date created : May 12 2014
last update  : Sep 18  2014
Developer    : Diljot Grewal (dgrewal@bccrc.ca)
Input        : bam file
Output       : wig file
Parameters   : w,q
Seed used    : readCounter, filter_chromosomes.py
version: 1.1.6-1.0.0
```

###Dependencies
```
- python

```
###Known issues
The readCounter is an executable and it has only been tested on rocks/genesis. Doesn't work on mac.


###Last updates



### ChangeLog
* 1.1.3-1.0.0: initial commit
* 1.1.4-1.0.0: updated component_main.(chromosomes is now a list)
* 1.1.5-1.0.0: updated the chromosome param : default is nothing instead of 1-22,X,Y
* 1.1.6-1.0.0: added test config and gitignore

