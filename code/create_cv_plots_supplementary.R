## Matthew Ryan
## 28/08/20223
# packages ----------------------------------------------------------------

pacman::p_load(tidyverse, phdWork, patchwork)

dodge_pos <- 0.6
datasets <- c("cobre", "cobre_aal", "abide")

# functions ---------------------------------------------------------------

load_cv_data <- function(dataset){
  res_r <- read_rds(glue::glue("results/{dataset}_cv_results.Rds")) %>% 
    mutate(method="Riemannian")
  res_e <- read_rds(glue::glue("results/{dataset}_cv_results_euclidean.Rds")) %>% 
    mutate(method="Euclidean")
  res_f <- read_rds(glue::glue("results/{dataset}_cv_results_fisher.Rds")) %>% 
    mutate(method="Fisher")
  res <- bind_rows(res_r, res_e, res_f) %>% 
    filter(K<=10) %>% 
    group_by(K, method) %>% 
    summarise(m = mean(rmse), se = sd(rmse)/sqrt(n()), .groups = "drop") %>% 
    mutate(K = as.factor(K))
  return(res)
}

make_plot <- function(cv, title){
  pp <- cv %>% 
    ggplot(aes(x=K, y = m, colour = method)) +
    geom_point(position = position_dodge(width = dodge_pos), size = 2.5) +
    geom_linerange(aes(ymin=m-se, ymax=m+se), position = position_dodge(width = dodge_pos)) +
    theme_classic() +
    harrypotter::scale_color_hp_d("ravenclaw") +
    labs(x = "Number of latent variable (K)",
         y = "Cross validated RMSE",
         colour = "Method") +
    ggtitle(title) +
    theme(text = element_text(family = "Times New Roman", size= 16),
          plot.title = element_text(vjust = 0.5, hjust = 0.5))
  return(pp)
}


# get plots -------------------------------------------------------------
cobre_cv <- load_cv_data(datasets[1])
cobre_aal_cv <- load_cv_data(datasets[2])
abide_cv <- load_cv_data(datasets[3])

p_cobre <- make_plot(cobre_cv, "COBRE - MSDL")
p_cobre_aal <- make_plot(cobre_aal_cv, "COBRE - AAL")
p_abide <- make_plot(abide_cv, "ABIDE - AAL")

p <- ((p_cobre | p_cobre_aal) /(p_abide + plot_spacer())) +
  plot_layout(guides="collect") &
  theme(legend.position = "bottom")

ggsave("../R-PLS -Scientific Reports/fig/Supp_Figure_cv.png",
       plot = p, dpi = 900)
