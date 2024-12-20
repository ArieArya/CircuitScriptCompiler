# Optimization

## Types of Optimizations

In this section, we look at four different types of optimizations.

-   Copy propagation
-   Constant propagation
-   Constant folding
-   Dead code elimination

We note that much of our program (which evaluates circuit logic) can be evaluated at compile-time. This allows for significant optimizations so that much of the circuit simulation load will be handled by the compiler. See the examples below.

---

### Example - Big Circuit 1

Consider the example source code below (can also find in `sample_code/big_circuit_1.circuit`)

```
reg r1 = 1;
reg r2 = 0;
reg r3 = 1;
reg r4 = 1;
reg r5 = 0;

wire w1 = and(r1, r2);
wire w2 = or(w1, r3);
wire w3 = not(w2);
wire w4 = not(r4);
wire w5 = and(w4, r5);
wire w6 = not(w5);

wire out = or(w3, w6);

print(out);
```

Our language describes the circuit set-up. If we do not perform optimization (besides circuit reduction), the generated IR code would look like the below:

```
LOAD r1, 1
LOAD r2, 0
LOAD r3, 1
LOAD r4, 1
LOAD r5, 0
AND t1, r1, r2
MOV w1, t1
OR t2, w1, r3
MOV w2, t2
NOT t3, w2
MOV w3, t3
NOT t4, r4
MOV w4, t4
AND t5, w4, r5
MOV w5, t5
NOT t6, w5
MOV w6, t6
OR t7, w3, w6
MOV out, t7
PRINT out
```

The above takes a lot of instructions in our VM, and will take even more operations for more complicated circuits.

However, we note that the only value we are interested in is the wire `out`, i.e. via the print statement. Thus, our compiler can perform all the circuit evaluation in compile-time, and output an intermediate code with only a single line, as below:

```
PRINT 1  (this is the value of the wire "out")
```

This is in fact the generated optimized code of our language. Our VM that executes this IR can run extremely fast (1 instruction instead of many).

---

### Example - Logic Gates Circuit

Consider the code below (can also find in `sample_code/logic_gates.circuit`)

```
wire w1 = and(1, 1);
wire w2 = and(0, 1);
wire w3 = or(0, 1);
wire w4 = or(0, 0);
wire w5 = not(w4);
wire w6 = xor(0, 1);

print(w1);
print(w2);
print(w3);
print(w4);
print(w5);
print(w6);
```

As before, much of the circuit operations can be evaluated in compile-time. So, our IR will simply look like this:

```
PRINT 1
PRINT 0
PRINT 1
PRINT 0
PRINT 1
PRINT 1
```

If we did not have any optimizations, we would have a much bigger IR, like this:

```
AND t1, 1, 1
MOV w1, t1
MOV w2, 0
MOV w3, 1
OR t2, 0, 0
MOV w4, t2
NOT t3, w4
MOV w5, t3
XOR t4, 0, 1
MOV w6, t4
PRINT w1
PRINT w2
PRINT w3
PRINT w4
PRINT w5
PRINT w6
```

---

## Summary

We have shown how performing optimizations (copy propagation, constant propagation, constant folding, and dead code elimination) can significantly reduce the number of instructions in our generated IR. This demonstrates how compiler optimizations can improve overall performance of our compiled language.
