import random

#Kiterjesztett euklideszi
def ExtendedEuclid(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    while (b != 0):
        q = a // b
        a, b = b, a%b  #Itt egyszerre írom felül a kettőt különben nem lesz jó
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0


#Gyorshatványozás algoritmus
def powerMod(b, e, m):
    x = 1
    while (e > 0):
        if (e % 2 == 1):
            x = (b * x) % m
        b = (b*b) % m
        e = e // 2
    return x

#Miller-Rabin prímteszt
def millerrabin(n, a):
    d = n-1
    s = 0
    while (d % 2 == 0):
        d = d//2
        s = s + 1
    t = powerMod(a, d, n) #gyorshatványozás
    if (t == 1):
        return "Probably prime"
    while (s > 0):
        if (t == n-1 or t == 1):
            return "Probably prime"
        t = (t * t) % n
        if (t == n -1):
            return "Probably prime"
        return "Composite"


#Prímteszt alap nélkül
def isPrime(n):
    if (n == 3 or n == 2):
        return "Probably prime"
    if (n%2 == 0):
        return "Composite"

    #Ha akármelyikre Composite jön ki akkor nem lehet prím már.
    for i in range(n):
        a = random.randint(2, n-2)
    if millerrabin(n, a) == "Composite":
        return "Composite"
    return "Probably prime"

#kínai maradéktétel
def crt(c, d, p, q):
    c1 = powerMod(c, d % (p - 1), p)
    c2 = powerMod(c, d % (q - 1), q)
    M = p * q
    M1 = M//p
    M2 = M//q

    gcd, y1, y2 = ExtendedEuclid(M1, M2)
    m = (c1 * M1 * y1 + c2 * M2 * y2) % M
    return m


#prímszám generáló
def random_prime(min, max):
        while True:
            p = random.randint(min, max)
            if isPrime(p) == "Probably prime":
                return p


#Legnagyobb közös osztó
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


#Kulcsgenerálás
def rsakey():

    p = random_prime(5, 265)
    q = random_prime(5, 265)

    n = p*q
    fi=(p-1)*(q-1)

    e = 0
    for e in range(2, fi):
        if gcd(e, fi) == 1: #hogy biztosan relatív prímek legyenek
            break
    _, d, _ = ExtendedEuclid(e, fi)
    d = d % fi
    return e, d, n, p, q


#m^3 mod n
def encrypt(m, e, n):
    return (powerMod(m, e, n))

#c^d mod n
def decrypt(c, d, p, q):
    return crt(c, d, p, q)

#Igaz-e, hogy s = m^d mod n
def sign(m, d, n):
    return powerMod(m, d, n)

#s^e mod n
def verify(s, e, n, o):
    vmessage = powerMod(s, e, n)
    if vmessage == o:
        return "Megegyezik az eredetivel"
    else:
        return "Nem egyezik meg az eredetivel"



if __name__ == "__main__":
    e, d, n, p, q = rsakey()
    print(f"Nyilvános kulcs: {e}")
    print(f"Titkos kulcs: {d}")
    print(f"p = {p}, q = {q}")
    print(f"Modulus: {n}")

    m = 113
    titkositott = encrypt(m, e, n)
    visszafejtett = decrypt(encrypt(m, e, n), d, p, q)
    alairas = sign(m, d, n)
    ellenorzes = verify(alairas, e, n, m)
    print(f"Eredeti üzenet: {m}" )
    print("Titkosított üzenet: ", titkositott)
    print("Visszafejtett üzenet: ", visszafejtett)


    print("Aláírás: ", alairas)
    print("Ellenőrzés: ", ellenorzes)




