import pandas as pd

# Load data from a CSV file
def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

# Filter data based on a specific condition (age threshold)
def filter_data(data, age_threshold):
    """Filter data based on a specific condition (age threshold)."""
    filtered_data = data[data['age'] > age_threshold]
    return filtered_data

# Group data by a categorical column and calculate aggregate statistics
def aggregate_data(data, group_column):
    """Group data by a categorical column and calculate aggregate statistics."""
    aggregated_data = data.groupby(group_column).agg({
        'amount': ['sum', 'mean', 'count']
    })
    aggregated_data.columns = ['total', 'average', 'count']
    return aggregated_data

# Arrange data in descending order
def arrange_data(data, order_column):
    """Arrange data in descending order."""
    arranged_data = data.sort_values(by=order_column, ascending=False)
    return arranged_data

# Save processed data to a CSV file
def save_data(data, file_path):
    """Save processed data to a CSV file."""
    try:
        data.to_csv(file_path, index=True)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

# Print the processed data
def print_data(data):
    """Print the processed data."""
    print(data)

# Main function
def main():
    file_path = "data.csv"
    age_threshold = 18
    group_column = 'category'
    order_column = 'total'
    output_file_path = "outputs/output.csv"

    # Load data
    data = load_data(file_path)
    if data is not None:
        # Filter data
        filtered_data = filter_data(data, age_threshold)
        
        # Aggregate data
        aggregated_data = aggregate_data(filtered_data, group_column)
        
        # Arrange data
        arranged_data = arrange_data(aggregated_data, order_column)
        
        # Save data
        save_data(arranged_data, output_file_path)
        
        # Print data
        print_data(arranged_data)

if __name__ == "__main__":
    main()