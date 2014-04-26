library(reshape)
library(dplyr)
library(ggplot2)
library(plotrix)

setwd("/Users/km/Dropbox/lexicon/wiki")

a <- list.files()
a <- a[grep('txt$', a)]
a <-  cbind(a, colsplit(a, split="[_.]", names= c('a', 'b', 'c'))[2])

d <- NULL
for (i in 1:nrow(a))
    {
        newd <- read.csv(as.character(a[i, 1]), sep='\t')
        newd$lang <- a[i, 2]
        d <- rbind(d, newd)
    }


write.csv(d, file='all_lexicon.csv', row.names=F)

#d <- read.csv('all_lexicon.csv')

d <- d[d$length > 2 & d$length < 8, ]
d <- d[d$lang != 'simple', ]
d <- group_by(d, lang, length)

cor.test.p <- function(x, y) {return(as.numeric(cor.test(x, y, method='spearman')[3]))}

d$lc <- log(d$count)
d.sum <- summarise(d, cor.n.f = cor(lc, neighbors, method='spearman'),
                   cor.mp.f = cor(lc, mps, method='spearman'),
                   cor.prob.f = cor(lc, prob, method='spearman'),
                   cor.prob.n = cor(prob, neighbors, method='spearman'),
                   cor.prob.mp = cor(prob, mps, method='spearman'),
                   cor.n.f.p = cor.test.p(lc, neighbors),
                   cor.mp.f.p = cor.test.p(lc, mps),
                   cor.prob.f.p = cor.test.p(lc, prob),
                   cor.prob.n.p = cor.test.p(prob, neighbors),
                   cor.prob.mp.p = cor.test.p(prob, mps))

d.se <- summarise(d, cor.f.s1 = cor(s1, lc, method='spearman'),
                   cor.f.s2 = cor(s2, lc, method='spearman'),
                   cor.f.s3 = cor(s3, lc, method='spearman'),
                   cor.f.s4 = cor(s4, lc, method='spearman'),
                   cor.f.s5 = cor(s5, lc, method='spearman'),
                  cor.f.e1 = cor(e1, lc, method='spearman'),
                  cor.f.e2 = cor(e2, lc, method='spearman'),
                  cor.f.e3 = cor(e3, lc, method='spearman'),
                  cor.f.e4 = cor(e4, lc, method='spearman'),
                  cor.f.e5 = cor(e5, lc, method='spearman')
                  )

d <- mutate(d,   f.z = scale(lc),
                   mp.z = scale(mps),
                   n.z = scale(neighbors),
                   prob.z = scale(prob))


wikilang <- read.csv('wikilang.csv')
d.sum <- merge(d.sum, wikilang, by = c('lang'), all.x=T)
unique(d.sum[is.na(d.sum$wikilang), ]$lang )

pdf('corplots.pdf')
for (i in c('cor.n.f', 'cor.mp.f', 'cor.prob.f', 'cor.prob.n', 'cor.prob.mp')) {
    d.sum$v <- d.sum[ , i]
    print(ggplot(d.sum, aes(x=v))   + xlim(-1, 1) + geom_histogram() + ggtitle(i) + geom_vline(xintercept=0, colour='red') + facet_grid(length ~ .))
}

dev.off()


pdf('corplots_point.pdf')
for (i in c('cor.n.f', 'cor.mp.f', 'cor.prob.f', 'cor.prob.n', 'cor.prob.mp')) {
    d.sum$v <- d.sum[ , i]
    #d.sum$lang <- factor(d.sum$lang, labels=arrange(d.sum[d.sum$length == 4, ], v)$lang)
    print(ggplot(d.sum, aes(x=lang, y=v, label=lang, colour=as.factor(Script)))   + geom_text(aes(size=Size/4)) + ggtitle(i) + geom_hline(yintercept=0, colour='red') + facet_grid(length ~ .) )
}

dev.off()



pdf('corplots_box.pdf')
for (i in c('cor.n.f', 'cor.mp.f', 'cor.prob.f', 'cor.prob.n', 'cor.prob.mp')) {
    d.sum$v <- d.sum[ , i]
    d.sum$lang <- factor(d.sum$lang, labels=arrange(d.sum[d.sum$length == 4, ], v)$lang)
    print(ggplot(d.sum, aes(x=as.factor(Size), y=v))   + geom_violin() + ggtitle(i)  + facet_grid(length ~ .))
}

dev.off()


summary(d.sum)
unique(d.sum[ d.sum$cor.prob.f > .4, ])

unique(d.sum[ d.sum$cor.prob.f < .05, ])
unique(d.sum[ d.sum$cor.prob.n < .05, ])
unique(d.sum[ d.sum$cor.n.f < .05, ])

table(d[d$lang == 'en', ]$length)
table(d[d$lang == 'zh', ]$length)
table(d[d$lang == 'ja', ]$length)

pdf('big_cor.pdf')

print(ggplot(d[d$length == 4, ], aes(x=prob.z, f.z)) + geom_point(alpha=.002) + geom_smooth(method=lm) + facet_wrap(~lang, ncol=10) + geom_hline(yintercept=0, alpha=.2) + xlim(-5, 5) +  ylim(-5, 5) + ggtitle('prob vs freq'))
print(ggplot(d[d$length == 4, ], aes(x=n.z, f.z)) + geom_point(alpha=.002) + geom_smooth(method=lm) + facet_wrap(~lang, ncol=10) + geom_hline(yintercept=0, alpha=.2) + xlim(-5, 5) + ylim(-5, 5) +  ggtitle('neighbors vs freq'))
dev.off()

library(hexbin)
pdf('~/Dropbox/writeup/PDFs/big_cor2_probvfreq.pdf')

print(ggplot(d[d$length == 4, ], aes(x=prob.z, f.z)) + geom_hex(aes(fill=..density..*100), na.rm=T, alpha=.66, binwidth=c(.5, .5)) + scale_fill_continuous(limits=c(1, 12), na.value='white') + facet_wrap(~lang, ncol=10) + geom_hline(yintercept=0, alpha=.2) + xlim(-3, 3) +  ylim(-3, 3) + ggtitle('prob vs freq') + geom_smooth(method=lm, colour='red'))

dev.off()

pdf('~/Dropbox/writeup/PDFs/big_cor2_neighborsvsfreq.pdf')
print(ggplot(d[d$length == 4, ], aes(x=n.z, f.z)) + geom_hex(aes(fill=..density..*100), na.rm=T, alpha=.66, binwidth=c(.5, .5)) + scale_fill_continuous(limits=c(1, 12), na.value='white') + facet_wrap(~lang, ncol=10) + geom_hline(yintercept=0, alpha=.2) + xlim(-3, 3) +  ylim(-3, 3) + ggtitle('neighborhood density vs freq') + geom_smooth(method=lm, colour='red'))

dev.off()

eng <- d[d$lang == 'en' & d$length == 5, ]



d.sum.melt <- melt(d.sum, id.vars= c('lang', 'length'))
d.sum.sum <- group_by(d.sum.melt, length, variable)
d.sum.sum <- summarise(d.sum.sum, m=mean(value), lower = mean(value) - 1.96*std.error(value), upper = mean(value) + 1.96 *std.error(value), under0= sum(value < 0), under.1 = sum(value < .1), notsig=sum(value > .05))
print(d.sum.sum, digits=2)

pdf('~/Dropbox/lexicon/writeup/PDFs/summary_of_stats.pdf')
ggplot(d.sum.sum[grepl('\\.p$', d.sum.sum$variable) == F, ], aes(x=variable, y=m)) + geom_bar(aes(colour=variable, fill=variable)) + facet_grid(length ~ .) + geom_errorbar(aes(ymin=lower, ymax=upper, width=.4)) + ylim(0, 1) + ylab('correlation')
dev.off()

d.sum.melt$length <- paste(as.character(d.sum.melt$length), ' letters')
pdf('~/Dropbox/lexicon/writeup/PDFs/violins_of_stats.pdf')
ggplot(d.sum.melt[grepl('\\.p$', d.sum.melt$variable) == F, ], aes(x=variable, y=value, fill=variable)) + geom_boxplot() + facet_grid(. ~ length) + ylim(-1, 1) + geom_hline(yintercept=0, colour='red') +  ylab('correlation')
dev.off()

d.sum.melt$length <- paste(as.character(d.sum.melt$length), ' letters')
pdf('~/Dropbox/lexicon/writeup/PDFs/many_hists.pdf')
ggplot(d.sum.melt[grepl('\\.p$', d.sum.melt$variable) == F, ], aes(x=variable, y=value, fill=variable)) + geom_violin() + facet_grid(. ~ length) + ylim(-1, 1) + geom_hline(yintercept=0, colour='red') +  ylab('correlation')
dev.off()


d.sum.sum$variable <- as.character(d.sum.sum$variable)
d.sum.sum$length <- as.factor(d.sum.sum$length)
x <- d.sum.sum[grepl('\\.p$', d.sum.sum$variable) == T, c('length', 'variable', 'notsig') ]
x$length <-  paste(as.character(x$length), ' letters')
for.table <- cast(x, variable ~ length, value='notsig')
sink('~/Dropbox/lexicon/writeup/PDFs/table_of_not_sig.txt')
xtable(for.table)
sink()
