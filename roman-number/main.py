# Roman Numeral Converter

def roman_to_int(numeral):
  final_answer = 0

  if "CM" in numeral:
    final_answer += 900
    numeral = numeral.replace("CM", "")
  if "CD" in numeral:
    final_answer += 400
    numeral = numeral.replace("CD", "")
  if "XC" in numeral:
    final_answer += 90
    numeral = numeral.replace("XC", "")
  if "XL" in numeral:
    final_answer += 40
    numeral = numeral.replace("XL", "")
  if "IX" in numeral:
    final_answer += 9
    numeral = numeral.replace("IX", "")
  if "IV" in numeral:
    final_answer += 4
    numeral = numeral.replace("IV", "")

  for i in numeral:
    if i == "M":
      final_answer += 1000
    elif i == "D":
      final_answer += 500
    elif i == "C":
      final_answer += 100
    elif i == "L":
      final_answer += 50
    elif i == "X":
      final_answer += 10
    elif i == "V":
      final_answer += 5
    elif i == "I":
      final_answer += 1

  print("The roman numerals you entered translates to: " + str(final_answer) + "!")

if __name__ == "__main__":
    print("Welcome to the roman numeral converter!")
    print("This program will convert roman numerals to integers.")
    print("The roman numerals you can enter are: M, D, C, L, X, V, I")

    roman_int = input("Enter the roman numerals you want to convert: ").strip().upper()

    while not all(char in "MDCLXVI" for char in roman_int):
        print("Invalid input. Please enter valid roman numerals.")
        roman_int = input("Enter the roman numerals you want to convert: ").strip().upper()
        
    roman_to_int(roman_int)