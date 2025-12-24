library(dplyr)

# Load data
data <- read.csv("data.csv")

# Process data
result <- data %>%
  filter(age > 18) %>%
  group_by(category) %>%
  summarise(
    total = sum(amount),
    average = mean(amount),
    count = n()
  ) %>%
  arrange(desc(total))

# Save results
write.csv(result, "output.csv")
print(result)