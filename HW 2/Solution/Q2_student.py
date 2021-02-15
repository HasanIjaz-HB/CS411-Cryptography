import requests

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


API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 24775

endpoint = '{}/{}/{}'.format(API_URL, "q2", my_id )
response = requests.get(endpoint) 	
if response.ok:	
  r = response.json()
  p, q, e, c = r['p'], r['q'], r['e'], r['cipher']    #Use these variables to calculate m
  print(c)
else:  print(response.json())

##SOLUTION
n = p*q
k=gcd(c,n)
phi = (p-1)*(p+1)

d=modinv(e,phi)

result = pow(c,d,n)
print()
print(result)
## END OF SOLUTION


m = result 	#ATTN: change this into the number you calculated and DECODE it into a string m_

m_ = "Change this to the message you found from m by decoding. Yes, it is a meaningful text."


#query result
endpoint = '{}/{}/{}/{}'.format(API_URL, "q2c", my_id, m_ )    #send your answer as a string
response = requests.put(endpoint) 	
print(response.json())
