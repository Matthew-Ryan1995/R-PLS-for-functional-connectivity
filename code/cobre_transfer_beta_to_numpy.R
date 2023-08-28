
# Libraries ---------------------------------------------------------------

pacman::p_load(tidyverse, reticulate, phdWork, glue)

source("code/calculate_vip.R")

# Data --------------------------------------------------------------------
dataset <- "cobre"
M <- read_rds("results/cobre_rpls_model_K_3.Rds")
regions <- read_csv("data/msdl_rois_labels.csv",
                    col_types = cols())

Tmat <- do.call(cbind, M$scoresX)
P.hat <- do.call(cbind, M$loadingsX)
W.hat <- do.call(cbind, M$weightsX)
C.hat <- do.call(cbind, M$weightsY)
B <- map_dbl(M$reg_steps, ~.x$b1) %>%
  diag()
Y <- M$Y[[1]]

beta <- W.hat %*% solve(t(P.hat) %*% W.hat) %*% B %*% t(C.hat)


true_vip <- calculate_vip(Tmat = Tmat, W = W.hat,  Y = Y)

# Significant values ------------------------------------------------------
fl <- list.files("results/cobre_vip/", full.names = T)
sig <- map(fl, read_rds)
sig <- (Reduce("+", sig)/200)
sig[1:39, ] <- 1
sig <- sig %>%
  apply(2, p.adjust, method = "fdr")

SIG <- sig %>% 
  as_tibble(rownames = "pred") %>% 
  mutate(ss = map(pred, str_split, "-"),
         s1 = map_chr(ss, ~.x[[1]][[1]]),
         s2 = map_chr(ss, ~.x[[1]][[2]])) %>% 
  select(s1, s2, full_vip) %>% 
  pivot_wider(names_from=s2, values_from=full_vip) %>% 
  select(-s1) %>% 
  as.matrix()
SIG[which(is.na(SIG), arr.ind = T)] <- 0
SIG <- SIG + t(SIG)

np = import("numpy")

for (j in 1:ncol(beta)){
  P_true <- unvec(P = M$muX, vec = beta[, j])
  P_true[SIG>0.05] <- 0
  np$save(glue("data/{dataset}_{colnames(beta)[j]}_coeffs.npy"),
          r_to_py(P_true))
}





# np$save("test_numpy.npy", r_to_py(P_true))