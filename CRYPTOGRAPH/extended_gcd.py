#GCD Extended version
#a⋅u+b⋅v = gcd(a,b)
#output : gcd(a,b), u, v
def x_gcd(a, b):
    #same way with gcd work but with additional feature
    if b == 0:
        return  a,1,0 #return value of gcd(a,b), x1, y1 
    else:
        extended_gcd, x1, y1 = x_gcd(b, a % b)
        #assign x as the base case first of 0(y1 when b == 0) and update as code backtrack
        x = y1
        # assign y with 1 as the base case then continue with backtrack
        y = x1 - (a // b)*y1
        return extended_gcd, x, y #return the gcd, u, v as list

a = int(input("inster a: "))
b = int(input("inster b: "))

print(x_gcd(a,b))


