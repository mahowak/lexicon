library(ggplot2)
library(plyr)


FOLDERID <- "~/Desktop/"
FOLDERKM <- "~/Dropbox/"


if (file.exists(FOLDERID)) {FOLDER <- FOLDERID} else {FOLDER<-FOLDERKM}
setwd(paste(FOLDER, "lexicon/", sep=""))

StdErr <- function (x) { return (sd(x)/sqrt(length(x))); }


multmerge <- function(mypath)
{
filenames=list.files(path=mypath, full.names=TRUE)
datalist = lapply(filenames, function(x){read.csv(file=x,header=T)})
Reduce(function(x,y) {rbind(x,y)}, datalist)
}


all <- multmerge('evaluation')


data <- ddply(all, .(model, smoothing), summarize, perplexity = mean(ppl), SE= StdErr(ppl))

pdf("PDFs/evaluation.pdf")
p<-ggplot(subset(data, smoothing == "srilm_add"), aes(x = model, y= perplexity, colour = model, group= model)) +  geom_point() + geom_errorbar(aes(ymin=perplexity-SE, ymax=perplexity+SE), width=.1) + ylab("ppl")+ xlab("models")+ggtitle("evaluation")
print(p)
dev.off()

