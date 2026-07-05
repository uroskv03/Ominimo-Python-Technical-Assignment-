# Ominimo-Python-Technical-Assignment-

We take MTPL as a fixed, reference value.

To increase the values, we use the following recommended coefficients:
VARIANT_COEF = 1.07
DEDUCTIBLE_COEF = 1.11
PRODUCT_LEVEL_COEF = 1.20 (assuming this should be the highest coefficient)

In cases where MTPL is not available or zero as a reference value, we use MIN_VAL for prices that are zero or negative, because it makes no sense to multiply zero by a coefficient.

First, we compare the values with MTPL and increase any value that is less than or equal to it.
Next, we compare by deductible and apply the increases (only within the same types, of course).
Then, we repeat the process by variant, and finally by product level.

Since changes at the product level could potentially disrupt the hierarchy in previous levels, it is best to repeat this entire process until no further changes occur. 
I decided to use a loop instead of recursion for the scalability to avoid a StackOverflow. I decided to always increase the value because of simplicity - to reduce the number of iterations.

I also considered to cover the case where for example: 500 and 100 deductibles exist, but 200 is missing. Since the text says "You may assume the input dictionary contains all relevant combinations", I assumed I didn't need to do that.



