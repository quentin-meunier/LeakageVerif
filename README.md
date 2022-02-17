# LeakageVerif: Scalable and Efficient Leakage Verification in Symbolic Expressions

LeakageVerif is a formal verification tool for the probing security of masked implementations. It provides a way for verifying probing security on a set of symbolic expressions.

LeakageVerif is a python library offering a set of constructs and functions for writing and verifying symbolic expressions. A symbolic expression in LeakageVerif is a fixed width expression comprising operations on constants and symbolic variables. Each symbolic variable has a type between secret, mask and public. LeakageVerif verifies that the distribution of the expression value is independent from the secret values it contains, considering that mask variables follow an random uniform distribution.

This work is currently under review and has been published as a preprint under the following reference:  
Meunier, Q. L., Pons, E. and Heydemann, K. (2021). LeakageVerif: Scalable and Efficient Leakage Verification in Symbolic Expressions". Cryptology ePrint Archive (2021).
[Link](https://eprint.iacr.org/2021/1468)


## Installation

As a python library, LeakageVerif just needs to be cloned to a directory called `leakage_verif`, which is the name of the python module it provides. The parent directory of `leakage_verif` must be added to the PYTHONPATH environment variable. LeakageVerif has only be tested on Linux so far.


## Usage

In order to use LeakageVerif constructs, put the following line at the beginning of a python file:
```
from leakage_verif import *
```

Symbolic variables are created with a function called `symbol`: the first parameter is the symbol name, the second parameter the symbol type ('S' for secret, 'M' for mask and 'P' for a public variable), and the third parameter the symbol width. Constants with a function called `constant`, taking as parameters the value and the width.
```
from __future__ import print_function
from leakage_verif import *

# Creating an 8-bit secret variable named 'k' 
k = symbol('k', 'S', 8)

# Creating an 8-bit mask variable named 'm0'
m = symbol('m', 'M', 8)

# Creating the 8-bit constant 0xAE
c = constant(0xAE, 8)

# Computing an expression
e = k ^ m ^ c

# Checking probing security on e
res = checkTpsVal(e)

if res:
    print('# Expression %s is probing secure' % e)
else:
    print('# Expression %s is not probing secure' % e)

```

## Supported operations

* `^`: bitwise exclusive OR
* `&`: bitwise AND
* `|`: bitwise OR
* `~`: bitwise NOT
* `+`: arithmetic addition
* `-`: arithmetic subtraction
* `<<`: logical shift left. The shift amount must be a constant or a python integer, and cannot be symbolic.
* `>>`: arithmetic shift right. The shift amount must be a constant or a python integer, and cannot be symbolic.
* `\*`: finite field multiplication. Currently, it is only implemented on 8 bits, and with the irreducible polynomial 0x11B.
* `\*\*`: integer multiplication, modulo 2 to the power of the expression width.

Some operations are implemented in the form of functions:

* `LShR(x, y)`: logical shift right. The shift amount y must be a constant or a python integer, and cannot be symbolic.
* `RotateRight(x, y)`: right shift with rotation
* `Concat(x, y, ...)`: concatenation of expressions
* `Extract(msb, lsb, e)`: extraction of some of the bits in e, from the most significant bit given by msb, to the least significant bit given by lsb.
* `ZeroExt(v, e)`: zero extension: extension of the expression e by the addition of v bits with value 0 on the left of e
* `SignExt(v, e)`: signed extension: extension of the expression e by adding v time the MSB of e on its left

## Functionalities

### Simplification

LeakageVerif implements a wide range of simplifications, taking advantage of operators properties. In order to simplify an expression, simply call the `simplify` function:
```
p0 = symbol('p0', 'P', 8)
p1 = symbol('p1', 'P', 8)
m = symbol('m', 'M', 8)
e = ((p0 ^ m) | (p0 & constant(0, 8))) ^ (m & constant(0xFF, 8) + (p0 ^ p0))
simplifiedExp = simplify(e)
print('simplifiedExp: %s' % simplifiedExp)
```

### Bit decomposition of expressions

LeakageVerif can decompose an expression into a concatenation of bit expressions. Although this feature is mostly used in the verification algorithm, it is possible to get the equivalent bit decomposition with the function `getBitDecomposition`. n-bit symbolic variables are decomposed in n 1-bit variables of the same type.
```
k = symbol('k', 'S', 4)
exp = k & constant(0x5, 4)
bitExp = getBitDecomposition(exp)
print('bitExp: %s' % bitExp)
```

### Arrays

Symbolic array accesses can be modeled in LeakageVerif expressions. Currently, only some types of arrays are considered, more specifically those in which the corresponding initialization in the non-symbolic implementation is made without using symbolic variables. This means that accessing to an array with expression e as index cannot leak more information than e, and prevents for example to have an index i such that array[i] = exp, where exp is a symbolic expression. This is particularly useful for algorithms like the AES in which the SBox can be implemented as an array. In order to create an array, one has to use the `registerArray` function. Parameters include the array name, input and output width, and array size. For example, the SBox from the AES can be implemented as follows:
```
sbox = [ 0x63, 0x7C, ..., 0x16 ]
registerArray('mysbox', 8, 8, None, 256, None)

def SBox(e):
    if isinstance(e, ConstNode):
        return Const(sbox[e.cst], 8)
    sb = getArrayByName('mysbox')
    return sb[e]
```
It is advised to always consider the case in which an expression is concrete, as this allows to evaluate the expression for specific input values. This is very useful for checking an implementation, as it is sufficient to replace symbolic variables with constants in order to check the correctness of an implementation. This also allows to use the **concrete evaluation** module functions.

Arrays can also be associated to a base address and a function. The base address represents its memory implantation, while the function to call is used as a substitute for the expression to use. This mechanism is useful when verifying assembly code. In that case, if a memory address accessing the array has a symbolic part, this part can be used as the offset. If a function is also associated to the array, it can be called on the index. This allows for example to implement multiplication by 2 or 3 in the AES with an array:
```
def mul_02(mem, e):
    return constant(2, 8) * e

registerArray('mul_02', 8, 8, 0x8c34, 256, mul_02)
```
Examples using this functionality can be found in the `Arm-ASM` benchamrk.

Note that this is not necessary when implementing the AES directly because in the latter case we can simply replace the array access with the expression `constant(2, 8) * e` or `constant(3, 8) * e`.
 


### Concrete Evaluation

The concrev module provides functions based on concrete evaluation. This comes in two flavours: exhaustive evaluation and random evaluation. Exhaustive evaluation enumerates all possible symbolic variables' values, and random evaluation evaluate the expression for arbitrarily chosen values. The provided functions are:

* `compareExpsWithExev(e0, e1)`: checks that expressions e0 and e1 are equivalent for all possible combinations of inputs
* `compareExpsWithRandev(e0, e1, nbEval)`: checks that expressions `e0` and `e1` provide the same result for nbEval evaluations, in which the value of all symbolic variables is chosen randomly. This is useful when enumeration is not possible.
* `getDistribWithExev(e)`: Computes the distribution of the expression `e` regarding its secret variables. The first returned value is True iff the expression has a uniform distribution, the second returned value is True iff the distribution is independent from the secret variables' values.


### Verification

The main verification function, `checkTpsVal(e)` verifies the probing security of the expression `e`. Some other security properties are also considered, and are detailed in [1]:

* `checkTpsTrans(e0, e1)`: verifies that the couple of expression (e0, e1) is probing secure
* `checkTpsTransXor(e0, e1)`: verifies that expression `e0 ^ e1` is probing secure
* `checkTpsTransBit(e0, e1)`: verifies that each couple of expressions of the form (`e0[i]`, `e1[i]`) is probing secure, where `e0[i]` (resp. `e1[i]`) is the expression of the `i`-th bit of `e0` (resp. `e1`)
* `checkTpsTransXorBit(e0, e1)`: verifies that each expression of the form `e0[i] ^ e1[i]` is probing secure



## Benchmarks

The `benchmarks` directory contains a few applications, while the `tests` directory contains smaller tests. Some of the benchmarks are taken from [MaskedVerifBench](https://www.url.com).

* AES-Herbst (from MaskedVerifBench): masked version of the AES following the scheme in [2], comprising the key schedule and ten rounds.
* AES-SM (from MaskedVerifBench): masked implementation adapted from [3]. It implements the same masking scheme as the one in [2], but with a symbolic Galois field multiplication by constants 2 and 3 in the mix-columns step, and does not mask the key schedule.
* ISW-And: several versions of the ISW AND scheme from [4]. Versions with 2 or 3 shares are considered, as well as the presence of an additional random for computing expression of the form a<sub>i</sub>b<sub>j</sub>. Verifications are made at the first and second orders.
* Secmult (from MaskedVerifBench): secure Galois field multiplication as described in [5].
* Secmult-SM (from MaskedVerifBench): Secmult algorithm with symbolic multiplication.
* Arm-Asm: Arm assembly implementations of AES-Herbst and of the Secmult program. Minimal models for the ISA and the memory are provided, and the leakage model consists in analyzing the result (value) of each instruction which modifies a general purpose register in the processor core.



## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)



## References

[1] Meunier, Q. L., El Ouahma, I. B., and Heydemann, K. (2020, September). SELA: a Symbolic Expression Leakage Analyzer. In International Workshop on Security Proofs for Embedded Systems.

[2] Herbst, C., Oswald, E., and Mangard, S. (2006, June). An AES smart card implementation resistant to power analysis attacks. In International conference on applied cryptography and network security (pp. 239-252). Springer, Berlin, Heidelberg.

[3] Yao, Y., Yang, M., Patrick, C., Yuce, B., and Schaumont, P. (2018, April). Fault-assisted side-channel analysis of masked implementations. In 2018 IEEE International Symposium on Hardware Oriented Security and Trust (HOST) (pp. 57-64). IEEE.

[4] Ishai, Y., Sahai, A., and Wagner, D. (2003, August). Private circuits: Securing hardware against probing attacks. In Annual International Cryptology Conference (pp. 463-481). Springer, Berlin, Heidelberg.

[5] Rivain, M., and Prouff, E. (2010, August). Provably secure higher-order masking of AES. In International Workshop on Cryptographic Hardware and Embedded Systems (pp. 413-427). Springer, Berlin, Heidelberg.

