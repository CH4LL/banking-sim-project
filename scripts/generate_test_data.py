import random

def generate_data(num_results=4):
    results = []
    for _ in range(num_results):
        # Generate random integers between 100 and 999
        results.append(random.randint(100, 999))
    return results

if __name__ == "__main__":
    data = generate_data()
    # Print each number on a new line
    # This is how Flask will capture the output
    for number in data:
        print(number)