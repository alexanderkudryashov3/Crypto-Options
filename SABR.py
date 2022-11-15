import torch

class SABR:
    def __init__(self):
        pass

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