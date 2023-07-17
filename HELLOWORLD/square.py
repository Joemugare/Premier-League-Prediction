def get_square(number):
    square = number ** 2
    return square

# Example usage
input_number = float(input("Enter a number: "))
result = get_square(input_number)
print(f"The square of {input_number} is {result}.")
