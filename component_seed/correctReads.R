library(TitanCNA)
version <- "0.1.1"
args <- commandArgs(TRUE)

tumWig <- args[1]
normWig <- args[2]
gc <- args[3]
map <- args[4]
target_list <- args[5]
outfile <- args[6]

message('titan: Correcting GC content and mappability biases...')

if( is.null(target_list) ){
    cnData <- correctReadDepth(tumWig, normWig, gc, map, targetedSequence = target_list)
} else {
    cnData <- correctReadDepth(tumWig, normWig, gc, map)
}

write.table(cnData, file = outfile, col.names = TRUE, row.names = FALSE, quote = FALSE, sep ="\t")
