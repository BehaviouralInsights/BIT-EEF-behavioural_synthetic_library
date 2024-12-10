#! /usr/bin/RScript
# Pipeline Code (only JSON output )

# setwd(getSrcDirectory(function() {})[1])
# Input -------------------------------------------------------------------
require(rlang, lib.loc = "C:\\Users\\iori.thomas\\AppData\\Local\\R\\win-library\\4.4")
require(jsonlite, lib.loc = "C:\\Users\\iori.thomas\\AppData\\Local\\R\\win-library\\4.4")
require(janitor, lib.loc = "C:\\Users\\iori.thomas\\AppData\\Local\\R\\win-library\\4.4")
require(tidyverse, lib.loc = "C:\\Users\\iori.thomas\\AppData\\Local\\R\\win-library\\4.4")
require(openxlsx, lib.loc = "C:\\Users\\iori.thomas\\AppData\\Local\\R\\win-library\\4.4")

command_line_options <- commandArgs(trailingOnly = TRUE)

# Folder location
folder_path_orig <- command_line_options[1]
folder_path_synth <- command_line_options[2]
folder_path_meta <- command_line_options[3]
# cwd <- "C:\\Code_Development\\EEF-LoFi-Synthetic-Data-Work\\development_version" # command_line_options[5]
# print(cwd)
print(folder_path_meta)

### Import data ####
# List all JSON files in the folder
json_files <- list.files(path = folder_path_orig, pattern = "\\.json$", full.names = TRUE)
# List all TSV files in the folder
tsv_files <- list.files(path = folder_path_synth, pattern = "\\.tsv$", full.names = TRUE)

print(tsv_files)
print(json_files)

# Function to read a single JSON file
read_json_file <- function(file_path) {
  fromJSON(file_path)
}

# Function to read a single TSV file
read_tsv_file <- function(file_path) {
  read_delim(file_path, delim = "\t", escape_double = FALSE, trim_ws = TRUE, comment = "#")
}

# Read all JSON files and store them in a list
json_list <- suppressMessages(lapply(json_files, read_json_file))

# Read all TSV files and store them in a list
data_list <- suppressMessages(lapply(tsv_files, read_tsv_file))

# Name each element in the list by the file name without the path
clean_names_orig <- json_files %>%
  basename() %>%
  tools::file_path_sans_ext() %>%
  janitor::make_clean_names()

clean_names_synth <- json_files %>%
  basename() %>%
  tools::file_path_sans_ext() %>%
  janitor::make_clean_names()

names(json_list) <- clean_names_orig
names(data_list) <- clean_names_synth



# Code --------------------------------------------------------------------
type_filter <- function(df, type) {
  if (type == "numeric") {
    df$Column_details %>%
      as_tibble() %>%
      filter(Type == "numeric") %>%
      select(any_of(c("Name", "mean", "standard_deviation", "missing_value_freq"))) %>%
      pivot_longer(cols = -Name, names_to = "stat", values_to = "value")
  } else if (type == "categorical") {
    df$Column_details %>%
      as_tibble() %>%
      filter(Type == "categorical") %>%
      select(where(~ !all(is.na(.)))) %>%
      select(-Type) %>%
      pivot_longer(
        cols = -Name,
        names_to = "Category_Option",
        values_to = "proportion"
      ) %>%
      filter(!is.na(proportion)) %>%
      filter(proportion != 0) %>% # remove any categories that have 0 frequency
      filter(!Name %in% c("Project", "Project_Type")) %>% # remove project and project_type
      filter(!str_detect(Name, "_Desc$"))
  } else {
    print("error: type not found")
  }
}

# Apply the filter and select function to each data frame in the list
numeric_json_list <- lapply(json_list, type_filter, type = "numeric")
cat_json_list <- lapply(json_list, type_filter, type = "categorical")

# Now that we extracted all numeric variables, we go to the synthetic data
# We extract the columns named in the Name column, then calculate the mean,
# standard deviation and missing_value_frequency

calculate_metrics <- function(data_df, name_df) {
  data_df %>%
    select(any_of(name_df$Name)) %>%
    summarise(across(everything(), list(
      mean = ~ mean(.x, na.rm = TRUE),
      standard_deviation = ~ sd(.x, na.rm = TRUE),
      missing_value_freq = ~ mean(is.na(.x))
    ), .names = "{col}__{fn}")) %>%
    t() %>%
    as.data.frame(stringsAsFactors = FALSE) %>%
    rownames_to_column(var = "Name_stat") %>%
    separate_wider_delim(cols = "Name_stat", delim = "__", names = c("Name", "stat")) %>%
    rename("value" = "V1")
}

# Apply the metric calculation function to each data frame in the list
metrics_list <- mapply(calculate_metrics, data_list, numeric_json_list, SIMPLIFY = FALSE)

### Combine the Metrics ###
combine_metrics <- function(json_df, metric_df) {
  combined <- json_df %>%
    left_join(metric_df, by = c("Name", "stat"), suffix = c("_original", "_synthetic"))
}

calculate_metrics_cat <- function(data_df, name_df) {
  data_df %>%
    select(any_of(name_df$Name)) %>%
    mutate(across(everything(), as.character)) %>% 
    pivot_longer(cols = everything(), names_to = "Name", values_to = "Category_Option") %>%
    group_by(Name, Category_Option) %>%
    summarise(proportion = n() / nrow(data_df), .groups = "drop") %>%
    mutate(Category_Option = if_else(is.na(Category_Option) | Category_Option == "NA", "nan", Category_Option)) %>%
    filter(!Name %in% c("Project", "Project_Type")) %>%
    filter(!str_detect(Name, "_Desc$"))
}

# Apply the metric calculation function to each data frame in the list
metrics_list_cat <- mapply(calculate_metrics_cat, data_list, cat_json_list, SIMPLIFY = FALSE)

# bobby add
cat_json_list <- cat_json_list %>% 
  map(
    function (x) {
      x %>% 
        mutate(Category_Option = if_else(
          !is.na(as.numeric(Category_Option)) & as.numeric(Category_Option) %% 1 == 0,
          as.character(round(as.numeric(Category_Option))),
          Category_Option
        )) %>%
        mutate(Category_Option = if_else(
          str_detect(Category_Option, "^[0-9]{4}-[0-9]{2}-[0-9]{2}.+"),
          str_sub(Category_Option, 1, 10),
          Category_Option
        )) %>% 
        mutate(Category_Option = if_else(
          !is.na(as.numeric(Category_Option)) & str_detect(Category_Option, "^-{0,1}\\d+\\.\\d{6,}$"),
          sprintf("%.5f", as.numeric(Category_Option)),
          Category_Option
        ))
    }
  )

# bobby add
metrics_list_cat <- metrics_list_cat %>%
  map(
    function (x) {
      x %>%
        mutate(Category_Option = if_else(
          !is.na(as.numeric(Category_Option)) & str_detect(Category_Option, "^-{0,1}\\d+\\.\\d{6,}$"),
          sprintf("%.5f", as.numeric(Category_Option)),
          Category_Option
        ))
    }
  )


### Combine the Metrics ###
combine_metrics_cat <- function(json_df, metric_df) {
  combined <- json_df %>%
    full_join(metric_df, by = c("Name", "Category_Option"), suffix = c("_original", "_synthetic"))
}

# Apply the combine function to each pair of data frames
combined_metrics_cat_list <- mapply(function(json_df, metric_df) {
  if (is.null(json_df) || is.null(metric_df)) {
    return(NULL)
  }
  combine_metrics_cat(json_df, metric_df)
}, cat_json_list, metrics_list_cat, SIMPLIFY = FALSE)


############ formal test. X^2 test (we want these datasets to be the same, so high p value)
calculate_chi_square <- function(data_list) {
  chi_square_results_list <- list()
  
  for (dataset_name in names(data_list)) {
    dataset_df <- data_list[[dataset_name]]
    
    selected_columns <- unique(dataset_df$Name)
    chi_square_results <- data.frame()
    
    for (col in selected_columns) {
      temp <- dataset_df %>%
        filter(Name == col) %>%
        filter(!is.na(proportion_synthetic) & !is.na(proportion_original))
      
      if (nrow(temp) < 2) {
        next
      }
      
      chisq_test <- chisq.test(temp$proportion_original, temp$proportion_synthetic, simulate.p.value = TRUE)
      
      chi_square_results <- rbind(chi_square_results, data.frame(
        Column = col,
        Chi_Square = chisq_test$statistic,
        p_value = chisq_test$p.value
      ))
    }
    
    chi_square_results_list[[dataset_name]] <- chi_square_results
  }
  
  return(chi_square_results_list)
}

# Apply the chi-square calculation function to the combined_metrics_cat_list
# chi_square_results_list <- calculate_chi_square(combined_metrics_cat_list)

####### 2. correlations

## numerical ##
calculate_correlations <- function(data_df, name_df) {
  selected_data <- data_df %>%
    select(any_of(name_df$Name))
  
  if (ncol(selected_data) <= 1) {
    return(NULL)
  }
  
  column_combinations <- combn(colnames(selected_data), 2, simplify = FALSE)
  correlation_results <- data.frame()
  
  for (combination in column_combinations) {
    col1 <- combination[1]
    col2 <- combination[2]
    
    # Calculate correlation
    cor_test <- cor.test(selected_data[[col1]], selected_data[[col2]],
                         alternative = "two.sided",
                         method = "pearson", exact = TRUE, conf.level = 0.95
    )
    
    # Store the result
    correlation_results <- rbind(
      correlation_results,
      data.frame(Column1 = col1, Column2 = col2, Correlation = cor_test$estimate, p_value = cor_test$p.value)
    )
  }
  return(correlation_results)
}


correlation_results_list <- mapply(function(data_df, name_df) {
  if (is.null(name_df) || nrow(name_df) == 0) {
    return(NULL)
  }
  calculate_correlations(data_df, name_df)
}, data_list, numeric_json_list, SIMPLIFY = FALSE)

## categorical data ##

# Function to calculate chi-square test of independence for categorical data
calculate_chi_square <- function(data_df, name_df) {
  selected_data <- data_df %>%
    select(any_of(name_df$Name))
  
  if (ncol(selected_data) <= 1) {
    return(NULL)
  }
  
  column_combinations <- combn(colnames(selected_data), 2, simplify = FALSE)
  chi_square_results <- data.frame()
  
  for (combination in column_combinations) {
    col1 <- combination[1]
    col2 <- combination[2]
    
    # Ensure both columns have at least 2 unique values
    if (length(unique(selected_data[[col1]])) < 2 | length(unique(selected_data[[col2]])) < 2) {
      next
    }
    
    # Create a contingency table
    contingency_table <- table(selected_data[[col1]], selected_data[[col2]])
    
    # Ensure the contingency table has at least 2 rows and 2 columns
    if (nrow(contingency_table) < 2 | ncol(contingency_table) < 2) {
      next
    }
    # Perform chi-square test
    chi_square_test <- chisq.test(contingency_table, simulate.p.value = TRUE)
    
    # Store the result
    chi_square_results <- rbind(chi_square_results, data.frame(
      Column1 = col1,
      Column2 = col2,
      Chi_Square = chi_square_test$statistic,
      p_value = chi_square_test$p.value
    ))
  }
  return(chi_square_results)
}

# Apply the chi-square calculation function to each data frame in the list
chi_square_results_list <- mapply(function(data_df, name_df) {
  if (is.null(name_df) || nrow(name_df) == 0) {
    return(NULL)
  }
  calculate_chi_square(data_df, name_df)
}, data_list, cat_json_list, SIMPLIFY = FALSE)


##### #### correlation between categorical and numerical ######################
## ANOVA between categorical and numerical columns ##

calculate_anova <- function(data_df, num_name_df, cat_name_df) {
  selected_num_data <- data_df %>%
    select(any_of(num_name_df$Name))
  
  selected_cat_data <- data_df %>%
    select(any_of(cat_name_df$Name))
  
  anova_results <- data.frame()
  
  for (num_col in colnames(selected_num_data)) {
    for (cat_col in colnames(selected_cat_data)) {
      # Ensure both columns have at least 2 unique values
      if (length(unique(selected_num_data[[num_col]])) < 2 | length(unique(selected_cat_data[[cat_col]])) < 2) {
        next
      }
      
      # Ensure the categorical column has at least 2 levels and convert to factor
      cat_col_data <- as.factor(selected_cat_data[[cat_col]])
      if (nlevels(cat_col_data) < 2) {
        next
      }
      
      # Perform ANOVA
      anova_test <- aov(selected_num_data[[num_col]] ~ cat_col_data, data = data_df)
      p_value <- summary(anova_test)[[1]][["Pr(>F)"]][1]
      
      # Store the result
      anova_results <- rbind(anova_results, data.frame(
        Numeric_Column = num_col,
        Categorical_Column = cat_col,
        p_value = p_value
      ))
    }
  }
  return(anova_results)
}

# Apply the ANOVA calculation function to each data frame in the list
anova_results_list <- mapply(function(data_df, num_name_df, cat_name_df) {
  if (is.null(num_name_df) || nrow(num_name_df) == 0 || is.null(cat_name_df) || nrow(cat_name_df) == 0) {
    return(NULL)
  }
  calculate_anova(data_df, num_name_df, cat_name_df)
}, data_list, numeric_json_list, cat_json_list, SIMPLIFY = FALSE)

# Function to rename columns
rename_columns <- function(df) {
  if (!is.null(df)) {
    cols <- names(df)
    if ("Column1" %in% cols) {
      df <- df %>% rename(Comparison_column_1 = Column1)
    }
    if ("Column2" %in% cols) {
      df <- df %>% rename(Comparison_column_2 = Column2)
    }
    if ("Numeric_Column" %in% cols) {
      df <- df %>% rename(Comparison_column_1 = Numeric_Column)
    }
    if ("Categorical_Column" %in% cols) {
      df <- df %>% rename(Comparison_column_2 = Categorical_Column)
    }
    df
  } else {
    NULL
  }
}

# Rename columns in all datasets
anova_results_list <- map(anova_results_list, rename_columns)
chi_square_results_list <- map(chi_square_results_list, rename_columns)
correlation_results_list <- map(correlation_results_list, rename_columns)

# Get all unique dataset names across the three lists
all_names <- unique(c(names(anova_results_list), names(chi_square_results_list), names(correlation_results_list)))

# Initialize an empty list to store the combined datasets
combined_results_list <- list()

# Loop through each unique dataset name and combine the corresponding datasets
for (name in all_names) {
  combined_results_list[[name]] <- bind_rows(
    if (!is.null(anova_results_list[[name]])) anova_results_list[[name]] %>% mutate(test = "anova") else NULL,
    if (!is.null(chi_square_results_list[[name]])) chi_square_results_list[[name]] %>% mutate(test = "chi_square") else NULL,
    if (!is.null(correlation_results_list[[name]])) correlation_results_list[[name]] %>% mutate(test = "correlation") else NULL
  )
}

print("Here is the output!!!!")
# Output ------------------------------------------------------------------
# Convert combined_metrics_list to JSON and save
# numerical_metrics_comparison_json <- toJSON(combined_metrics_list, pretty = TRUE)
numerical_metrics_comparison_json <- toJSON(metrics_list, pretty = TRUE)
file_loc <- paste(c(trimws(folder_path_meta), "numerical_metrics_comparison.json"), collapse = "\\")
print(file_loc)
write(numerical_metrics_comparison_json, file = file_loc) # "numerical_metrics_comparison.json") # nolint: line_length_linter.
print(file_loc)

# Convert combined_metrics_cat_list to JSON and save
categorical_metrics_comparison_json <- toJSON(combined_metrics_cat_list, pretty = TRUE)
file_loc <- paste(c(trimws(folder_path_meta), "categorical_metrics_comparison.json"), collapse = "\\")
write(categorical_metrics_comparison_json, file = file_loc) # "categorical_metrics_comparison_json")
print(file_loc)

# Convert combined_results to JSON and save
corr_p_values_json <- toJSON(combined_results_list, pretty = TRUE)
file_loc <- paste(c(trimws(folder_path_meta), "corr_p_values.json"), collapse = "\\")
write(corr_p_values_json, file = file_loc) # "corr_p_values.json")
print(file_loc)

