
# Libraries ---------------------------------------------------------------

pacman::p_load(tidyverse, reticulate, phdWork, glue)

source("code/calculate_vip.R")


# Data --------------------------------------------------------------------
dataset <- "abide"
M <- read_rds("results/abide_rpls_model_K_6.Rds")

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
ordering <- rownames(beta)
find_val <- function(s){
  which(s == ordering)
}

fl <- list.files("results/abide_vip/", full.names = T)
sig <- map(fl, read_rds)
sig <- do.call(rbind, sig)
sig <- sig/200
sig <- sig %>% 
  as_tibble(rownames = "pred") %>% 
  mutate(nn = map_dbl(pred, find_val)) %>% 
  arrange(nn) %>%
  select(-nn) 
sig_rows = sig$pred
sig <- sig %>% 
  select(-pred) %>% 
  as.matrix()
rownames(sig) <- sig_rows
sig[1:116, ] <- 1
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