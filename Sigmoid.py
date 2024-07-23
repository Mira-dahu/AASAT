import math

def calculate_rho_sigmoid(Pa, k=10, theta=0.5):
    return 1 / (1 + math.exp(-k * (Pa - theta)))