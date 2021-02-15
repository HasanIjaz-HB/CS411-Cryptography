
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



#Q5

q = 15141339084211537780798402821468668253233855293250282470707486523729
p = 15459352678170194999059797953835943703769299798522640485949251021230061239872933286596281671875036444766767260825161156339142374953144264667175663093532210016977000296281428180052962512096930034626707240943073909429948568647175489641923947055523690662397275499814011659615933313001220733558180164993086472379325887209418439076036830595968948122463542565488458285559269152814846930461678806155717771594791617514000333739836058367191702301817095873715810768950392576601345434651042282496258898798293897916341315693731763534513871295870117294672305447940132333142894162790759196704240972899412016593006223087871357404969
g = 3800569625008648766049545537807478639158256666453837543156865205157342453175195338293914518318389932512419197022492193267072466754594620461534567362497841710002599111953091344930343994503431071692400525354528547918075410538790275781900267312641988973075426468087022427855954288858299458927808889518984317490141729401786342725042250941182574740334793901912974170222604015177323368814264989835679407076289974855552414398779625521837257916022552980027627057473062644879659632681204107806120144998907991338913266334321160324651484012752441634140243465730939619242515280714356873699965985363402010686851443396200018800199
#public key 
key = 13811718194912887731259973687531659017221233072693758339320677556085961091741512534312991319990988012320895125273138799484930424656328618986338233650799555131896857586001490595604365368085682743275712428137943225119715628405892357306029150574584119785832325605674838801154641895745311161271889436502899846458131900988387777254676157672199525938326470244363881227814557082187788046660952433631553517068095734365024876910709029416850114854064043338879940542901936624969303248595208108795751225387203405395739941042570698164719973037261394764330314120509607344408485820133307388882699955010320183318447065675487861322141

msg1 = b"He who laugh last didn't get the joke"
r1 = 7807207725923213670059456706077357545604668400924354746850607726310
s1 = 10137413521818981860558295844142463248736280669671376607939774420169

msg2 = b"Ask me no questions, and I'll tell you no lies"
r2 = 13601517662990253244919392623006368173804524139680316147330845851641
s2 = 5354638027707905626045156057361096890377811387248394522419069236340

h1 = pow(g, s1, p)
h2 = pow(g, s2, p)


x=4 #coeffcient between k1 and k2 brute force

alfa = (((s1 * h2) - (s2*h1*x)) * modinv((s2 * r1 * x - s1 * r2),q)) % q
print("alfa = " + str(alfa))


if Sig_Ver(msg1, r1, s1, key, q, p, g): #signature verification for message1
    print("signature verifies:) ")
else:
    print("invalid signature:( ")

if Sig_Ver(msg2, r2, s2, key, q, p, g): #signature verification for message2
    print("signature verifies:) ")
else:
    print("invalid signature:( ")
