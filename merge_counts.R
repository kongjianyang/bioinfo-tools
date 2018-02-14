#!/usr/bin/Rscript
# htseq-combine_all.R

# Take all htseq-count results and melt them in to one big dataframe
## do this for either tophat_all or tophat_gtf mappings.
tophat.all <- list.files(pattern = "_counts.txt",
    all.files = TRUE,
    recursive = FALSE,
    ignore.case = FALSE,
    include.dirs = FALSE)

# we choose the 'all' series
myfiles <- tophat.all
DT <- list()

# read each file as array element of DT and rename the last 2 cols
for (i in 1:length(myfiles) ) {
    DT[[myfiles[i]]] <- read.table(myfiles[i], header = F)
    cnts <- substr(myfiles[i], 1, nchar(myfiles[i])-29)
    cnts <- substr(cnts, 6, nchar(cnts))
    colnames(DT[[myfiles[i]]]) <- c("ID", cnts)
}

# merge all elements based on first ID columns
data <- DT[[myfiles[1]]]
for (i in 2:length(myfiles)) {
    y <- DT[[myfiles[i]]]
    z <- merge(data, y, by = c("ID"))
    data <- z
}

data <- data[-c(1:5),]
# final merged table

write.table(data,
    file = "counts_all.txt",
    quote = FALSE,
    row.names = FALSE,
    col.names = TRUE)
