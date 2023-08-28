## Matthew Ryan
## 18/11/2022
# packages ----------------------------------------------------------------

pacman::p_load(tidyverse, patchwork, figpatch)

height <- 8

# functions ---------------------------------------------------------------

stack_imgs <- function(img_list){
  
  p = img_list[[1]]
  
  for(i in 2:length(img_list)){
    p = p / img_list[[i]]
  }
  
  p <- p + plot_layout(tag_level = "new")
  return(p)
}

fl <- list.files("img/", pattern="msdl_[A-Z]+", full.names = T)
sub_imgs <- 3

for(i in 1:(ceiling(length(fl)/sub_imgs))){
  sub_fl <- fl[(sub_imgs*(i-1) + 1):(sub_imgs*i)]
  sub_fl <- na.omit(sub_fl)
  imgs <- map(sub_fl, fig)
  pp <- stack_imgs(imgs)
  ggsave(glue::glue("../R-PLS -Scientific Reports/fig/Supp_Figure_MSDL_{i}.png"), 
         plot=pp, dpi=900)
}

fl <- list.files("img/", pattern="aal_[A-Z]+", full.names = T)
sub_imgs <- 3

for(i in 1:(ceiling(length(fl)/sub_imgs))){
  sub_fl <- fl[(sub_imgs*(i-1) + 1):(sub_imgs*i)]
  sub_fl <- na.omit(sub_fl)
  imgs <- map(sub_fl, fig)
  pp <- stack_imgs(imgs)
  ggsave(glue::glue("../R-PLS -Scientific Reports/fig/Supp_Figure_AAL_{i}.png"), 
         plot=pp, dpi=900)
}
# 
# imgs <- map(fl, fig)
# 
# pp <- stack_imgs(imgs)
# 
# ggsave("test.png", plot=pp, dpi=900)
