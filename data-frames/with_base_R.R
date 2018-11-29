#!/usr/bin/Rscript
#
# example.R

options(stringsAsFactors = F)  # always use this in R

Log = function(fmt, ...) {
  cat('\n  ')
  cat(sprintf(fmt, ...))
  cat('\n')
}

main = function(argv) {
  traffic = read.csv('traffic.csv', colClasses=c("Date", "character", "numeric")) 

  Log('Loaded data:')
  print(traffic)

  daily = aggregate(traffic$num_hits, by=list(date=traffic$date), FUN=sum)
  Log('Daily traffic:')
  print(daily)

  total_hits = sum(traffic$num_hits)
  Log('Total hits = %d', total_hits)

  percentage = function(num_hits) {
    sum(num_hits) / total_hits * 100.0
  }
  popular = aggregate(traffic$num_hits, by=list(url=traffic$url), FUN=percentage)
  Log('Popular Pages:')
  print(popular)
}

main(commandArgs(TRUE))
