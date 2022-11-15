import torch
from torch.distributions import normal

class SABR:
    def __init__(self):
        self.params = None

    def sigma_SABR(self, params, x1, beta=0.5):
        K, S, t = x1

        alpha, nu, rho = params

        z = nu / alpha * (S * K) ** ((1 - beta) / 2) * torch.log(S / K)

        x = torch.log((torch.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))

        numerator = 1 + (((1 - beta) ** 2 / 24) * alpha ** 2 / ((S * K) ** (1 - beta))
                         + (rho * beta * nu * alpha) / (4 * (S * K) ** ((1 - beta) / 2))
                         + ((2 - 3 * rho ** 2) / 24 * nu ** 2)) * t

        denominator = ((S * K) ** ((1 - beta) / 2) * (1 + (1 - beta) ** 2 / 24 * torch.log(S / K) ** 2
                                                  + (1 - beta) ** 4 / 1920 * torch.log(S / K) ** 4))

        sigma = alpha * numerator / denominator * z / x

        return sigma

    def set_params(self, params):
        self.params = params

    def d1(self, S, K, t, sigma, r=0):
        return (torch.log(S / K) + (r + sigma ** 2 / 2.) * t) / (sigma * torch.sqrt(t))

    def d2(self, S, K, t, sigma, r=0):
        return self.d1(S, K, t, sigma, r) - sigma * torch.sqrt(t)

    def bs_call(self, x1, r=0):
        norm = normal.Normal(0, 1)
        K, S, t = x1
        sigma = self.sigma_SABR(self.params, x1, beta=0.5)
        return S * norm.cdf(self.d1(S, K, t, sigma, r)) - K * torch.exp(-r * t) * norm.cdf(self.d2(S, K, t, sigma, r))

    def bs_put(self, x1, r=0):
        K, S, t = x1
        sigma = self.sigma_SABR(self.params, x1, beta=0.5)
        return K * torch.exp(-r * t) - S * self.bs_call(S, K, t, sigma, r)
