# НОД - GCD Task

# GCD
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


a = 66528
b = 52920
print("crypto{"+str(gcd(a, b))+"}")
