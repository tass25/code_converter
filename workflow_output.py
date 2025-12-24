import pandas as pd

# Load data from a CSV file
def load_data(file_name):
    """Load data from a CSV file."""
    return pd.read_csv(file_name)

# Filter data to include only rows where age exceeds a certain threshold
def filter_data(data, age_threshold):
    """Filter data to include only rows where age exceeds a certain threshold."""
    return data[data['age'] > age_threshold]

# Group data by a categorical column and calculate aggregate statistics
def group_and_aggregate(data, group_by_column, statistics):
    """Group data by a categorical column and calculate aggregate statistics."""
    aggregated_data = data.groupby(group_by_column).agg({
        'amount': ['sum', 'mean', 'count']
    })
    aggregated_data.columns = ['total', 'average', 'count']
    return aggregated_data

# Sort data in descending order by a specific column
def sort_data(data, sort_column):
    """Sort data in descending order by a specific column."""
    return data.sort_values(by=sort_column, ascending=False)

# Save data to a file and display it
def save_and_display(data, file_name):
    """Save data to a file and display it."""
    data.to_csv(file_name)
    print(data)

# Main function
def main():
    # Load data
    data = load_data('data.csv')
    
    # Filter data
    filtered_data = filter_data(data, 18)
    
    # Group and aggregate data
    aggregated_data = group_and_aggregate(filtered_data, 'category', ['total', 'average', 'count'])
    
    # Sort data
    sorted_data = sort_data(aggregated_data, 'total')
    
    # Save and display data
    save_and_display(sorted_data, 'output.csv')

if __name__ == "__main__":
    main()