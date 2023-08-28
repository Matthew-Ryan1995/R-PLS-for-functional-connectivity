## Matthew Ryan
## 18/11/2022
# packages ----------------------------------------------------------------

pacman::p_load(tidyverse, patchwork, figpatch)

height <- 8

# functions ---------------------------------------------------------------

load_images <- function(dataset,  predictor){
  
  if(dataset == "cobre"){
    py_plot = "COBRE MSDL"
  }else if(dataset == "cobre_aal"){
    py_plot = "COBRE AAL"
  }else{
    py_plot = "ABIDE AAL"
  }
  
  py_pos = fig(glue::glue("img/{py_plot}_{predictor}_positive.png"))
  py_neg = fig(glue::glue("img/{py_plot}_{predictor}_negative.png"))
  
  R_num = case_when(str_detect(predictor, "age") ~ 1,
                    str_detect(predictor, "group") ~ 2,
                    str_detect(predictor, "sex") ~ 3,
                    TRUE ~ 4)
  
  R_plot = fig(glue::glue("img/{dataset}_coefficient_subnetworks_TRUE_{R_num}.png"))
  
  p = py_pos/py_neg/R_plot + plot_layout(tag_level = "new")
  return(p)
}


# COBRE MSDL plots --------------------------------------------------------
preds <- c("age", "groupPatient")
dataset <- "cobre"
p1 <- load_images(dataset, preds[1])
p2 <- load_images(dataset, preds[2])

p <- (p1 | p2) +
  plot_annotation(tag_levels = c("A", "1")) &
  theme(text = element_text(family = "Times New Roman"))

ggsave("../R-PLS -Scientific Reports/fig/Figure_1_cobre_results.png", plot = p,
       height = height, width = 0.9*height, bg="transparent",
       dpi = 900)

# COBRE AAL plots --------------------------------------------------------
preds <- c("age", "groupPatient")
dataset <- "cobre_aal"
p1 <- load_images(dataset, preds[1]) 
p2 <- load_images(dataset, preds[2]) 

p <- (p1 | p2) +
  plot_annotation(tag_levels = c("A", "1")) &
  theme(text = element_text(family = "Times New Roman"))

ggsave("../R-PLS -Scientific Reports/fig/Figure_2_cobre_aal_results.png", plot = p,
       height = height, width = 0.9*height,
       dpi = 900)


# COBRE AAL plots --------------------------------------------------------
preds <- c("age", "groupAutism", "sexMale", "eyeClosed")
dataset <- "abide"
p1 <- load_images(dataset, preds[1])
p2 <- load_images(dataset, preds[2])
p3 <- load_images(dataset, preds[3])
p4 <- load_images(dataset, preds[4])

pp1 <- (p1 | p2) +
  plot_annotation(tag_levels = c("A", "1")) &
  theme(text = element_text(family = "Times New Roman"))
pp2 <- (p3 | p4) +
  plot_annotation(tag_levels = c("A", "1")) &
  theme(text = element_text(family = "Times New Roman"))

ggsave("../R-PLS -Scientific Reports/fig/Figure_3_abide_results_age_group.png", plot = pp1,
       height = height, width = 0.9*height, bg="transparent",
       dpi = 900)
ggsave("../R-PLS -Scientific Reports/fig/Figure_4_abide_results_sex_eye.png", plot = pp2,
       height = height, width =0.9*height, bg="transparent",
       dpi = 900)