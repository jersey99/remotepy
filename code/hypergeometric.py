N = 75  # Total Questions
n = 45  # Questions per turn


def prod(l): return reduce(lambda x, y: x * y, l, 1)


def prod(l): return reduce(lambda x, y: x * y, l, 1)


def fact(n): return prod(range(1, n + 1))


def choose(n, k):
    return fact(n) / (fact(k) * fact(n - k))


def hyperGeometric(k, n, K, N):
    return (choose(K, k) * choose(N - K, n - k)) / (choose(N, n) * 1.)

#print("wikipedia test", hyperGeometric(4,10,5,50), hyperGeometric(5,10,5,50))

X = {}  # Memoise


def expectedTurns(Q):
    if Q in X: return X[Q]
    Ev = Pf = 0.0
    if N == Q: return 0.
    for i in range(min(N - Q + 1, n + 1)):
        Pgo = hyperGeometric(i, n, N - Q, N)
        if i == 0:
            # The case where All the questions are previously seen
            Pf = Pgo
            continue
        Ev += Pgo * expectedTurns(Q + i)
    Ev = (1 + Ev) / (1 - Pf)
    X[Q] = Ev
    return Ev


def totalTurns(n=45, totalN=75):
    global N
    N = totalN
    retVal = 1 + expectedTurns(n)  # the Extra 1 for the first turn
    print retVal
    return retVal

if __name__ == "__main__":
    totalTurns()
