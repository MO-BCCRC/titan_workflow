args <- commandArgs(TRUE)

version <- "0.1.3"

library(TitanCNA)
obj_file <- args[1]
outdir <- args[2]
numClusters <- args[3]
id <- args[4]
rid <- args[5]
chr <- args[6]
chr <- eval(parse(text=chr))
ploidy <- args[7]

# load a workspace into the current session
load(obj_file)

#### PLOT RESULTS ####
finoutdir <- paste(outdir,"/",id,"_",rid,"_cluster_",numClusters,"_ploidy_",ploidy,"/",sep="")

dir.create(finoutdir, recursive=TRUE)
library(SNPchip)  ## use this library to plot chromosome idiogram (optional)
norm <- tail(convergeParams$n,1) #convergeParams$n[length(convergeParams$n)]
ploidy <- tail(convergeParams$phi,1) #convergeParams$phi[length(convergeParams$phi)]
for (i in chr){
    outplot <- paste(finoutdir,id,"_",rid,"_cluster_",numClusters,"_chr",i,".png",sep="")
    png(outplot,width=1200,height=1000,res=100,type="cairo")
    
    # if 2 or fewer clusters, use c(4,1) panels
    if (as.numeric(numClusters) <= 2){
		par(mfrow=c(4,1))
	}else{
		par(mfrow=c(3,1))  
	}
    
    ## PLOT LOG RATIO (CNA) ##
    tryCatch({
    plotCNlogRByChr(results, i, ploidy=ploidy, geneAnnot=NULL, spacing=4, 
    				ylim=c(-4,6), cex=0.5, main=paste("Chr ",i,sep=""), xlab="")
    },
    error=function(err){
    print(paste('Warning: plotCNlogRByChr skipped for chromosome ', i, 'due to ', err))
    #print(err)
    })

    ## PLOT ALLELIC RATIOS (LOH) ##
    tryCatch({
    plotAllelicRatio(results, i, geneAnnot=NULL, spacing=4, 
    				ylim=c(0,1), cex=0.5, main=paste("Chr ",i,sep=""), xlab="")
    },
    error=function(err){
    print(paste('Warning: plotAllelicRatio skipped for chromosome ', i, 'due to ', err))
    #print(err)
    })

    ## PLOT CELLULAR PREVALENCE AND CLONAL CLUSTERS ##
    tryCatch({
    plotClonalFrequency(results, i, normal=norm, geneAnnot=NULL, spacing=4,
                    ylim=c(0,1), cex=0.5, main=paste("Chr ",i,sep=""), xlab="")
    },
    error=function(err){
    print(paste('Warning: plotClonalFrequency skipped for chromosome ', i, 'due to ', err))
    #print(err)
    })


    if (as.numeric(numClusters) <= 2){ 
        tryCatch({
        plotSubcloneProfiles(results, i, cex = 2, spacing=6, main=paste("Chr ",i,sep=""))
        },
        error=function(err){
        print(paste('Warning: plotSubcloneProfiles skipped for chromosome ', i, 'due to ', err))
        #print(err)
        })
    }


    ## PLOT SUBCLONE PROFILE FOR 2 OR FEWER CLONAL CLUSTER RUNS ##
    tryCatch({
    if (as.numeric(numClusters) <= 2){
		#plotSubcloneProfiles(results, i, cex = 2, spacing=6, main=paste("Chr ",i,sep=""))
		pI <- plotIdiogram(i,build="hg19",unit="bp",label.y=-4.25,new=FALSE,ylim=c(-2,-1))
	}else{
		pI <- plotIdiogram(i,build="hg19",unit="bp",label.y=-0.35,new=FALSE,ylim=c(-0.2,-0.1))
	}
	
    },
    error=function(err){
    print(paste('Warning: plotIdiogram skipped for chromosome ', i, 'due to ', err))
    #print(err)
    })

    dev.off()
}
