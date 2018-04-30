cat header.csv > random.csv
find . -name "project.js" | xargs cat | jq --raw-output '"\(.name),\(.stats.CoveredBranches),\(.stats.CoveredStatements),\(.stats.CoveredMethods),\(.stats.TotalPercentageCovered),\(.stats.LineCount),\(.stats.NcLineCount),\(.stats.TotalFiles),\(.stats.TotalMethods),\(.stats.TotalClasses)"' >> random.csv
