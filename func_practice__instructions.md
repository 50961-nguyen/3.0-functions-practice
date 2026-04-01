## Setup
- create func_practice.py in your Practice Folder, under Unit 2

## Instructions

Your job is to determine whether a user inputted number is prime or not. Here is how you will do that.

1. Create a function called `evenly_divides(a: int, b: int) -> bool` that returns true if `a` evenly divides `b`. For example 6 evenly divides 36, but 4 does not evenly divide 2 (make sure that sentence makes sense) **HINT** Use the `%` operator.
2. Create a function called `is_prime(n: int) -> bool` that determines if the number is prime. To do so, follow the pseudo code below

```plaintext
function is_prime(n: integer) -> boolean
    if n is 1, then return False  # One is not prime

    for every number from 2 up to, but not including n
        if the number evenly divides n
            return False  # This means that n cannot be prime
    
    return True  # This means we've tried to divide every number between 2-n by n and nothing went in evenly, therefore n is prime.
```
3. Create a main function that asks the user to input a value.
    * if the user inputs a prime, print: f"{number} is prime"
    * if the user inputs a composite number, print: f"{number} is not prime"
    * Don't forget to include IPO comments in main() and the docstring in your functions

### Starter code
```python
"""
HEADER COMMENTS
"""

def evenly_divides(a: int, b: int) -> bool:
    """
    TODO: write the docstring
    """


def is_prime(n: int) -> bool:
    """
    TODO: write the docstring
    """


def main():
    """
    The main program that asks the user to input a number and checks if it is prime or composite. 
    """
    pass  # Remove this line once you write your program. This is only here so there is no error.


if __name__ == "__main__":
    main()
```
