import subprocess
import concurrent.futures
import numpy as np
import hashlib

# Define the range of numbers
start_number = 7105647338419064407
end_number = 74611294676837538538

# Specify the base string for hashing
base_string = "03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852"

# Generate an array of numbers in the specified range
numbers = np.arange(start_number, end_number + 1)

def execute_keymath(number):
    # Concatenate the base string with the current number and hash it using SHA256
    input_str = f"{base_string}-{number:020d}"
    hashed_result = hashlib.sha256(input_str.encode()).hexdigest()
    
    # Check if the result starts with "02145"
    if hashed_result.startswith("02145"):
        print(f"Number: {number}\tResult: {hashed_result}")
        return number, f"Result: {hashed_result}"

# Set the number of worker processes (adjust as needed)
num_workers = 4

# Use ProcessPoolExecutor for parallel execution
with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
    # Submit tasks for execution
    results = list(executor.map(execute_keymath, numbers))

# Filter results based on the condition
filtered_results = [(number, result) for number, result in results if result is not None]

# Create a matrix with numbers and corresponding results
result_matrix = np.array(filtered_results, dtype=object)

# Save the NumPy array to a text file
np.savetxt("meme_matrix_parallel_sha256.txt", result_matrix, delimiter='\t', fmt='%s')

print("Task completed. Results saved in meme_matrix_parallel_sha256.txt.")
