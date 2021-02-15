import math
import random
import warnings
import sympy

def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


n= 97289040915427312142046186233204893375 
a= 61459853434867593821323745103091100940
b= 22119567361435062372463814709890918083


a_2 = 87467942514366097632147785951765210855 
b_2 = 3291682454206668645932879948693825640  



a_3 = 74945727802091171826938590498744274413 
b_3 = 54949907590247169540755431623509626593  


d= gcd(a,n)
d_2 = gcd (a_2,n)
d_3 = gcd(a_3,n)

print("For a = " + str(a))
print("d = GCD(a,n)= "+ str(d))


if(b%d==0):
    print("yes")
else:
    print("There is no solution since " + str(d) + " doesn't divide b")    
    
print("\n")


print("For a2 = " + str(a_2))
print("d2 = GCD(a2,n) = " + str(d_2))
ainv=modinv(a_2,n)

if(b_2%d_2==0):
    print("There are " +str(d_2) +" number of solutions")
    ainv=modinv(a//d,n//d)
    while d_2 != 0:
        answer= ainv + ((d_2-1)*(n//d_2))
        print("One of the solution is: "+ str(answer))
        d_2 = d_2 - 1
else:
    print("There is no solution since 5 doesn't divide b")
    
print("\n")

	
print("For a3 = " + str(a_3))
print("d3 = GCD(a3,n) = " + str(d_3))

if (d_3==1):
    ainv=modinv(a_3,n)
    answer=(b_3*ainv)%n
    print("There is one solution: " +str(answer))
    print("\n")

