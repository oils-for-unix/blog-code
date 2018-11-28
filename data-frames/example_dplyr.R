#!/usr/bin/Rscript
#
# example.R

library(dplyr)

options(stringsAsFactors = F)  # always use this in R

Log = function(fmt, ...) {
  cat(sprintf(fmt, ...))
  cat('\n')
}

main = function(argv) {
  traffic = data_frame(
     date = as.Date(c('2018-11-30', '2018-11-30', '2018-12-01', '2018-12-01')),
     url = c('/releases.html', '/blog/', '/releases.html', '/blog/'),
     hits = c(42, 1000, 84, 2000)
  )
  print(traffic)
  cat('\n')

  # Filter rows of the data frame.  dplyr uses a shell-like left-to-right
  # expression syntax.
  traffic %>% filter(url == '/blog/') -> blog
  print(blog)
  cat('\n')

  Log('Total traffic to /blog/ = %d', sum(blog$hits))
}

main(commandArgs(TRUE))
