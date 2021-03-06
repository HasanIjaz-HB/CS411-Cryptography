# use "pip install sympy" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import random
import sympy
import warnings
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

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
    
def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p

def Param_Generator(qsize, psize):
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize-qsize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g

# Generating private-public key pair
def Key_Gen(q, p, g):
    s = random.randint(1, q) # private key
    h = pow(g, s, p)         # public key
    return s, h

# Signature generation
def Sig_Gen(message, a, k, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    r = pow(g, k, p)%q
    s = (modinv(k, q)*(h+a*r))%q
    return r, s

# Signature verification
def Sig_Ver(message, r, s, beta, q, p, g):
    shake = SHAKE128.new(message)
    h = int.from_bytes(shake.read(q.bit_length()//8), byteorder='big')
    u1 = (modinv(s, q)*h)%q
    u2 = (modinv(s, q)*r)%q
    v1 = (pow(g, u1, p)*pow(beta, u2, p)%p)%q

    if v1 == r:
        return True
    else:
        return False

# Test
print("Testing the DSA signature generation and verification")
# Generate domain parameters (q, p, g)
q, p, g = Param_Generator(224, 2048)
print("q =", q)
print("p =", p)
print("g =", g)

# Generate private-public key pairs for a user
a, beta = Key_Gen(q, p, g)
print("secret key (a):", a)
print("public key (beta):", beta)

message = b'Hello World!'
k = random.randint(0, q-1)
r, s = Sig_Gen(message, a, k, q, p, g)

if Sig_Ver(message, r, s, beta, q, p, g):
    print("signature verifies:) ")
else:
    print("invalid signature:( ")    


#Q4

q = 18462870797958734358460540315802311963744999954506807981508498635091
p = 21844102112122237484058484990223222527816981702828279171498143036582716271485474028380542696862193720852272618397503658771128114568430034544311836848132556591324273117839115478343051538427437664722980830771161939139222964707695276957432968033365352302080366315415735532111302710857807281798249043320899027800135122873123243743524724602070457967657285884563858968187732680723369906222214201250288443824722261682828970158731587663585174032887767988219143996717380923998096794060064023264584949115354715211375168860544716843940259887168163262505413440632980952366656691935232538721726450037087263854935179798694999345517
g = 13843079639351340920273184714590884400432847093058770970775133079628015343474638985949514224469231316509301786191837239734743524804707156837615319355419215945094865320399756037490734275197507243978890158231379210099367755690209217652326933425758170008835084657241675545571324146202714002127571892258435472678396358353938476569410849475658691697420643000086724156167275855286708191941521213998074404126295230559090196852525498568126029906179168789585152438330622252753643553805877257623433974639379577436808678860489830511416186993204671106346196262903362008285485594747047950971109814842643611103016670841253194356243

#public key - beta 
key = 6187481213658176498787124123601684091780046690985227386674127034254039365850646655310542241724937514112519192485497669738105144173607992347626869972509174309127140941080651743898030456747633487761927322752193676176314211884662768871783260572354989592156755352437101758031330846064492530779348477298394716501400849788380847680039744807953192006233069850428367974025006391433578254859633968702925514987402010031888483663325943692618870576893826021018783543580318493456251127341437691102522482919743872855098214539426447960934626890138798345418250945885432084267499991534185991486840567366979305573275554091497155603826

msg1 = b"He who laugh last didn't get the joke"
r = 6164572993148268278544315246158794966061243456603081427389792698784
s1 = 2412874836775368230194957659405258449579579568340501217618177629780

msg2 = b"Ask me no questions, and I'll tell you no lies"
r = 6164572993148268278544315246158794966061243456603081427389792698784
s2 = 343379365128270720539597367095485301128970178274104846189598795161

h1 = pow(g, s1, p)  # taken from KeyGen function
h2 = pow(g, s2, p)

first_part_of_the_equation = (s1*h2) - (s2*h1)
x=s2-s1
second_part_of_the_equation = modinv(r*x,q)

print(first_part_of_the_equation)
print(second_part_of_the_equation)


alfa = (first_part_of_the_equation * second_part_of_the_equation) % q
print("Alfa is " + str(alfa))

if Sig_Ver(msg1, r, s1, key, q, p, g): # checking if signature verifies for message1
    print("signature verifies:) ")
else:
    print("invalid signature:( ")

if Sig_Ver(msg2, r, s2, key, q, p, g): # checking if signature verifies for message2
    print("signature verifies:) ")
else:
    print("invalid signature:( ")

