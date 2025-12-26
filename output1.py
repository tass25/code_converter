import pandas as pd

# Load data from a CSV file
def load_data(file_name):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_name)
        return data
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None

# Filter data to include only rows where age exceeds a certain threshold
def filter_data(data, age_threshold):
    """Filter data to include only rows where age exceeds a certain threshold."""
    filtered_data = data[data['age'] > age_threshold]
    return filtered_data

# Group data by a categorical column and calculate aggregate statistics
def aggregate_data(data, group_by_column):
    """Group data by a categorical column and calculate aggregate statistics."""
    aggregated_data = data.groupby(group_by_column).agg({
        'amount': ['sum', 'mean', 'count']
    })
    aggregated_data.columns = ['total', 'average', 'count']
    return aggregated_data

# Sort results in descending order by a specific column
def sort_data(data, sort_column):
    """Sort results in descending order by a specific column."""
    sorted_data = data.sort_values(by=sort_column, ascending=False)
    return sorted_data

# Save results to a CSV file
def save_data(data, file_name):
    """Save results to a CSV file."""
    data.to_csv(file_name)

# Display results
def display_data(data):
    """Display results."""
    print(data)

# Main function
def main():
    # Load data
    data = load_data('data.csv')
    
    if data is not None:
        # Filter data
        filtered_data = filter_data(data, 18)
        
        # Aggregate data
        aggregated_data = aggregate_data(filtered_data, 'category')
        
        # Sort data
        sorted_data = sort_data(aggregated_data, 'total')
        
        # Save data
        save_data(sorted_data, 'output.csv')
        
        # Display data
        display_data(sorted_data)

if __name__ == "__main__":
    main()