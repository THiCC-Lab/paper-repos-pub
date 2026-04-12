# Author: Deja Workman @ Penn State
# Date: 4/12/2026
# Description: This is code for the paper "The STRONG-R and the Carceral Algorithmic Constitution of Anti-Blackness".

# Set Working Directory
#setwd("C://Users//Student//Desktop//Carceral Algorithms")
setwd("C://Users//dqw5409//Desktop//STRONG-R")

# Upload data
# Data from Bureau of Justice Statistics that was downloaded as SPSS data/SAV file
library(haven)
library(data.table)
data <- read_sav("37692-0001-Data.sav")

# Clean the data according to race
# Create new collapsed race column as Black/White/Both/Other Only, omit remaining
data[, 'Collapsed_Race'] = NA
data$Collapsed_Race[data$V0016==1 & data$V0017==2] <- "White"
data$Collapsed_Race[data$V0016==2 & data$V0017==1] <- "Black"
data$Collapsed_Race[data$V0016==1 & data$V0017==1] <- "BothBW"
data$Collapsed_Race[data$V0016==2 & data$V0017==2] <- "NBNW"
data <- data[complete.cases(data[,c("Collapsed_Race")]),]

# Check population race via chart
race_labels <- c("Black","BothBW","NBNW","White")
pie_labels <- round(100*table(data$Collapsed_Race)/sum(table(data$Collapsed_Race)), 1)
pie(table(data$Collapsed_Race), cex =1.5,labels = paste(pie_labels,"%", race_labels), col = c("red", "green", "blue", "purple"))
legend(1,1,c("Black", "BothBW", "NBNW", "White"), fill = c("red", "green", "blue", "purple"), cex=0.75)
#barplot(table(data$Collapsed_Race), ylim=c(0,12000), col=c("red","purple","blue","green"))

# Age at First Conviction - Subdataset
ageConviction <- subset(data, select = c(Collapsed_Race, V0899))
ageConviction <- subset(ageConviction, V0899 > 0)

# Age at First Conviction - Box and Whiskers
boxplot(V0899~Collapsed_Race, data = ageConviction, xaxt="n", xlab="Categorical Race", ylab="Age at First Arrest")
axis(side=1,at=c(1:4),labels=c("Black","Black & White","Not Black or White", "White"))
abline(h=24, col="red")

# Age at First Conviction - Avg Stats
afcBlack <- mean(ageConviction$V0899[ageConviction$Collapsed_Race=="Black"])
afcWhite <- mean(ageConviction$V0899[ageConviction$Collapsed_Race=="White"])
afcBoth <- mean(ageConviction$V0899[ageConviction$Collapsed_Race=="BothBW"])
afcNBNW <- mean(ageConviction$V0899[ageConviction$Collapsed_Race=="NBNW"])

# Age at First Conviction - Median Stats
afcmedBlack <- median(ageConviction$V0899[ageConviction$Collapsed_Race=="Black"])
afcmedWhite <- median(ageConviction$V0899[ageConviction$Collapsed_Race=="White"])
afcmedBoth <- median(ageConviction$V0899[ageConviction$Collapsed_Race=="BothBW"])
afcmedNBNW <- median(ageConviction$V0899[ageConviction$Collapsed_Race=="NBNW"])

# Age at First Conviction - ANOVA
library(dplyr)
afc_anova <- aov(ageConviction$V0899~ageConviction$Collapsed_Race)
summary(afc_anova)

# Number of Times Arrested - Subdataset
timesArrested <- subset(data, select = c(Collapsed_Race, V0899, RV0014))
timesArrested <- subset(timesArrested, V0899 > 0 & RV0014 > -1 & RV0014 < 101)

whitetimesArrested <- subset(timesArrested, select = c(Collapsed_Race, V0899, RV0014))
whitetimesArrested <- subset(whitetimesArrested, Collapsed_Race == "White")

blacktimesArrested <- subset(timesArrested, select = c(Collapsed_Race, V0899, RV0014))
blacktimesArrested <- subset(blacktimesArrested, Collapsed_Race == "Black")

# Number of Times Arrested - Scatter Plot
plot(timesArrested$V0899[timesArrested$Collapsed_Race=="White"],timesArrested$RV0014[timesArrested$Collapsed_Race=="White"], col="purple")
points(timesArrested$V0899[timesArrested$Collapsed_Race=="Black"],timesArrested$RV0014[timesArrested$Collapsed_Race=="Black"], col="red")
abline(lm(RV0014~V0899,data=whitetimesArrested), col="purple")
abline(lm(RV0014~V0899,data=blacktimesArrested), col="red")

# Highest Level of Education - Subdataset
highestEd <- subset(data, select = c(Collapsed_Race, V0935))
highestEd <- subset(highestEd, V0935>0 & V0935<30)

# Highest Level of Education - Populate new column of categorical information
highestEd[,"Category"] = NA
highestEd$Category[highestEd$V0935>0 & highestEd$V0935<6] <- "Elementary"
highestEd$Category[highestEd$V0935>5 & highestEd$V0935<9] <- "Middle"
highestEd$Category[highestEd$V0935>8 & highestEd$V0935<13] <- "High"
highestEd$Category[highestEd$V0935>12 & highestEd$V0935<17] <- "College"
highestEd$Category[highestEd$V0935>16 & highestEd$V0935<19] <- "Graduate"

# Highest Level of Education - Individual Barplots
barplot(table(highestEd$V0935[highestEd$Collapsed_Race=="Black"]), ylim=c(0,3000), main = "Years of Education (Black)")
barplot(table(highestEd$V0935[highestEd$Collapsed_Race=="White"]), ylim=c(0,3000), main = "Years of Education (White)")
barplot(table(highestEd$V0935[highestEd$Collapsed_Race=="BothBW"]), ylim=c(0,3000), main = "Years of Education (Both Black & White)")
barplot(table(highestEd$V0935[highestEd$Collapsed_Race=="NBNW"]), ylim=c(0,3000), main = "Years of Education (Not Black or White)")

# Highest Level of Education - ChiSquare
highestEd_chisq <- chisq.test(table(highestEd$Collapsed_Race,highestEd$Category))
print(highestEd_chisq)

# Highest Level of Education - Percentage Function + Table
edPercent <- function(race,category){
  tempdf <- highestEd[highestEd$Collapsed_Race==race,]
  total <- nrow(tempdf)
  tempdf <- tempdf[tempdf$Category==category,]
  subtotal <- nrow(tempdf)
  return(round((subtotal/total)*100,2))
}

highestEd_ptable <- matrix(c(edPercent("Black","Elementary"),edPercent("White","Elementary"),
                             edPercent("BothBW","Elementary"),edPercent("NBNW","Elementary"),
                             edPercent("Black","Middle"),edPercent("White","Middle"),
                             edPercent("BothBW","Middle"),edPercent("NBNW","Middle"),
                             edPercent("Black","High"),edPercent("White","High"),
                             edPercent("BothBW","High"),edPercent("NBNW","High"),
                             edPercent("Black","College"),edPercent("White","College"),
                             edPercent("BothBW","College"),edPercent("NBNW","College"),
                             edPercent("Black","Graduate"),edPercent("White","Graduate"),
                             edPercent("BothBW","Graduate"),edPercent("NBNW","Graduate")), ncol=5)

rownames(highestEd_ptable) <- c("Black","White","BothBW","NBNW")
colnames(highestEd_ptable) <- c("Elementary", "Middle", "High", "College", "Graduate")
highestEd_ptable <- as.table(highestEd_ptable)
print(highestEd_ptable)

# Highest Level of Education - Grouped Percentage Barplot
barplot(height = highestEd_ptable, beside=TRUE, ylim=c(0,100), col=c("red", "blue", "green", "purple"))
legend(18,70,rownames(highestEd_ptable),fill = c("red", "purple", "blue", "green"),cex=0.75)

# Income - Subdataset
income <- subset(data, select = c(Collapsed_Race, V1145))
income <- subset(income, V1145>0)

# Income - Black vs White Income according to Census data
library(readxl)
black_income <- as.data.frame(read_excel("Census Median Incomes.xlsx", sheet="Black"))
white_income <- as.data.frame(read_excel("Census Median Incomes.xlsx", sheet="White"))
rownames(black_income) <- "Median Income"
rownames(white_income) <- "Median Income"

plot(c(2016,2017,2018,2019,2021,2022,2023,2024),
     c(sum(black_income$"2016"),sum(black_income$"2017"),sum(black_income$"2018"),sum(black_income$"2019"),
       sum(black_income$"2021"),sum(black_income$"2022"),sum(black_income$"2023"),sum(black_income$"2024")),
     type = "o", yaxt="n",col="red",ylim=c(0,100000),ylab="Median Income",xlab="Year")
axis(side=2,at=c(10000,20000,30000,40000,50000,60000,70000,80000,90000,100000),
     labels=c(10000,20000,30000,40000,50000,60000,70000,80000,90000,100000))
lines(c(2016,2017,2018,2019,2021,2022,2023,2024),
     c(sum(white_income$"2016"),sum(white_income$"2017"),sum(white_income$"2018"),sum(white_income$"2019"),
       sum(white_income$"2021"),sum(white_income$"2022"),sum(white_income$"2023"),sum(white_income$"2024")),
     type="o", pch=2,col="purple")
lines(c(2016,2016),c(black_income$"2016",white_income$"2016"), col="grey")
lines(c(2024,2024),c(black_income$"2024",white_income$"2024"), col="grey")
text(2016.5,50000,label=paste("$",toString(sum(white_income$`2016`)-sum(black_income$`2016`)),sep=""))
text(2023.5,70000,label=paste("$",toString(sum(white_income$`2024`)-sum(black_income$`2024`)),sep=""))
legend(2016,100000,c("Black", "White"),fill = c("red", "purple"),cex=0.75)

#Income - ANOVA
income_anova <- aov(income$V1145~income$Collapsed_Race)
summary(income_anova)


# Income - Grouped Sum Barplot
barplot(table(income$Collapsed_Race,income$V1145), names.arg=c("<$200","$200-599","$600-$999","$1000-$1999","$2000-$4999",">$5000"),
        col=c("red","blue","green","purple"),xlab="Income",beside=TRUE)
legend(1,80,rownames(table(income$Collapsed_Race,income$V1145)),fill=c("red", "blue", "green", "purple"),cex=0.75)

# Income - Percentage Function + Table
incomePercent <- function(race,category){
  tempdf <- income[income$Collapsed_Race==race,]
  total <- nrow(tempdf)
  tempdf <- tempdf[tempdf$V1145==category,]
  subtotal <- nrow(tempdf)
  return(round((subtotal/total)*100,2))
}

income_ptable <- matrix(c(incomePercent("Black",1),incomePercent("White",1),
                          incomePercent("BothBW",1),incomePercent("NBNW",1),
                          incomePercent("Black",2),incomePercent("White",2),
                          incomePercent("BothBW",2),incomePercent("NBNW",2),
                          incomePercent("Black",3),incomePercent("White",3),
                          incomePercent("BothBW",3),incomePercent("NBNW",3),
                          incomePercent("Black",4),incomePercent("White",4),
                          incomePercent("BothBW",4),incomePercent("NBNW",4),
                          incomePercent("Black",5),incomePercent("White",5),
                          incomePercent("BothBW",5),incomePercent("NBNW",5), 
                          incomePercent("Black",6),incomePercent("White",6),
                          incomePercent("BothBW",6),incomePercent("NBNW",6)),ncol=6)

rownames(income_ptable) <- c("Black","White","BothBW","NBNW")
colnames(income_ptable) <- c("<$200", "$200-$599", "$600-$999", "$1000-$1999", "$2000-$4999", ">$5000")
income_ptable <- as.table(income_ptable)
print(income_ptable)

# Income - Grouped Percentage Barplot
barplot(height = income_ptable, beside=TRUE, col=c("red", "purple", "green", "blue"))
legend(1,25,rownames(income_ptable),fill = c("red", "purple", "green", "blue"),cex=0.75)

# Housing - Subdataset
housing <- subset(data, select = c(Collapsed_Race, V0961))
housing <- subset(housing, V0961>0)

# Housing - Homelessness Percentages
whitehomeless <- round((nrow(housing[housing$Collapsed_Race=="White"&housing$V0961==1,])/nrow(housing[housing$Collapsed_Race=="White",]))*100,2)
blackhomeless <- round((nrow(housing[housing$Collapsed_Race=="Black"&housing$V0961==1,])/nrow(housing[housing$Collapsed_Race=="Black",]))*100,2)
bothhomeless <- round((nrow(housing[housing$Collapsed_Race=="BothBW"&housing$V0961==1,])/nrow(housing[housing$Collapsed_Race=="BothBW",]))*100,2)
nbnwhomeless <- round((nrow(housing[housing$Collapsed_Race=="NBNW"&housing$V0961==1,])/nrow(housing[housing$Collapsed_Race=="NBNW",]))*100,2)

# Housing - Homelessness ChiSqaure
homeless_chisq <- chisq.test(table(housing$Collapsed_Race,housing$V0961))
print(homeless_chisq)

# Programming - Subdataset
programming_nolonger <- subset(data, select = c(Collapsed_Race, V1468, V1469, V1470, V1471, V1472, V1473, V1474, V1475))

programming_none_job <- subset(data, select = c(Collapsed_Race, V1478))
programming_none_job <- subset(programming_none_job, V1478>-2)
programming_none_ed <- subset(data, select = c(Collapsed_Race, V1510))
programming_none_ed <- subset(programming_none_ed, V1510>-2)

# Programming - Reason No Longer Barplot
programming_nolonger_completed_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1468==1,])
programming_nolonger_completed_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1468==1,])
programming_nolonger_completed_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1468==1,])
programming_nolonger_completed_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1468==1,])

programming_nolonger_graduated_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1469==2,])
programming_nolonger_graduated_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1469==2,])
programming_nolonger_graduated_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1469==2,])
programming_nolonger_graduated_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1469==2,])

programming_nolonger_quit_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1470==3,])
programming_nolonger_quit_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1470==3,])
programming_nolonger_quit_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1470==3,])
programming_nolonger_quit_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1470==3,])

programming_nolonger_notallowed_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1471==4,])
programming_nolonger_notallowed_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1471==4,])
programming_nolonger_notallowed_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1471==4,])
programming_nolonger_notallowed_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1471==4,])

programming_nolonger_transfered_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1472==5,])
programming_nolonger_transfered_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1472==5,])
programming_nolonger_transfered_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1472==5,])
programming_nolonger_transfered_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1472==5,])

programming_nolonger_availability_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1473==6,])
programming_nolonger_availability_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1473==6,])
programming_nolonger_availability_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1473==6,])
programming_nolonger_availability_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1473==6,])

programming_nolonger_other_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1474==7,])
programming_nolonger_other_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1474==7,])
programming_nolonger_other_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1474==7,])
programming_nolonger_other_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1474==7,])

programming_nolonger_unknown_black <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="Black"&programming_nolonger$V1475==7,])
programming_nolonger_unknown_white <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="White"&programming_nolonger$V1475==7,])
programming_nolonger_unknown_both <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="BothBW"&programming_nolonger$V1475==7,])
programming_nolonger_unknown_nbnw <- nrow(programming_nolonger[programming_nolonger$Collapsed_Race=="NBNW"&programming_nolonger$V1475==7,])

programming_nolonger_matrix <- matrix(c(programming_nolonger_completed_black,programming_nolonger_completed_white,
                                        programming_nolonger_completed_both,programming_nolonger_completed_nbnw,
                                        programming_nolonger_graduated_black,programming_nolonger_graduated_white,
                                        programming_nolonger_graduated_both,programming_nolonger_graduated_nbnw,
                                        programming_nolonger_quit_black,programming_nolonger_quit_white,
                                        programming_nolonger_quit_both,programming_nolonger_quit_nbnw,
                                        programming_nolonger_notallowed_black,programming_nolonger_notallowed_white,
                                        programming_nolonger_notallowed_both,programming_nolonger_notallowed_nbnw,
                                        programming_nolonger_transfered_black,programming_nolonger_transfered_white,
                                        programming_nolonger_transfered_both,programming_nolonger_availability_nbnw,
                                        programming_nolonger_availability_black,programming_nolonger_availability_white,
                                        programming_nolonger_availability_both,programming_nolonger_graduated_nbnw,
                                        programming_nolonger_other_black,programming_nolonger_other_white,
                                        programming_nolonger_other_both,programming_nolonger_other_nbnw,
                                        programming_nolonger_unknown_black,programming_nolonger_unknown_white,
                                        programming_nolonger_unknown_both,programming_nolonger_unknown_nbnw),nrow=4, ncol=8)
rownames(programming_nolonger_matrix) <- c("Black", "White", "BothBW", "NBNW")
colnames(programming_nolonger_matrix) <- c("Completed", "Graduated", "Quit", "No Longer \nAllowed", "Transfered", "No Longer \nAvailable", "Some Other \nReason", "Don't \nKnow")

par(mar=c(5,15,4,2))
barplot(height=programming_nolonger_matrix,xlim=c(0,400),cex.axis=2.5,horiz=TRUE,las=1,cex.names = 2.5,beside=TRUE, col=c("red","purple","green","blue"))
legend("topright",rownames(programming_nolonger_matrix),fill = c("red", "purple", "green", "blue"))
dev.off()

# Programming - Reason Job Percentage Table
programmingnoneJobPercent <- function(race,category){
  tempdf <- programming_none_job[programming_none_job$Collapsed_Race==race,]
  total <- nrow(tempdf)
  tempdf <- tempdf[tempdf$V1478==category,]
  subtotal <- nrow(tempdf)
  return(round((subtotal/total)*100,2))
}

programming_none_job_ptable <- matrix(c(programmingnoneJobPercent("Black",-1),programmingnoneJobPercent("White",-1),
                          programmingnoneJobPercent("BothBW",-1),programmingnoneJobPercent("NBNW",-1),
                          programmingnoneJobPercent("Black",1),programmingnoneJobPercent("White",1),
                          programmingnoneJobPercent("BothBW",1),programmingnoneJobPercent("NBNW",1),
                          programmingnoneJobPercent("Black",2),programmingnoneJobPercent("White",2),
                          programmingnoneJobPercent("BothBW",2),programmingnoneJobPercent("NBNW",2),
                          programmingnoneJobPercent("Black",3),programmingnoneJobPercent("White",3),
                          programmingnoneJobPercent("BothBW",3),programmingnoneJobPercent("NBNW",3),
                          programmingnoneJobPercent("Black",4),programmingnoneJobPercent("White",4),
                          programmingnoneJobPercent("BothBW",4),programmingnoneJobPercent("NBNW",4),
                          programmingnoneJobPercent("Black",5),programmingnoneJobPercent("White",5),
                          programmingnoneJobPercent("BothBW",5),programmingnoneJobPercent("NBNW",5), 
                          programmingnoneJobPercent("Black",6),programmingnoneJobPercent("White",6),
                          programmingnoneJobPercent("BothBW",6),programmingnoneJobPercent("NBNW",6),
                          programmingnoneJobPercent("Black",7),programmingnoneJobPercent("White",7),
                          programmingnoneJobPercent("BothBW",7),programmingnoneJobPercent("NBNW",7),
                          programmingnoneJobPercent("Black",8),programmingnoneJobPercent("White",8),
                          programmingnoneJobPercent("BothBW",8),programmingnoneJobPercent("NBNW",8),
                          programmingnoneJobPercent("Black",9),programmingnoneJobPercent("White",9),
                          programmingnoneJobPercent("BothBW",9),programmingnoneJobPercent("NBNW",9),
                          programmingnoneJobPercent("Black",10),programmingnoneJobPercent("White",10),
                          programmingnoneJobPercent("BothBW",10),programmingnoneJobPercent("NBNW",10)),ncol=11)

rownames(programming_none_job_ptable) <- c("Black","White","BothBW","NBNW")
colnames(programming_none_job_ptable) <- c("Don't Know","Doesn't Know Anything \nAbout Program","Doesn't Need \nProgram",
                             "Hasn't Been Offered the \nChance to Attend","Has Heard \nBad Things",
                             "Staff Didn't Want \nThem to Attend", "Too Busy to \nAttend", 
                             "Not Qualified\n /Allowed to Attend", "Could Not Get In \n/Wait-Listed", 
                             "No Specific Reason", "Some Other Reason")
programming_none_job_ptable <- as.table(programming_none_job_ptable)
print(programming_none_job_ptable)

# Programming - Grouped Percentage Job Reason Barplot
par(mar=c(5,20,4,2))
barplot(height = programming_none_job_ptable, xlim=c(0,40),cex.axis=2.5,las=1,cex.names=2,horiz=TRUE,beside = TRUE, col=c("red","purple", "green","blue"))
legend(25,15,rownames(programming_none_job_ptable),fill = c("red", "purple", "green", "blue"))
dev.off()

# Programming - Reason Education Percentage Table
programmingnoneEdPercent <- function(race,category){
  tempdf <- programming_none_ed[programming_none_ed$Collapsed_Race==race,]
  total <- nrow(tempdf)
  tempdf <- tempdf[tempdf$V1510==category,]
  subtotal <- nrow(tempdf)
  return(round((subtotal/total)*100,2))
}

programming_none_ed_ptable <- matrix(c(programmingnoneEdPercent("Black",-1),programmingnoneEdPercent("White",-1),
                                        programmingnoneEdPercent("BothBW",-1),programmingnoneEdPercent("NBNW",-1),
                                        programmingnoneEdPercent("Black",1),programmingnoneEdPercent("White",1),
                                        programmingnoneEdPercent("BothBW",1),programmingnoneEdPercent("NBNW",1),
                                        programmingnoneEdPercent("Black",2),programmingnoneEdPercent("White",2),
                                        programmingnoneEdPercent("BothBW",2),programmingnoneEdPercent("NBNW",2),
                                        programmingnoneEdPercent("Black",3),programmingnoneEdPercent("White",3),
                                        programmingnoneEdPercent("BothBW",3),programmingnoneEdPercent("NBNW",3),
                                        programmingnoneEdPercent("Black",4),programmingnoneEdPercent("White",4),
                                        programmingnoneEdPercent("BothBW",4),programmingnoneEdPercent("NBNW",4),
                                        programmingnoneEdPercent("Black",5),programmingnoneEdPercent("White",5),
                                        programmingnoneEdPercent("BothBW",5),programmingnoneEdPercent("NBNW",5), 
                                        programmingnoneEdPercent("Black",6),programmingnoneEdPercent("White",6),
                                        programmingnoneEdPercent("BothBW",6),programmingnoneEdPercent("NBNW",6),
                                        programmingnoneEdPercent("Black",7),programmingnoneEdPercent("White",7),
                                        programmingnoneEdPercent("BothBW",7),programmingnoneEdPercent("NBNW",7),
                                        programmingnoneEdPercent("Black",8),programmingnoneEdPercent("White",8),
                                        programmingnoneEdPercent("BothBW",8),programmingnoneEdPercent("NBNW",8),
                                        programmingnoneEdPercent("Black",9),programmingnoneEdPercent("White",9),
                                        programmingnoneEdPercent("BothBW",9),programmingnoneEdPercent("NBNW",9),
                                        programmingnoneEdPercent("Black",10),programmingnoneEdPercent("White",10),
                                        programmingnoneEdPercent("BothBW",10),programmingnoneEdPercent("NBNW",10)),ncol=11)

rownames(programming_none_ed_ptable) <- c("Black","White","BothBW","NBNW")
colnames(programming_none_ed_ptable) <- c("Don't Know","Doesn't Know Anything \nAbout Program","Doesn't Need Program/ \nNot Interested in Program",
                                           "Hasn't Been Offered the \nChance to Attend Program","Has Heard Bad \nThings About Program",
                                           "Staff Didn't Want \nThem to Attend Program", "Too Busy to \nAttend Program", 
                                           "Not Qualified\n /Allowed to Attend Program", "Could Not Get Into \nProgram/Wait-Listed", 
                                           "No Specific Reason", "Some Other Reason")
programming_none_ed_ptable <- as.table(programming_none_ed_ptable)
print(programming_none_ed_ptable)

# Programming - Grouped Percentage Education Reason Barplot
par(mar=c(5,22,4,2))
barplot(height = programming_none_ed_ptable, xlim=c(0,40), cex.axis=2.5,las=1,cex.names=2,horiz=TRUE,beside = TRUE, col=c("red","blue", "green","purple"))
legend(30,5,rownames(programming_none_ed_ptable),fill = c("red", "blue", "green", "purple"),cex=0.75)

# Programming - Reason ChiSquare
programming_none_job_chisq <- chisq.test(table(programming_none$Collapsed_Race,programming_none$V1477))
programming_none_ed_chisq <- chisq.test(table(programming_none$Collapsed_Race,programming_none$V1510))

