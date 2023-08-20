#EARIN exercise 2, Andreas Kalavas, Panagiota Chita

import numpy as np
import random


def user_inputs():
    dim = input('Give function dimensionality: ');
    dim = int(dim)
    while dim < 1:
        dim = int(input('Give correct dimensionality (>0): '));
    print('Give matrix A (each row you add press Enter) : ')
    a = [[0 for i in range(dim)] for j in range(dim)]
    i = 0
    while i < dim:
        a[i] = list(map(int, input().split()))
        i += 1
    a = np.array(a)
    b = list(map(int, input("Give d-dimensional vector b: ").split()));
    b = np.array(b)
    c = input('Give constant c: ');
    c = int(c)
    d = int(input('Give the range of searched integers as 𝑑≥1 that for each dimension i, −2^d<xi<2^d: '))
    while d < 1:
        d = int(input('Give correct number d (>0): '));
    psize = int(input('Give population size: '));
    while psize < 1:
        psize = int(input('Give correct population size (>0): '));
    pcr = float(input('Give crossover probability (reccomended >0.8): '))
    while pcr < 0 or pcr > 1:
        pcr = float(input('Give correct crossover probability (in range (0,1)) : '))
    pmu = float(input('Give mutation probability (0.1<reccomended<0.2): '))
    while pmu < 0 or pmu > 1:
        pmu = float(input('Give correct mutation probability (in range(0,1)): '))
    ite = int(input('Give number of iterations: '))
    repl = int(input('Give no of individuals to select to keep in the population, each iteration (rec. ~pop. size/5): '))
    while repl < 0 or repl > psize:
        repl = int(input('Give correct replacement number (in range(0,psize)): '))
    pairs=repl//2
    return dim, a, b, c, d, psize, pcr, pmu, ite, repl, pairs

# Transform our elements from binary to decimal (using the first bit to define the sign of the number)
def ma2vec(m, d):
    x = []
    for i in range(d):
        t = 0
        tt = 0
        if m[i][0] == 0:
            for j in m[i]:
                if tt == 0:
                    tt = 1
                    continue
                t *= 2
                t += j
        else:
            for j in m[i]:
                if tt == 0:
                    tt = 1
                    continue
                t *= 2
                t += j
            t = -t
        x.append(t)
    x = np.array(x)
    return x


# function f(x) = x^TAx + b^Tx + c, also the fitness function
def func(a, b, c, po, d):
    x = ma2vec(po, d)
    temp = np.matmul(x.transpose(), a)
    xax = np.matmul(temp, x)
    bx = np.matmul(b.transpose(), x)
    ans = c + bx + xax
    return ans

def fitvalues(pop):
    val = []
    for i in pop:
        t = func(a, b, c, i, dim)
        val.append(t)
    min=np.min(val)
    max=np.max(val)
    scaval=[]
    for i in range(psize):
        scaval.append((val[i] - min) / (max - min))
    return val,scaval

def roulette_wheel_selection(pop, val, repl, offset):
    psize=len(pop)
    temp = random.choices(np.arange(0, psize), weights=(val), k=repl)
    tpop = []
    for i in range(repl):
        tpop.append((val[temp[i]],pop[temp[i]]))
    tpop.sort(reverse=True)
    i=0
    for a,b in tpop:
        pop[(i + offset) % psize] = b
        i+=1
    offset = (offset + repl) % psize
    return pop, offset

def crossover(repl, pop, offset,dim):
    pairs=repl//2
    psize=len(pop)
    temp=0
    for i in range(pairs):
        cross = np.random.binomial(size=1, n=1, p=pcr)
        if cross == 0: continue
        par1 = pop[(2 * i+offset-repl+psize)%psize]
        par2 = pop[(2 * i + 1+offset-repl+psize)%psize]
        # sp is the random point where the crossover will be performed
        sp = random.randrange(1, d + 1)
        child1 = []
        child2 = []

        for k in range(dim):
            child1.append(par1[k][:sp] + par2[k][sp:])
            child2.append(par2[k][:sp] + par1[k][sp:])
        pop[(offset+temp)%psize] = child1
        pop[(1 +offset+temp)%psize] = child2
        temp+=2
    return pop,temp

def mutation(psize, pop,offset,repl,tt):
    temp=0
    for i in range(repl):
        mut = np.random.binomial(size=1, n=1, p=pmu)
        if mut == 0:
            continue
        par=pop[(offset-repl+psize+i)%psize]
        for k in range(dim):
            btm = max(1,random.randrange(0,  d-1))
            for j in range(btm):
                if(j==btm-1):
                    par[k][d-j]=(par[k][d - j] + 1) % 2
                    continue
                if np.random.binomial(size=1, n=1, p=pmu) == 0:
                    continue
                par[k][d - j] = (par[k][d - j] + 1) % 2
        pop[(offset+tt+temp)%psize]=par
        temp+=1
    offset=(offset+temp+tt)%psize
    return pop, offset



                    ### MAIN ###

# initialization
dim, a, b, c, d, psize, pcr, pmu, ite, repl, pairs = user_inputs()
fifo = 0
offset = 0
pop = [[[random.randint(0, 1) for i in range(d + 1)] for j in range(dim)] for k in range(psize)]

maxans=0
for i in range(ite):
    val , scaval= fitvalues(pop)
    if(i==0):
        maxans=np.max(val)
    else:
        maxans=max(maxans,np.max(val))
    pop,offset = roulette_wheel_selection(pop, scaval, repl, offset)
    pop,temp = crossover(repl, pop, offset,dim)
    pop, offset = mutation(psize, pop,offset,repl,temp)
val,scaval =fitvalues(pop)
print('final population: ', pop)
print('final population values: ',val)
print('final population best value: ',np.max(val))
print('final population value mean: ',np.mean(val))
print('best overall value: ',maxans)
