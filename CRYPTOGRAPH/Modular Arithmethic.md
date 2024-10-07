# GCD
https://cryptohack.org/courses/modular/gcd/
The Greatest Common Divisor (GCD), sometimes known as the highest common factor, is the largest number which divides two positive integers $(a,b)$.  
  
For $a=12, b=8$ we can calculate the divisors of $a: 1,2,3,4,6,12$ and the divisors of $b: 1,2,4,8$. Comparing these two, we see that $gcd(a,b)=4$
  
Now imagine we take $a=11,b=17$. Both a and b are prime numbers. As a prime number has only itself and 11 as divisors, $gcd⁡(a,b)=1$
  
We say that for any two integers $a,b$, if $gcd⁡(a,b)=1$ then a and b are coprime integers.  
  
If a and b are prime, they are also coprime. If a is prime and $b<a$ then aa and bb are coprime.  
  
There are many tools to calculate the GCD of two integers, but for this task we recommend looking up [Euclid's Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm).  


# Extended GCD
https://cryptohack.org/courses/modular/egcd/  
Let a and b be positive integers.  
  
The extended Euclidean algorithm is an efficient way to find integers $u,v$ such that  
  
$a⋅u+b⋅v=gcd⁡(a,b)$
  
 Later, when we learn to decrypt RSA ciphertexts, we will need this algorithm to calculate the modular inverse of the public exponent.  
  
Knowing that $p,q$ are prime, what would you expect $gcd⁡(p,q)$ to be? For more details on the extended Euclidean algorithm, check out [this page](https://web.archive.org/web/20230511143526/http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html).