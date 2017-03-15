# RedEnvelope
A better red envelope machenism for WeChat

[WeChat red envelope](https://en.wikipedia.org/wiki/WeChat_red_envelope}) enables a user to send money with some degree of randomness. A red envelope is determined by two numbers: amount of money *M* and number of receivers *N*. Receiver *k* gets a random amount of money *X_k*, adding up to *M*. This problem is simplified as generating *N* random variables adding to *1*.

An ideal implementation of red envelope should be **fair**, in the sense that all *X<sub>k</sub>* follow the same distribution. To achieve this, one can sample *N-1* independent random variables of uniform distribution from *[0, 1]* and use these numbers as partition points, this can guarantee fairness but requires extra storage space for the *N-1* random numbers.

A better solution is to generate random numbers on demand, in which case we need a function taking only two inputs: remaining money *m* and number of remaining receivers *n*, and output a random variable. One proposed method is to sample by truncated normal distribution *N(1/n, σ<sup>2</sup>)*, this method is unfair unless *σ = 0*, where the distribution becomes Dirac distribution and everyone get the same amount of money--very boring. In general, sampling by normal distribution needs to compromise between level of fairness and level of fun, thus not a good solution.

The correct solution is to sample by **Beta distribution**. It can be shown that if *x* follows *Beta(c, c(n-1))*, *c > 0*, returning _m*x_ will guarantee fairness: all *X<sub>k</sub>* follow distribution *Beta(c, c(N-1))*, which is not a boring distribution.
