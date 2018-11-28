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
  traffic = read.csv('traffic.csv')

  Log('Loaded data:')
  print(traffic)

  by_url = aggregate(traffic$num_hits, by=list(url=traffic$url), FUN=sum)
  Log('Aggregated over URL:')
  print(by_url)

  total_hits = sum(traffic$num_hits)

  Log('Total traffic to /blog/ = %d', total_hits)

  summary = data.frame(url = by_url$url, percentage = by_url$x / total_hits * 100.0)
  Log('Percentage by URL:')
  print(summary)

  return()

  traffic = data.frame(
     date = as.Date(c('2018-11-30', '2018-11-30', '2018-12-01', '2018-12-01')),
     url = c('/releases.html', '/blog/', '/releases.html', '/blog/'),
     hits = c(42, 1000, 84, 2000)
  )
  print(traffic)
  cat('\n')

  # Filter rows of the data frame.
  blog = subset(traffic, url == '/blog/')
  print(blog)
  cat('\n')

  Log('Total traffic to /blog/ = %d', sum(blog$hits))
}

main(commandArgs(TRUE))
