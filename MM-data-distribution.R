library(ggplot2)
library(gcookbook)
merge.MM.FF2_2016_2020 <- read.table(file="D:/Myanmar/merge_event_eq (isap91 arrival _ pick_result)_final", header = T,sep = ",", fill=TRUE)
# merge.MM.FF2_2016_2020 <- read.table(file="D:/緬甸BH/merge_event_eq.csv", header = T,sep = ",", fill=TRUE)
# merge.MM.FF2_2016_2020_cut <- read.table(file="D:/緬甸BH/merge_event_eq_cut.csv", header = T,sep = ",", fill=TRUE)

plot_rec <- merge.MM.FF2_2016_2020
plot_rec <- plot_rec[order(plot_rec$picks_result),]
# plot_rec <- merge.MM.FF2_2016_2020[350:1077,1:44]

####################### 資料統計 ##########################
need_data_index <- which((plot_rec$dist_surface>100 & plot_rec$Mw>5.5) | plot_rec$dist_surface<100)#把符合條件的地震抓出
for(i in need_data_index){
  need_data_index <- c(need_data_index,which(plot_rec$sta_get_time==plot_rec[i,2])) #把符合條件的地震抓出後延伸到收到該地震的所有測站，
}
need_data_index <- need_data_index[!duplicated(need_data_index)] #扣掉重複的index
need_data_index <- need_data_index[order(need_data_index)] #把index排好
need_data <- plot_rec[need_data_index,1:44] #follow index取出要的資料(依照給定的規則)
need_data[1] <- c(1:length(need_data_index)) #把index行弄成新的index按照順序排好(也可以不要)

plot_rec["DO"] <- c(1:length(plot_rec[,1]))#建立DO這行
for(i in c(1:length(plot_rec[,1]))){
  ifelse(plot_rec[i,2] %in% need_data[,2], plot_rec["DO"][i,] <- 'yes', plot_rec["DO"][i,] <- 'no') #判斷要的資料是否有在原本的csv中

}

write.table(plot_rec,file="D:/Myanmar/merge_event_eq(add_cut).csv",sep=",",row.names=F, na = "NA") #新增DO到原本的cs

# write.table(need_data,file="D:/緬甸BH/merge_event_eq.csv",sep=",",row.names=F, na = "NA") #把要的資料輸出新的csv

####################### 圖形繪製 ##########################

## distance_Mw
p <-ggplot(plot_rec, aes(dist_sor, Mw, shape=picks_result , color =picks_result))+
    geom_point(size=5,shape=79)+
    # scale_shape_manual(values = c(1,19))+
    scale_color_manual(values = c("#0000E3", "#FF0000"))+
    ggtitle("Distance vs Mw (2016-2021)") + xlab("Distance (km)") + ylab("Mw")+
    scale_x_continuous(limits=c(30,2000),trans='log2',breaks=(c(1,2,5,10,20,50,100,200,500,1000,2000))
                       ,minor_breaks=c(seq(0.01,0.09,by=0.01),
                        seq(0.1,0.9,by=0.1),seq(1,10,by=1),
                        seq(10,100,by=10),seq(100,1000,by=100)))+
    scale_y_continuous(limits=c(3,7),breaks=(c(3,4,5,6,7)))+
    theme(panel.background=element_blank(),#去除背景
          panel.grid.major=element_line(colour='gray90', size=0.8),
          panel.grid.minor=element_line(colour='gray90', size=0.8),
          panel.border = element_rect(fill=NA,color="black", size=2, linetype="solid"),
          plot.margin = margin(1,1,0.1,0.1, "cm"),
          plot.title = element_text(hjust = 0.5,size=20),
          axis.title.x=element_text(hjust = 0.5,size=20),
          axis.title.y=element_text(hjust = 0.5,size=20),
          axis.text = element_text(size=20),
          )
ggsave("D:/Myanmar/2016-2021_total_distance_Mw_distribution(after_picking).png", p , width = 9, height = 7, dpi = 300)