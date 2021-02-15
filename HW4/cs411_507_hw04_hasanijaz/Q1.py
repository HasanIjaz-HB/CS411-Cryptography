import random
import requests

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 24775   ## Change this to your ID

endpoint = '{}/{}/{}'.format(API_URL, "RSA_Oracle", my_id )
response = requests.get(endpoint) 	
c, N, e = 0,0,0 
if response.ok:	
  res = response.json()
  print(res)
  c, N, e = res['c'], res['N'], res['e']    #get c, N, e
else: print(response.json())

######

#c = 25216623858801485236571698003874600328148053922872438945090650640363988910771308628360266209288475652003739423439782037354548646343719236451455899161281548233346036402879251005292304046237195505832912298025363157324109904991452527201628773420708785984836909199428963614665140211123858150769137727343876306020307566420916019740890561405835098947328623548248449055658191531702786283545733517272553300992386396267554293988521208538585979245922611837611295000509664290096109944101744189374882051086532977704755024279189796052861275791711501395226940741495880682227594671956875637266107690170923546486270791705989322181219
#N = 26570927162480737628985979203754072331946194492775210615224297972011744173941901816424061641629410774614008488685919271530391604171337234198111376684967784318130245430521386636931825815033716005580574144536158735220817017331513776598639232191685378945108934070246971078593116594187093852985690509208868473031905575752098253618707363954507549299255829726753255010984781668655145200872618181467368237195042352624541163587556719474038165282251445151777510755393767011091201655442513743652421000131775919984218048130718796389532361194191968866028104038025606263666775683757562416321168778465969563785651946597616485652527
#e = 65537
x = random.randint(pow(2, 64, N),pow(2, 128, N))
print(x)
cprime=(c * pow(x,e,N)) % N
print("c_ is:", cprime)
#c_=cprime.to_bytes((cprime.bit_length()+7)//8, byteorder='big')


###### Query Oracle it will return corresponding plaintext
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_query", my_id, cprime)
response = requests.get(endpoint) 	
if(response.ok): m_ = (response.json()['m_'])
else:print(response)

####
# this part works if we get m_ from the above
print("m_ is :",m_)

m = (m_ * modinv(x,N)) % N
print("m is: ", m)
m_decrypt= m.to_bytes((m.bit_length()+7)//8, byteorder='big')
print("The message is:",m_decrypt)
res = m_decrypt


###Send your answer to the server.
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_checker", my_id, res)
response = requests.put(endpoint)
print(response.json())