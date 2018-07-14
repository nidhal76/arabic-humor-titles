results <- read.csv("/Users/mikahama/Desktop/f1283541.csv")
master <- head(results, 1000)
apprentice <- tail(results, 1000)

master_avg <- colMeans(x=data.frame(master$q_1,master$q_2,master$q_3,master$q_4,master$q_5,master$q_6,master$q_7,master$q_8,master$q_9), na.rm = TRUE)
apprentice_avg <- colMeans(x=data.frame(apprentice$q_1,apprentice$q_2,apprentice$q_3,apprentice$q_4,apprentice$q_5,apprentice$q_6,apprentice$q_7,apprentice$q_8,apprentice$q_9), na.rm = TRUE)
titles = c("Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9")

height <- rbind(master_avg, apprentice_avg)
mp <- barplot(height, beside = TRUE,
              ylim = c(0, 5), names.arg = titles)
text(mp, height, labels = format(height,3),
     pos = 3, cex = .75)
