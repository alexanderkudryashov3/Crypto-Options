import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import torch

class Levenberg_Marquardt:
    def __init__(self, y, x, f, params):
        
        self.y = y
        self.x = x
        self.f = f
        self.l = 100
        self.nu_up = 1/1.5
        self.nu_down = 2
        self.params = params
        self.update_residuals()
        self.losses = [torch.norm(self.residuals).item()]
        self.origins = []
        self.increments = []

    def boundaries(self):
        
        self.params[0][self.params[0]<0] = 1e-2
        self.params[1][self.params[1]<0] = 1e-2
        self.params[2][self.params[2]>1] = 1-1e-2
        self.params[2][self.params[2]<-1] = -1+1e-2
        
    def update_params(self):
        
        self.dparams = torch.matmul(torch.matmul(torch.inverse((self.l*torch.eye(self.J.size(dim=1))+
                                            torch.matmul(torch.transpose(self.J, 0, 1), self.J))),torch.transpose(self.J, 0, 1)), self.residuals)
        
        self.origins.append(tuple(self.params.tolist()))
        self.increments.append(tuple(self.dparams.tolist()))
        
        self.params += self.dparams
        self.boundaries()

        
        
    def update_residuals(self):
        
        self.residuals = self.y - self.f(self.params, self.x)
        
        
    def update_jacobian(self):
        
        self.J = torch.autograd.functional.jacobian(self.f, (self.params, self.x), create_graph=False, strict=False)[0]
        
        
    def step(self):

        self.update_jacobian()
        self.update_params()
        self.update_residuals()
        self.losses.append(torch.norm(self.residuals).item())
        
        if self.losses[-1]-self.losses[-2]>0:
            self.l*=self.nu_down
        else:
            self.l*=self.nu_up
            
            
    def fit(self, n_iter):

        for i in range(n_iter):
            self.step()
        return self.losses, self.params             
        
        
    def visualize(self):
                
        o = np.array(self.origins)
        v = np.array(self.increments)
        X = o[:, 0]
        Y = o[:, 1]
        Z = o[:, 2]
        dX = v[:, 0]
        dY = v[:, 1]
        dZ = v[:, 2]
        
        x1 = np.linspace(X.min(), X.max(), 10)
        y1 = np.linspace(Y.min(), Y.max(), 10)
        z1 = np.linspace(Z.min(), Z.max(), 10)
        param_grid = torch.Tensor(np.array(np.meshgrid(x1,y1,z1)).T.reshape(-1,3))
        loss_grid = [torch.norm(self.y - self.f(param_grid[i], self.x)) for i in range(len(param_grid))]
        
        fig = plt.figure()
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        
        img = ax.scatter(param_grid[:,0], param_grid[:,1], param_grid[:,2], c=loss_grid, cmap=plt.hot(),edgecolors='none', alpha=0.6)
        fig.colorbar(img)
        
        plt.quiver(X, Y, Z, dX, dY, dZ, normalize = True, color = 'Black', linewidth = 2, arrow_length_ratio=0.1)
        plt.show();
              