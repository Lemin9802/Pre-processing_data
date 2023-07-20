# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set figure size
plt.rcParams['figure.dpi'] = 100

# Load dataset
dataset = pd.read_csv("C:/Users/ADMIN/Downloads/E-commerce_Dataset.csv")

# Define function to print dataset info
def dataset_info(df):
    print(f"Dataset Info:\nNumber of rows: {df.shape[0]}\nNumber of columns: {df.shape[1]}")
    categorical_columns = 0
    numerical_columns = 0
    for column in df.columns:
        if df[column].dtype == 'object' or df[column].nunique() <= 10:
            categorical_columns += 1
        else:
            numerical_columns += 1
    print(f"Numerical columns: {numerical_columns}")
    print(f"Categorical columns: {categorical_columns}")

# Define function to print dataset
print_dataset = lambda df: print("\nDataset:\n", df)

# Define function to print dataset details using pandas info() function
def print_dataset_details(df):
    print("\033[1m" + "\n.: Dataset Details :." + "\033[0m")
    print("\033[36m*" * 22 + "\033[0m")
    df.info(memory_usage=False)

def print_all_column_values(df):
    for column in df.columns:
        print("\033[36m*" * 29)
        print("\033[1m" + f"\n.: {column} Values :." + "\033[0m")
        print("\033[36m*" * 29 + "\033[0m")
        if df[column].dtype == 'object' or df[column].nunique() <= 10:
            print("\033[1mCategorical:\033[0m")
            print(df[column].value_counts(dropna=False))
            print()
            print("\033[1mNull Values:\033[0m")
            print(df[column].isnull().sum())  # Print the number of null values for categorical columns
            print()
        else:
            print("\033[1mNumerical:\033[0m")
            print(df[column])
            print()
            print("\033[1mNull Values:\033[0m")
            print(df[column].isnull().sum())  # Print the number of null values for numerical columns
            print()

# Perform tasks
dataset_info(dataset)
print_dataset(dataset)
print_dataset_details(dataset)
print_all_column_values(dataset)

# Check for null values in dataset
print(f"Number of null values in each column:\n{dataset.isnull().sum()}")

# Count null and non-null values in each column
null_values = dataset.isnull().sum()
non_null_values = dataset.notnull().sum()

# Get column names from dataset
columns = dataset.columns

# Create a list to store columns with null values before processing
columns_with_null_before = []

# Check for null values in dataset and store columns with null values in the list
for column in dataset.columns:
    if null_values[column] > 0:
        columns_with_null_before.append(column)

# Loop through each column and plot horizontal bar chart for columns with null values
for column in dataset.columns:
    if null_values[column] > 0:
        value_counts = dataset[column].value_counts(dropna=False)
        labels = value_counts.index.astype(str)
        sizes = value_counts.values
        plt.figure(figsize=(8, 6))
        plt.barh(labels, sizes, color=plt.cm.Set3.colors)
        plt.xlabel('Count')
        plt.ylabel('Values')
        plt.title(f'Distribution of Values in Column "{column}" (Horizontal Bar Chart)')

        # Add count text on each bar
        for index, value in enumerate(sizes):
            plt.text(value, index, str(value), ha='left', va='center', color='black', fontweight='bold')

        plt.tight_layout()
        plt.show()

# Create a list to store columns that have been processed
columns_processed = []

# Create figure and axes for bar chart showing null and non-null values before processing
fig, ax1 = plt.subplots(figsize=(10, 6))

# Set bar chart data for non-null values (before processing)
bar_width = 0.4
bar_positions = np.arange(len(non_null_values))
ax1.barh(bar_positions, non_null_values, height=bar_width, color='gray', label='Non-null Values (Before)')

# Set axes labels and title for bar chart
ax1.set_xlabel('Number of Values')
ax1.set_ylabel('Columns')
plt.title('Number of Null and Non-null Values Before Data Processing')

# Set y-axis ticks and labels for bar chart
ax1.set_yticks(bar_positions)
ax1.set_yticklabels(non_null_values.index)

# Create figure and axes for line chart showing null values before processing
ax2 = ax1.twiny()
ax2.plot(null_values, bar_positions, marker='o', color='red', label='Null Values (Before)', linestyle='--')

# Set axes labels for line chart
ax2.set_xlabel('Number of Null Values')

# Set y-axis tick positions and labels for line chart
ax2.set_yticks(bar_positions)
ax2.set_yticklabels(non_null_values.index)

# Show the plot
plt.tight_layout()
plt.show()

# Replace null values with column mean or last value
processed_columns = []
for column in dataset.columns:
    if null_values[column] > 0:
        if dataset[column].dtype != 'object':
            dataset[column].fillna(dataset[column].mean(), inplace=True)
            if column == 'Discount':
                dataset[column] = dataset[column].round(1)  # Round to 1 decimal places for 'Discount' column
            else:
                dataset[column] = dataset[column].astype(int)  # Convert other columns to integers
        else:
            dataset[column].fillna(method='ffill', inplace=True)
        processed_columns.append(column)


# Save processed dataset to file
dataset.to_csv("C:/Assignment/E-commerce_Dataset_Processed.csv", index=False)

# Define function to print column values for processed columns
def print_processed_column_values(df):
    for column in df.columns:
        if column in processed_columns:
            print("\033[36m*" * 29)
            print("\033[1m" + f".: {column} Values :." + "\033[0m")
            print("\033[36m*" * 29 + "\033[0m")
            print(df[column].value_counts(dropna=False))
            print(f"Number of null values: {df[column].isnull().sum()}")  # Print the number of null values

# Display the processed columns
print("Processed Columns:")
print_processed_column_values(dataset)

# Check for processed null values in dataset
print(f"Number of processed null values in each column:\n{dataset.isnull().sum()}")

# Get the updated null values and non-null values
null_values = dataset.isnull().sum()
non_null_values = dataset.notnull().sum()

# Create figure and axes for bar chart showing null and non-null values after processing
fig, ax1 = plt.subplots(figsize=(10, 6))

# Set bar chart data for non-null values (after processing)
bar_width = 0.4
bar_positions = np.arange(len(non_null_values))
ax1.barh(bar_positions, non_null_values, height=bar_width, color='gray', label='Non-null Values (After)')

# Set axes labels and title for bar chart
ax1.set_xlabel('Number of Values')
ax1.set_ylabel('Columns')
plt.title('Number of Null and Non-null Values After Data Processing')

# Set y-axis ticks and labels for bar chart
ax1.set_yticks(bar_positions)
ax1.set_yticklabels(non_null_values.index)

# Create figure and axes for line chart showing null values after processing
ax2 = ax1.twiny()
ax2.plot(null_values, bar_positions, marker='o', color='red', label='Null Values (After)', linestyle='--')

# Set axes labels for line chart
ax2.set_xlabel('Number of Null Values')

# Set y-axis tick positions and labels for line chart
ax2.set_yticks(bar_positions)
ax2.set_yticklabels(non_null_values.index)

# Show the plot
plt.tight_layout()
plt.show()

# Loop through each processed column and plot horizontal bar chart
for column in processed_columns:
    value_counts = dataset[column].value_counts(dropna=False)
    labels = value_counts.index.astype(str)
    sizes = value_counts.values

    # Create figure and axes for bar chart
    fig, ax = plt.subplots(figsize=(8, 6))

    # Set bar chart data
    ax.barh(labels, sizes, color=plt.cm.Set3.colors)
    ax.set_xlabel('Count')
    ax.set_ylabel('Values')
    ax.set_title(f'Distribution of Values in Processed Column "{column}" (Horizontal Bar Chart)')

    # Add count text on each bar
    for index, value in enumerate(sizes):
        ax.text(value, index, str(value), ha='left', va='center', color='black', fontweight='bold')

    plt.tight_layout()
    plt.show()
