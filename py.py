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
ri=d/2
A1 = 2*math.pi*ro


#propertties of metal
#0 is 600 and 1 is 650
def get_km(T):
    if(T==0):
        return 26.69
    elif(T==1):
        return 26.53
#Properties of oxide
def get_kox(T):
    if(T==0):
        return 0.84
    elif(T==1):
        return 0.875

# properties of steam
def get_μs(T):
    if(T==0):
        return 34.55 *(10**-6)
    elif(T==1):
        return 36.44*(10**-6)
def get_ks(T):
    if(T==0):
        return 102.1*(10**-3)
    elif(T==1):
        return 106.4*(10**-3)
def get_cs(T):
    if(T==0):
        return 2967.9
    elif(T==1):
        return 2816.8

#Properties of flue gas
#0 is 800 and 1 is 900 2 is 1000
def get_μg(T):
    if(T==0):
        return 0.04283
    elif(T==1):
        return 0.04524
    elif(T==2):
        return 0.04755
def get_kg(T):
    if(T==0):
        return 0.06993
    elif(T==1):
        return 0.07468
    elif(T==2):
        return 0.07911
def get_cg(T):
    if(T==0):
        return 1222
    elif(T==1):
        return 1242
    elif(T==2):
        return 1259

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

# calculate length
def get_l(delta):
    rn=ri+(delta)
    return ro-rn

# calculate lengeth2
def get_l2(delta):
    rn=ri+(delta*2)
    return ro-rn

# calculate the area of the oxide
def getA2(delta):
    return 2*math.pi*(ri-delta)

# calculate steam convective heat transfer coefficient
def get_hs(ks,cs,μs,delta):
    res=(4*ms)/(3600*math.pi*(d-(2*delta))*μs)
    prs=(μs*cs)/ks
    return 0.023*(ks/(d-(2*delta)))*((res)**0.8)*(prs)**0.4

# calculate flue gas convective heat transfer coefficient
def get_hg(kg,cg,μg,delta):
    reg = (D*mg)/(3600*Nw*H*(St-D)*μg)
    prg = (μg*cg)/kg
    return 0.33*12*(kg/D)*((reg)**0.6)*(prg)**0.33

# calculate initial average tempreture
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

def getAvgTemp(km,kox,hg,hs,tg,ts,delta):
    matrix1 = np.array([
        [(km*A1/get_l(delta))+(hg*A1),-1*km*A1/get_l(delta),0],
        [-1*km*A1/get_l(delta),(km*A1/get_l(delta)+(kox*getA2(delta)/get_l2(delta))),-1*(kox*getA2(delta)/get_l2(delta))],
        [0,-1*(kox*getA2(delta)/get_l2(delta)),(kox*getA2(delta)/get_l2(delta))+(hs*getA2(delta))],
    ])
    # matrix1Inv = np.linalg.inv(matrix1)
    matrix2 = np.array([
        [hg*tg*A1],
        [0],
        [hs*ts*getA2(delta)],
    ])
    resultMatrix = np.linalg.solve(matrix1,matrix2)
    return  (resultMatrix[1][0]+resultMatrix[2][0])/2

print(getIntitalAvgTemp(26.69, get_hg(0.06993, 1222, 0.04283, 0), get_hs(0.1021, 2967.9,34.55*(10**-6) , 0), 800, 600))

# calculate delta by using tavg in meter
def getDelta(T_Avg,tFrom, tTo):
    pFrom = (T_Avg+273.15)*(20+math.log(tFrom))    
    pTo = (T_Avg+273.15)*(20+math.log(tTo))
    X_FROM = math.pow(math.e, 0.000564*pFrom-9.934);
    X_TO = math.pow(math.e, 0.000564*pTo-9.934);
    return ((X_TO-X_FROM)/2)*(10**-6) #converted to meter

# main iteration
def calc(μs,ks,cs,μg,kg,cg,km,kox,ts,tg):
    delta = 0
    for timeIndex in range (100):
        if(timeIndex==0):
            print("Initial")
            hg=get_hg(kg, cg, μg, delta)
            hs=get_hs(ks, cs, μs, delta)
            T_Avg = getIntitalAvgTemp(km, hg, hs, tg, ts)
            delta = getDelta(T_Avg, 1, 10)
            print(T_Avg)
        else:
            hg=get_hg(kg, cg, μg, delta)
            hs=get_hs(ks, cs, μs, delta)
            T_Avg = getAvgTemp(km, kox, hg, hs, tg, ts, delta)
            delta = getDelta(T_Avg, (timeIndex*10), ((timeIndex+1)*10))
            print(T_Avg)



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
        print("Ts=",ts,"      Tg=",tg)
        print("","μs=",μs, "ks=", ks, "cs=",cs, "μg=",μg, "kg=",kg, "cg=",cg, "km=",km, "kox=",kox, ts, tg)
        print("----------------------------------------------------------\n")
        calc(μs, ks, cs, μg, kg, cg, km, kox, ts, tg)
        