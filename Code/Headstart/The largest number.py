#Smaller or Larger Numbers

a = int(input("Enter 1st number: "))
b = int(input("Enter 2nd number: "))
c = int(input("Enter 3rd number: "))

if a == b == c:
    print("The numbers are all equal")
elif a == b and a != c:
     print(f"The first and second numbers, {a} and {b}, are equal")
     if a > b:
         print(f"And they are greater than the third number, {c}")
     else:
         print(f"But they are are smaller than the third number, {c}")
elif b == c and b != a:
     print(f"The second and third numbers, {b} and {c}, are equal")
     if b > a:
         print(f"And they are greater than the first number, {a}")
     else:
         print(f"But they are are smaller than the first number, {a}")
elif c == a and c != b:
     print(f"The first and third numbers, {a} and {c}, are equal")
     if c > b:
         print(f"And they are greater than the second number, {b}")
     else:
         print(f"But they are are smaller than the second number, {b}")
elif a > b and a > c:
    print(f"The first number, {a}, is the biggest")
elif b > a and b > c:
    print(f"The second number, {b}, is the biggest")
elif c > a and c > b:
    print(f"The third number, {c}, is the biggest")