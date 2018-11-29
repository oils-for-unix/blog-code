#!/usr/bin/Rscript
#
# with_dplyr.R

library(dplyr)

options(stringsAsFactors = F)  # always use this in R

Log = function(fmt, ...) {
  cat('\n  ')
  cat(sprintf(fmt, ...))
  cat('\n')
}

main = function(argv) {
  Log('----')

  traffic = read.csv('traffic.csv', colClasses=c("Date", "character", "numeric")) 
  Log('Loaded data:')
  print(traffic)

  traffic %>%
    group_by(date) %>%
    summarize(num_hits = sum(num_hits)) ->
    daily  # assign to 'daily'
  Log('Daily traffic:')
  print(daily)

  total_hits = sum(traffic$num_hits)
  Log('Total hits = %d', total_hits)

  traffic %>%
    group_by(url) %>%
    summarize(percentage = sum(num_hits) / total_hits * 100.0) %>%
    arrange(desc(percentage)) ->
    popular
  Log('Popular Pages:')
  print(popular)
}

main(commandArgs(TRUE))
