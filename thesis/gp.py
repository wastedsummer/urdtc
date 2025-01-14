from __future__ import division
import numpy as np
import matplotlib.pyplot as pl

""" This is code for simple GP regression. It assumes a zero mean GP Prior """


# This is the true unknown function we are trying to approximate
f = lambda x: np.sin(0.9*x).flatten()
#f = lambda x: (0.25*(x**2)).flatten()


# Define the kernel
def kernel(a, b):
    """ GP squared exponential kernel """
    kernelParameter = 0.1
    sqdist = np.sum(a**2,1).reshape(-1,1) + np.sum(b**2,1) - 2*np.dot(a, b.T)
    return np.exp(-.5 * (1/kernelParameter) * sqdist)

N = 10         # number of training points.
n = 50         # number of test points.
s = 0.00005    # noise variance.

# create training data
X = np.random.uniform(-5, 5, size=(N,1))
y = f(X) + s*np.random.randn(N)

# setup covariance function for training data
K = kernel(X, X)
# and perform cholesky decomposition
L = np.linalg.cholesky(K + s*np.eye(N))

# points we're going to make predictions at.
Xtest = np.linspace(-5, 5, n).reshape(-1,1)



# compute the mean at our test points.
Lk = np.linalg.solve(L, kernel(X, Xtest))
mu = np.dot(Lk.T, np.linalg.solve(L, y))

# compute the variance at our test points.
K_ = kernel(Xtest, Xtest)
print(K_.shape)
s2 = np.diag(K_) - np.sum(Lk**2, axis=0)
s = np.sqrt(s2)


# PLOTS:
# pl.figure(1)
# pl.clf()
# pl.plot(X, y, 'r+', ms=20)
# pl.plot(Xtest, f(Xtest), 'b-')
# pl.gca().fill_between(Xtest.flat, mu-1*s, mu+1*s, color="#dddddd")
# pl.plot(Xtest, mu, 'r--', lw=2)

# pl.savefig('predictive.png', bbox_inches='tight')
# pl.title('Mean predictions plus 3 st.deviations')
pl.axis([-5, 5, -3, 3])

# draw samples from the prior at our test points.
L = np.linalg.cholesky(K_ + 1e-6*np.eye(n))
f_prior = np.dot(L, np.random.normal(size=(n,10)))
# pl.figure(2)
pl.clf()
# pl.plot(Xtest, f_prior, color='xkcd:tan')
pl.title('Ten samples from the GP prior')
# pl.axis([-5, 5, -3, 3])
# pl.savefig('prior.png', bbox_inches='tight')

# draw samples from the posterior at our test points.
L = np.linalg.cholesky(K_ + 1e-6*np.eye(n) - np.dot(Lk.T, Lk))
f_post = mu.reshape(-1,1) + np.dot(L, np.random.normal(size=(n,10)))
pl.figure(1)

# pl.figure(figsize=(9,6))
pl.clf()

# sns.set_style('darkgrid')
# pl.plot(Xtest, f(Xtest), 'b-')
pl.plot(Xtest, mu, 'r', lw=2,color='#F67941',label='mean function')
pl.plot(Xtest[0], f_post[0][0], color='#AC454A', linestyle='dotted',label='samples')
pl.plot(Xtest, f_post, color='#AC454A', linestyle='dotted')
pl.gca().fill_between(Xtest.flat, mu-1*s, mu+1*s, color="#EAD296", alpha=0.5, label='standard deviation')
pl.plot(X, y, '.', ms=15,color='#4999F2', label='data points')
# print(Xtest[0].shape)
# print(f_post[0].shape)
pl.title('GP posterior')
pl.axis([-5, 5, -3, 3])
pl.legend()
pl.savefig('images/post.pdf',format='pdf', bbox_inches='tight')

pl.show()
