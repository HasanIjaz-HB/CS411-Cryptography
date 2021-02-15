import random
import requests
import BitVector as bit

API_URL = 'http://cryptlygos.pythonanywhere.com'	#DON'T CHANGE THIS
my_id = 24775   									#ATTN: Change this into your id number

endpoint = '{}/{}/{}'.format(API_URL, "poly", my_id )
response = requests.get(endpoint) 	
a = 0
b = 0
if response.ok:	
  res = response.json()
  print(res)
  a, b = res['a'], res['b']		#Binary polynomials a and b
else:
  print(response.json())

##SOLUTION  
#You need to calculate c and a_inv
#c = a(x)*b(x)
#a_inv is inverse of a

print("****************")
a = bit.BitVector(bitstring = a)
b = bit.BitVector(bitstring = b)
c = a.gf_multiply(b)

n=8
md = bit.BitVector(bitstring = '100011011')

quo,rmndr = c.gf_divide_by_modulus(md, n)

print("Answer of part a ")
print("C(x) is: ",rmndr)
print("****************")
c = str(rmndr)
		

inv_a = a.gf_MI(md, n)

if inv_a is not None:
    print("Answer of part b ")
    print("a_inv is: ",inv_a)
    print("****************")
else:
    print("No inverse exists")

a_inv = inv_a	

##END OF SOLUTION
 

#check result of part a
endpoint = '{}/{}/{}/{}'.format(API_URL, "mult", my_id, c)
response = requests.put(endpoint) 	
print(response.json())

#check result of part b
endpoint = '{}/{}/{}/{}'.format(API_URL, "inv", my_id, a_inv)
response = requests.put(endpoint) 	
print(response.json())
