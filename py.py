import math
import numpy as np

#pure constants
D=0.0508
d=0.0438
L=1
Nw=32
Sl=0.0762
St=0.244
ms=3600
mg=2.34*(10**6)
H=10
ro=D/2
A1 = 2*math.pi*ro


#propertties of metal
#0 is 600 and 1 is 650
def get_km(T):
    if(T==0):
        return 3
    elif(T==1):
        return 4
#Properties of oxide
def get_kox(T):
    if(T==0):
        return 3
    elif(T==1):
        return 4

# properties of steam
def get_μs(T):
    if(T==0):
        return 1
    elif(T==1):
        return 2
def get_ks(T):
    if(T==0):
        return 3
    elif(T==1):
        return 4
def get_cs(T):
    if(T==0):
        return 5
    elif(T==1):
        return 6

#Properties of flue gas
#0 is 800 and 1 is 900 2 is 1000
def get_μg(T):
    if(T==0):
        return 7
    elif(T==1):
        return 8
    elif(T==2):
        return 9
def get_kg(T):
    if(T==0):
        return 10
    elif(T==1):
        return 11
    elif(T==2):
        return 12
def get_cg(T):
    if(T==0):
        return 13
    elif(T==1):
        return 14
    elif(T==2):
        return 15

#get tempretures
def getTs(index):
    if index==0:
        return 600
    elif index==1:
        return 650
def getTg(index):
    if index==0:
        return 800
    elif index==1:
        return 900
    elif index==2:
        return 1000


def get_l(delta):
    rn=d/2+(delta/2)
    return ro-rn


def get_hs(ks,cs,μs,delta):
    res=(4*ms)/(3600*math.pi*(d-(2*delta))*μs)
    prs=(μs*cs)/ks
    return 0.023*(ks/(d-(2*delta)))*((res)**0.8)*(prs)**0.4

def get_hg(kg,cg,μg,delta):
    reg = (D*mg)/(3600*Nw*H*(St-D)*μg)
    prg = (μg*cg)/kg
    return 0.33*12*(kg/D)*((reg)**0.6)*(prg)**0.33

def getIntitalAvgTemp(km,hg,hs,tg,ts):
    matrix1 = np.array([
        [(km*A1/get_l(0))+hg*A1, -1*(km*A1/get_l(0))],
        [-1*(km*A1/get_l(0)), (km*A1/get_l(0))+hs*A1],
    ])
    # matrix1Inv = np.linalg.inv(matrix1)
    matrix2 = np.array([
        [hg*tg*A1],
        [hs*ts*A1],
    ])
    resultMatrix = np.linalg.solve (matrix1,matrix2)
    return  resultMatrix[1][0]

print(getIntitalAvgTemp(26.69, get_hg(0.06993, 1222, 0.04283, 0), get_hs(0.1021, 2967.9,34.55*(10**-6) , 0), 800, 600))


def calc(μs,ks,cs,μg,kg,cg,km,kox,ts,tg):
    print("adf")


for i in range (2):
    μs = get_μs(i)
    ks = get_ks(i)
    cs = get_cs(i)
    km = get_km(i)
    kox = get_kox(i)
    ts = getTs(i)
    for j in range (3):
        μg = get_μg(j)
        kg = get_kg(j)
        cg = get_cg(j)
        tg=getTg(i)
        calc(μs, ks, cs, μg, kg, cg, km, kox, ts, tg)
        