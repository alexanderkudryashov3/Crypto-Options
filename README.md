# Crypto-Options
Crypto-Options Volatility Surface Calibration and Arbitrage
This project's aim is to calibrate implied volatility surface for options on criptocurrencies.

## Getting data
The necessary data has been pulled from Deribit API (Deribit is world's biggest bitcoin and ethereum options exchange). The file get_data.py contains a class Parser which provides with possibility to either fetch live data for n minutes, or to get historical data using tardis_dev library, but its free usage is limited to getting data for the first day of the month. Corresponding method  returns a dataset containing currency, type of the option, days until expiration, strike, mark price, mark implied volatility and underlying price. 

## Calibration
For surface calibration, SABR model has been used. SABR is a stochastic volatility model, which attempts to capture the volatility smile in derivatives markets. The name stands for "stochastic alpha, beta, rho", referring to the parameters of the model. File SABR.py makes use of an approximation formula presenting the implied volatility of European call option as a function of strike and today’s forward price, i.e. σ(K,f), derived by singular perturbation analysis by P.S. Hagan and his co-workers[1].
![IMG_6272FD8E159B-1](https://user-images.githubusercontent.com/60070857/209577582-dea15fa9-89c7-45d3-bfdd-669b922def37.jpeg)
It also implements the closed-form solution of Black-Scholes model.

## Non-linear optimisation
Non-linear least squares problem is solved using Levenberg–Marquardt algorithm implemented in Levenberg_Marquardt.py.

## Results
The main result of the project is the calibrated volatility surface (SABR calibration.ipynb):

![ezgif-1-54076948dd](https://user-images.githubusercontent.com/60070857/209576440-45c0b193-d70c-42aa-9442-f90501aa5ae7.gif?raw=true)
![ezgif-1-6b1ab8a88d](https://user-images.githubusercontent.com/60070857/209576443-42db3aab-c974-4dbf-af22-ef6912091cdd.gif?raw=true)


Volatility smile has been modeled fairly well:

<img width="453" alt="Screenshot 2022-12-26 at 10 17 54 PM" src="https://user-images.githubusercontent.com/60070857/209577855-c3ea9547-e74d-4456-b141-b43dd64ccebb.png">


Testing on new data (test SABR calibration.ipynb) also shows good perfomance:

<img width="447" alt="Screenshot 2022-12-26 at 10 26 47 PM" src="https://user-images.githubusercontent.com/60070857/209578353-ef42b95d-22e4-4f09-9585-0f7efdf6239b.png">


## Future development
Implementing other stochastic volatility models, for example, Heston model.
Testing different options trading strategies and looking for potential arbitrage opportunities on this market.


[1] P. S. Hagan, D. Kumar, A. Lesniewski, D. E. Woodward: Managing Smile Risk, http://www.math.ku.dk/~rolf/SABR.pdf, 2002.

