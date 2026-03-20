library(readr)
df <- read_csv("~/Trabajos en R/12. Videogame Sales.csv")
View(df)
library(tidyverse) 

#usamos summary para visualizar lo que tenemos

summary(df)

#buscamos NA sumando los NA que se encuentren en cada variable

colSums(is.na(df))

#Nos encontramos con 0 NA, sin embargo la variable year la toma como character


colSums(df== "N/A")

#hay datos faltantes pero escritos como N/A
#se eliminan los NA, Years no se puede imputar
#publisher no sirve imputarlo porque se van a trabajar solo con tres empresas 
#eliminamos los NA en publisher y year. Cambiamos de clase Year a entero

df <- df %>% 
  filter( Publisher != "N/A") %>% 
  filter( Year != "N/A") %>% 
  mutate(Year= as.integer(Year))



#ahora eliminamos las variables que no vamos a usar y filtramos filas 

df_limpio <- df %>% 
  select(-Platform, -Genre, -NA_Sales, -EU_Sales, -JP_Sales, -Other_Sales) %>% 
  filter( Publisher %in%c("Nintendo", "Sony Computer Entertainment
", "Microsoft Game Studios") )

#por ultimo cambiamos el nombre de una variable 

df_limpio <- df_limpio %>% 
  rename(Global_Sales_Millons=Global_Sales)

write_csv(df_limpio, "dataset_limpio.csv")



