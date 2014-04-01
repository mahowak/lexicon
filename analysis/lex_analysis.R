library(ggplot2)
library(reshape)
library(lme4.0)
library(dplyr)

setwd("/Users/km/Dropbox/lexicon/analysis")

dat <- list.files('../rfiles/all_runs')
dat <- dat[grep('^global', dat)]
d <- NULL
for (i in dat) {
    df <- read.csv(paste('../rfiles/all_runs/', i, sep=''))
    df$f <- i
    d <- rbind(d, df)
            }

d$f <- gsub('_syll_', '', d$f)
d$f <- gsub('_pcfg_', '', d$f)
d$f <- gsub('_smoothing0.01', '', d$f)
d$f <- gsub('manual_', '', d$f)
d$f <- gsub('\\.txt', '', d$f)

d <- cbind(d, colsplit(d$f, split='_', names = c('global', 'lex', 'lemma', 'lang', 'mono', 'homo1', 'homo2', 'size', 'cv', 'iter', 'model', 'n')))

d$model.n <- paste(d$model, d$n, sep='_')
makehist.global <- function(d, v, title)
{
 d$value <- d[ , v]
real <- d[d$lexicon == 'real', ]
 sims <- d[d$lexicon != 'real', ]
 z <- mean(sims$value) - 1.96*sd(sims$value)
  z2 <- mean(sims$value) + 1.96*sd(sims$value)
 p <- ggplot(sims, aes(value, fill=as.factor(model.n)))
p <- p + geom_histogram(position ='identity', alpha=.3) + xlab(v) + theme(legend.position = 'right')
p <- p + geom_point(data=real, aes(value, 0), size = 3, colour = 'red')   + ggtitle(title) + facet_grid(lang ~ .) #+     geom_vline(xintercept =c(z, z2), linetype = 'longdash')
print(p)
}

pdf('global_pdfs.pdf')
for (j in c('mps', 'neighbors', 'avg_lev', 'avg_cluster', 'transitivity', 'bppair', 'tdpair', 'kgpair', 'X1entropy', 'X2entropy' ,'X3entropy', 'X4entropy', 'X5entropy', 'pctunique1', 'pctunique2', 'pctunique3', 'pctunique4', 'pctunique5')) {
makehist.global(d, j, j)}
dev.off()
