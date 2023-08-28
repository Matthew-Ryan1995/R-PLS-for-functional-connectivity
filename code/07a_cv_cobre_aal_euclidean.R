
# libraries ---------------------------------------------------------------
pacman::p_load(tidyverse, phdWork, rsample, yardstick)

walk(c("code/cross_validate_pls2.R"), source)
slurm_ntasks <- as.numeric(Sys.getenv("SLURM_NTASKS")) # Obtain environment variable SLURM_NTASKS
if (!is.na(slurm_ntasks)) {
  cores = slurm_ntasks # if slurm_ntasks is numerical, then assign it to cores
}else {
  cores = detectCores() - 1 # Figure out how many cores there are
}


# Data --------------------------------------------------------------------
df <- cobre_aal %>%
  select(age, group, cors) %>%
  mutate(
    group = fct_relevel(group, "Control"),
    cors = map(cors, function(c){
      c <- c[upper.tri(c)]
      names(c) <- str_c("X", 1:length(c))
      c <- as_tibble(t(c))
      return(c)
    })
  ) %>%
  unnest(cors)

model_formula <- ~ age + group


# seed and CV -------------------------------------------------------------

set.seed(1668286)

folds <- rsample::vfold_cv(df, v = 10, strata = group)


# run cv ------------------------------------------------------------------

results <- cv_rpls_fit(folds, model_formula, mc.cores = cores)

write_rds(results, "results/cobre_aal_cv_results_euclidean.Rds")

# Fisher --------------------------------------------------------------------
df <- cobre %>%
  select(age, group, cors) %>%
  mutate(
    group = fct_relevel(group, "Control"),
    cors = map(cors, function(c){
      c <- atanh(c[upper.tri(c)])
      names(c) <- str_c("X", 1:length(c))
      c <- as_tibble(t(c))
      return(c)
    })
  ) %>%
  unnest(cors)

model_formula <- ~ age + group


# seed and CV -------------------------------------------------------------

set.seed(1668286)

folds <- rsample::vfold_cv(df, v = 10, strata = group)


# run cv ------------------------------------------------------------------

results <- cv_rpls_fit(folds, model_formula, mc.cores = cores)

write_rds(results, "results/cobre_aal_cv_results_fisher.Rds")
