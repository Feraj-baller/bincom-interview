import re
import random
import psycopg2
from collections import Counter


#I PUT COMMENTS IN PLACE TO ENSURE READABILITY
# Extract color data from the HTML table
def extract_colors():
    # Color data from the HTML table
    color_data = {
        "MONDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
        "TUESDAY": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
        "WEDNESDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
        "THURSDAY": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
        "FRIDAY": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
    }
    
    # Combine all colors into a single list
    all_colors = []
    for day, colors in color_data.items():
        day_colors = [color.strip() for color in colors.split(',')]
        all_colors.extend(day_colors)

    # Correct any misspellings (e.g., "BLEW" to "BLUE", "ARSH" might be a typo)
    corrected_colors = []
    for color in all_colors:
        if color == "BLEW":
            corrected_colors.append("BLUE")
        elif color == "ARSH":
            corrected_colors.append("ASH")  
        else:
            corrected_colors.append(color)
    
    return corrected_colors

# 1. Which color of shirt is the mean color?
def get_mean_color(colors):
    # Count frequency of each color
    color_counts = Counter(colors)
    
    # Calculate the mean position
    total_colors = len(colors)
    mean_position = total_colors // 2
    
    # Sort colors by frequency
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1])
    
    # Find the color at the mean position
    cumulative = 0
    for color, count in sorted_colors:
        cumulative += count
        if cumulative >= mean_position:
            return color
    
    return None

# 2. Which color is mostly worn throughout the week?
def get_most_common_color(colors):
    color_counts = Counter(colors)
    most_common = color_counts.most_common(1)
    if most_common:
        return most_common[0][0]
    else:
        return None

# 3. Which color is the median?
def get_median_color(colors):
    # Sort colors alphabetically
    sorted_colors = sorted(colors)
    
    # Find the middle position
    n = len(sorted_colors)
    middle = n // 2
    
    # Return the color at the middle position
    return sorted_colors[middle]

# 4. Get the variance of the colors
def get_color_variance(colors):
    color_counts = Counter(colors)
    frequencies = list(color_counts.values())
    
    # Calculate mean frequency
    mean_freq = sum(frequencies) / len(frequencies)
    
    # Calculate variance
    variance = sum((x - mean_freq) ** 2 for x in frequencies) / len(frequencies)
    return variance

# 5. If a colour is chosen at random, what is the probability that the color is red?
def get_red_probability(colors):
    total_colors = len(colors)
    red_count = colors.count("RED")
    return red_count / total_colors

# 6. Save the colours and their frequencies in postgresql database
def save_to_postgresql(colors):
    try:
        # Count frequencies
        color_counts = Counter(colors)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="your_dbname",
            user="your_username",
            password="your_password",
            host="localhost"
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                color VARCHAR(50) PRIMARY KEY,
                frequency INTEGER
            )
        """)
        
        # Insert data
        for color, frequency in color_counts.items():
            cur.execute(
                "INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = %s",
                (color, frequency, frequency)
            )
        
        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()
        
        return "Data saved to PostgreSQL successfully"
    except Exception as e:
        return f"Database error: {str(e)}"

# 7. Recursive searching algorithm
def recursive_search(arr, target, start=0, end=None):
    if end is None:
        end = len(arr) - 1
    
    # Base case: empty array or invalid indices
    if start > end:
        return -1
    
    # Check middle element
    mid = (start + end) // 2
    
    # If target is found
    if arr[mid] == target:
        return mid
    
    # If target is smaller, search left half
    if arr[mid] > target:
        return recursive_search(arr, target, start, mid - 1)
    
    # If target is larger, search right half
    return recursive_search(arr, target, mid + 1, end)

# 8. Generate random 4 digits of 0s and 1s and convert to base 10
def generate_binary_and_convert():
    # Generate 4 random binary digits
    binary_digits = [random.choice(['0', '1']) for _ in range(4)]
    binary_str = ''.join(binary_digits)
    
    # Convert to base 10
    decimal = int(binary_str, 2)
    
    return binary_str, decimal

# 9. Sum the first 50 Fibonacci numbers
def sum_fibonacci(n=50):
    if n <= 0:
        return 0
    
    # Initialize first two Fibonacci numbers
    fib = [0, 1]

    # The Fibonacci sequence
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return sum(fib[:n+1])

# Main function to run all analyses
def main():
    # Extract colors
    colors = extract_colors()
    
    # 1. Mean color
    mean_color = get_mean_color(colors)
    print(f"1. Mean color: {mean_color}")
    
    # 2. Most common color
    most_common = get_most_common_color(colors)
    print(f"2. Most worn color: {most_common}")
    
    # 3. Median color
    median_color = get_median_color(colors)
    print(f"3. Median color: {median_color}")
    
    # 4. Variance
    variance = get_color_variance(colors)
    print(f"4. Variance of colors: {variance}")
    
    # 5. Probability of red
    red_prob = get_red_probability(colors)
    print(f"5. Probability of red: {red_prob:.4f}")
    
    # 6. Save to PostgreSQL
    # Commented out to avoid actual database operations
    # db_result = save_to_postgresql(colors)
    # print(f"6. {db_result}")
    print("6. Database code is ready but commented out to avoid actual DB operations")
    
    # 7. Recursive search demo
    numbers = sorted([random.randint(1, 100) for _ in range(10)])
    target = random.choice(numbers)
    result = recursive_search(numbers, target)
    print(f"7. Recursive search: Found {target} at index {result} in {numbers}")
    
    # 8. Binary to decimal conversion
    binary, decimal = generate_binary_and_convert()
    print(f"8. Generated binary: {binary}, Decimal: {decimal}")
    
    # 9. Fibonacci sum
    fib_sum = sum_fibonacci()
    print(f"9. Sum of first 50 Fibonacci numbers: {fib_sum}")

main()