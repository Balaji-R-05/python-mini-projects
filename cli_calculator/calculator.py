from mathematics import *

def main():
    try:
        num1 = float(input("Enter num1: "))
        num2 = float(input("Enter num2: "))
        op = input("Enter operation (+, -, *, /, %, **): ").strip()
        operations = {
            "+": add,
            "-": sub,
            "*": multiply,
            "/": divide,
            "%": mod,
            "**": exponention
        }

        if op in operations:
            if (op == "/" or op == "%") and num2 == 0:
                raise ZeroDivisionError("Denominator cannot be zero!")
            result = operations[op](num1, num2)
            print(f"{num1} {op} {num2} = {result:.4f}")
        else:
            print("Enter valid operation !!!")

    except ValueError:
        print("Invalid input! Please enter numeric values only.")

    except ZeroDivisionError as e:
        print(e)



if __name__ ==  "__main__":
    while True:
        main()
        if input("Do you want to continue? (y/n): ").lower() == 'n':
            break
        print("--------------------------------")