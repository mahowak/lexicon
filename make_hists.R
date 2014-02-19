library(ggplot2)
library(plyr)


FOLDERID <- "~/Desktop/"
FOLDERKM <- "~/Dropbox/"


if (file.exists(FOLDERID)) {FOLDER <- FOLDERID} else {FOLDER<-FOLDERKM}

setwd(paste(FOLDER, "lexicon/", sep=""))

dat.files <- list.files('rfiles', full.names=TRUE) # read file names with full paths
lengths = seq(1, 10, 1)


makehist.global <- function(fn, v, title)
{d <- read.csv(fn)
 d$value <- d[ , v]
real <- d[d$lexicon == 'real', ]
 sims <- d[d$lexicon != 'real', ]
 z <- mean(sims$value) - 1.96*sd(sims$value)
  z2 <- mean(sims$value) + 1.96*sd(sims$value)
 p <- ggplot(sims, aes(value))
p <- p + geom_histogram(fill = '#336600') + xlab(v) + theme(legend.position = 'none')
p <- p + geom_point(data=real, aes(value, 0), size = 3, colour = 'red')   + ggtitle(fn) +
     geom_vline(xintercept =c(z, z2), linetype = 'longdash')
print(p)
}

makehist.ind <- function(fn, v, title, l)
{
    d <- read.csv(fn)
    d$length <- nchar(as.character(d$word))
    d <- d[d$length == l, ]
 d <-  aggregate(d[, v], by=list(d$lexicon), mean)
    names(d) <- c('lexicon', 'value')
real <- d[d$lexicon == 'real', ]
 sims <- d[d$lexicon != 'real', ]
 z <- mean(sims$value) - 1.96*sd(sims$value)
  z2 <- mean(sims$value) + 1.96*sd(sims$value)
 p <- ggplot(sims, aes(value))
p <- p + geom_histogram(fill = '#336600') + xlab(v) + theme(legend.position = 'none')
p <- p + geom_point(data=real, aes(value, 0), size = 3, colour = 'red')   + ggtitle(paste(l, fn)) +
     geom_vline(xintercept =c(z, z2), linetype = 'longdash')
print(p)
}


for (f in dat.files)
    {

if (grepl('global', f))
    {
    	pdf(paste("PDFs/", substr(f, 8, nchar(f)), ".pdf", sep=""))
    	makehist.global(f, 'neighbors', f)
    	dev.off()
    	#d <- read.csv(f)
    	# print(f)
    	# real <- d[d$lexicon == 'real', ]
 		# sims <- d[d$lexicon != 'real', ]
    	# print(mean(real$homophones_type))
    	# print(mean(real$homophones_token))
    	}
if (grepl('indwords', f))
	{
		
	   	pdf(paste("PDFs/", substr(f, 8, nchar(f)), ".pdf", sep=""))
		for (l in lengths)
    	{makehist.ind(f, 'neighbors', f, l)}
    	dev.off()
}

}
