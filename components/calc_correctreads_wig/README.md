#calc_correctreads_wig : apply correction to the wig files based on the gc and mappability wigs.   

```
Development information

date created : May 12 2014
last update  : Sep 18  2014
Developer    : Diljot Grewal (dgrewal@bccrc.ca)
Input        : wig files for tumour, normal, gc and map
Output       : corrected wig file (input for TITAN)
Parameters   : sample id
Seed used    : correctReads.R
version: 1.1.5-0.1.2
```

###Dependencies

- R with TITANCNA package
- python

###Usage
The component calls the correctReadDepth function in TitanCNA 1.3.0
```
cnData <- correctReadDepth(tumWig, normWig, gc, map)
```

### ChangeLog
* 1.1.4-0.1.1: initial commit
* 1.1.4-0.1.2: added genome type 
* 1.1.5-0.1.2: added gitignore and test config
