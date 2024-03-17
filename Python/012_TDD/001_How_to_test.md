# How to test?

Three guidelines that (hopefully) most developers will agree with that will help you write valuable tests:

1. Tests should tell you the expected behavior of the unit under test. Therefore, it's advisable to keep them short and to the point. The GIVEN, WHEN, THEN structure can help with this:

* GIVEN - what are the initial conditions for the test?
* WHEN - what is occurring that needs to be tested?
* THEN - what is the expected response?

    So you should prepare your environment for testing, execute the behavior, and, at the end, check that output meets expectations.

2. Each piece of behavior should be tested once -- and only once. Testing the same behavior more than once does not mean that your software is more likely to work. Tests need to be maintained too. If you make a small change to your code base and then twenty tests break, how do you know which functionality is broken? When only a single test fails, it's much easier to find the bug.

3. Each test must be independent from other tests. Otherwise, you'll have hard time maintaining and running the test suite.