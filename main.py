import logging
import os
import random
import re
import statistics
from collections import Counter

import psycopg2
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


def read_html_file(path_to_html_file):
    with open(path_to_html_file, 'r') as f:
        html = f.read()
    return html


def extract_colours(html_content):
    colours = re.findall(r'\b(GREEN|YELLOW|BROWN|BLUE|PINK|ORANGE|CREAM|RED|WHITE|ARSH|BLEW|BLACK)\b', html_content)
    colours = [colour for colour in colours if
               colour not in ['DAY', 'COLOURS', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']]
    return colours


def get_mean_colour(colours):
    colour_count = Counter(colours)
    colour_frequency = sum(colour_count.values()) / len(colour_count)
    mean_colour = min(colour_count, key=lambda x: abs(colour_count[x] - colour_frequency))
    return mean_colour


def get_most_worn(colours):
    colour_count = Counter(colours)
    print(colour_count)
    most_worn = colour_count.most_common(1)[0][0]
    return most_worn


def get_median_colour(colours):
    sorted_colours = sorted(colours)
    print(sorted_colours)
    median_colour = sorted_colours[len(sorted_colours) // 2]
    return median_colour


def get_variance(colours):
    colour_count = Counter(colours)
    colour_frequencies = list(colour_count.values())
    print(colour_frequencies)
    variance = statistics.variance(colour_frequencies)
    return variance


def get_colour_probability(colours, colour):
    colour = colour.upper()
    colour_count = Counter(colours)
    x_colour_count = colour_count[colour]
    total_colours = len(colours)
    colour_probability = x_colour_count / total_colours
    return f"{colour_probability:.4f}"


def save_to_postgresql(colours):
    colour_count = Counter(colours)
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
        )
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS colour_frequencies (colour VARCHAR(50) PRIMARY KEY, frequency 
        INTEGER)""")
        for colour, frequency in colour_count.items():
            cur.execute("INSERT INTO colour_frequencies (colour, frequency) VALUES (%s, %s) ON CONFLICT (colour) DO "
                        "UPDATE SET frequency = excluded.frequency", (colour, frequency))
        conn.commit()
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()


def recursive_search(lis, size, key):
    if size == 0:
        return False
    if lis[size - 1] == key:
        return lis[size - 1]
    return recursive_search(lis, size - 1, key)


def convert_to_decimal():
    binary = ''.join(random.choice('01') for _ in range(4))
    decimal = int(binary, 2)
    return decimal


def fibonacci_sum(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return sum(fib[:n])


HTML_FILE_PATH = 'python_class_question.html'

html_content = read_html_file(HTML_FILE_PATH)

colours = extract_colours(html_content)

# 1. Which color of shirt is the mean color?
mean_colour = get_mean_colour(colours)
logger.info(f"1. Mean color: {mean_colour}")

# 2. Which color is mostly worn throughout the week?
most_worn = get_most_worn(colours)
logger.info(f"2. Most worn: {most_worn}")

# 3. Which color is the median?
median_colour = get_median_colour(colours)
logger.info(f"3. Median: {median_colour}")

# 4. BONUS Get the variance of the colors
variance = get_variance(colours)
logger.info(f"4. Variance: {variance}")

# 5. BONUS if a colour is chosen at random, what is the probability that the color is red?
colour_probability = get_colour_probability(colours, 'RED')
logger.info(f"5. Probability of RED: {colour_probability}")

# 6. Save the colours and their frequencies in postgresql database
save_to_postgresql(colours)
logger.info(f"6. Colours and their frequencies are saved to PostgreSQL")

# 7. BONUS write a recursive searching algorithm to search for a number entered by user in a list of numbers.
decimal = convert_to_decimal()
logger.info(f"7. Decimal: {decimal}")

# 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
search = recursive_search([1, 2, 3, 4, 5], 5, 3)
logger.info(f"8. Search: {search}")

# 9. Write a program to sum the first 50 fibonacci sequence.
sum_of_fibonacci = fibonacci_sum(50)
logger.info(f"9. Sum of Fibonacci: {sum_of_fibonacci}")
