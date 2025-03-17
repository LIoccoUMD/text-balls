import time
import numpy as np
now = time.localtime
HELLO = 12
print(f"time is: {now}")
# This is a comment to explain the code
def calculate_sum(a, b):
    num1 = 42          # Integer variable
    num2 = 3.14        # Float variable
    text = "Hello"     # String variable
    if a > b:
        return num1 + num2  # Keyword 'return'
    else:
        print(text)    # Function call
        return a + b

# Call the function with some values
n = 24
result = calculate_sum(10, 5)
print("Result is: " + str(result))

print(np.linspace(0, 2 * np.pi,n))

