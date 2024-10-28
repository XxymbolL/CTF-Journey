# GCD
https://cryptohack.org/courses/modular/gcd/
The Greatest Common Divisor (GCD), sometimes known as the highest common factor, is the largest number which divides two positive integers $(a,b)$.  
  
For $a=12, b=8$ we can calculate the divisors of $a: 1,2,3,4,6,12$ and the divisors of $b: 1,2,4,8$. Comparing these two, we see that $gcd(a,b)=4$
  
Now imagine we take $a=11,b=17$. Both a and b are prime numbers. As a prime number has only itself and 11 as divisors, $gcd⁡(a,b)=1$
  
We say that for any two integers $a,b$, if $gcd⁡(a,b)=1$ then a and b are coprime integers.  
  
If a and b are prime, they are also coprime. If a is prime and $b<a$ then a and b are coprime.  
  
There are many tools to calculate the GCD of two integers, but for this task we recommend looking up [Euclid's Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm).  


# Extended GCD
https://cryptohack.org/courses/modular/egcd/  
Let a and b be positive integers.  
  
The extended Euclidean algorithm is an efficient way to find integers $u,v$ such that  
  
$a⋅u+b⋅v=gcd⁡(a,b)$
  
 Later, when we learn to decrypt RSA ciphertexts, we will need this algorithm to calculate the [[Modular Invers]] of the public exponent.  
  
Knowing that $p,q$ are prime, what would you expect $gcd⁡(p,q)$ to be? For more details on the extended Euclidean algorithm, check out [this page](https://web.archive.org/web/20230511143526/http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html).

# Modular Aritmethic
https://cryptohack.org/courses/modular/ma0/
Imagine you lean over and look at a cryptographer's notebook. You see some notes in the margin:  

```
4 + 9 = 1  
5 - 7 = 10  
2 + 3 = 5  
```

At first you might think they've gone mad. Maybe this is why there are so many data leaks nowadays you'd think, but this is nothing more than modular arithmetic modulo 12 (albeit with some sloppy notation).  
  
You may not have been calling it modular arithmetic, but you've been doing these kinds of calculations since you learnt to tell the time (look again at those equations and think about adding hours).  
  
Formally, "*calculating time*" is described by the theory of congruences. We say that two integers are congruent modulo m if **$a≡b\ mod\ m$**
  
Another way of saying this, is that when we **divide** the integer a by m, the remainder is b. This tells you that if m divides a (this can be written as $m∣a$) then $a ≡ 0\ mod\ m$.  
  
