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

  total_hits = sum(traffic$num_hits)
  Log('Total traffic to /blog/ = %d', total_hits)

  traffic %>%
    group_by(date) %>%
    summarize(num_hits = sum(num_hits)) ->
    daily
  Log('Daily traffic:')
  print(daily)

  traffic %>%
    group_by(url) %>%
    summarize(percentage = sum(num_hits) / total_hits * 100.0) %>%
    arrange(desc(percentage)) ->
    popular # assigned to variable summary

  Log('Popular Pages:')
  print(popular)
}

main(commandArgs(TRUE))
