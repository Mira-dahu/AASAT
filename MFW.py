import math


def calculate_rho_multi_factor(Pa, ECM, RCS, ENV, w1=0.4, w2=0.3, w3=0.2, w4=0.1):
    def f(Pa):
        return (1 / (math.exp(1) - 1)) * (math.exp(Pa) - 1)

    def g(ECM):
        return 1 - ECM / 100  # 假设ECM为0-100的值

    def h(RCS):
        return 1 / (1 + math.exp(-0.1 * (RCS - 10)))  # Sigmoid函数

    def i(ENV):
        return ENV / 10  # 假设ENV为0-10的值

    rho = w1 * f(Pa) + w2 * g(ECM) + w3 * h(RCS) + w4 * i(ENV)
    return rho