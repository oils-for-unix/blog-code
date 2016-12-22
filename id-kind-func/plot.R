#!/usr/bin/Rscript
#
# plot.R

library(data.table)
library(ggplot2)

main = function(argv) {
  x=0:255
  for (n in c(0, 23)) {
    png(sprintf("bit-%d.png", n))
    plot(sort(bitwAnd(x, -x-n)))
    dev.off()
  }
}

main(commandArgs(TRUE))
