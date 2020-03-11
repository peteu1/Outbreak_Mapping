setwd("C:/Users/peter/Documents/Python Scripts/Outbreak_Mapping")
dat = read.csv(file="./COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv", head=T, sep=",")
us = dat[dat[,2] == "US",]
usTot = colSums(us[,5:ncol(us)])
plot(usTot)