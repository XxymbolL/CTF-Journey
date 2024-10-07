def gcd(a, b):
#looping until b hit 0 and return a
    while b != 0:
        #create a temp so we can create new b and re assign a with b
        temp = b
        b = a % b
        a = temp
    return a

a = int(input("input a: "))
b = int(input("input a: "))
print(gcd(a,b))

