.. toctree::
   :hidden: 
   :includehidden: 

tests.functional.nested2.test_sample2
-------------------------------------


Test file for preconditions & the like

.. topic:: Module Fixtures

   None!


TestRSABounds
~~~~~~~~~~~~~


RSA Bound checking.


.. topic:: Class Fixtures

   auth_session
      
      Login to a Token and return the authenticated session handle.
      
      :param: request
      :return
      


test_bad_modulus[p1]
++++++++++++++++++++


When modulus bits < 2048 using only FIPS primes, should return CKR_KEY_SIZE_RANGE


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


test_largest_valid_exponent[p1-186_3_PRIMES]
++++++++++++++++++++++++++++++++++++++++++++


Validate that AUX primes & regular primes sign/verify correctly
with the largest possible valid exponent.


.. topic:: Function Fixtures

   mech
      1


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


test_largest_valid_exponent[p1-186_3_AUX_PRIMES]
++++++++++++++++++++++++++++++++++++++++++++++++


Validate that AUX primes & regular primes sign/verify correctly
with the largest possible valid exponent.


.. topic:: Function Fixtures

   mech
      1


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      FAILED
      ::
         self = <tests.functional.nested2.test_sample2.TestRSABounds object at 0x0000000004B1C550>
         auth_session = 0, mech = 2
         
             @pytest.mark.parametrize('mech', [1, 2],
                                      ids=["186_3_PRIMES", "186_3_AUX_PRIMES"])
             def test_largest_valid_exponent(self, auth_session, mech):
                 """
                     Validate that AUX primes & regular primes sign/verify correctly
                     with the largest possible valid exponent.
                     """
         >       assert 1 == mech
         E       assert 1 == 2
         
         nested2\test_sample2.py:35: AssertionError
   **teardown**
      PASSED


test_bad_modulus_failing[p1]
++++++++++++++++++++++++++++


Fail this test, cause I want to see decent output.


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      FAILED
      ::
         self = <tests.functional.nested2.test_sample2.TestRSABounds object at 0x0000000004B1CDA0>
         auth_session = 0
         
             def test_bad_modulus_failing(self, auth_session):
                 """
                     Fail this test, cause I want to see decent output.
                     """
         >       assert "False" == "This isn't really false"
         E       assert 'False' == "This isn't really false"
         E         - False
         E         + This isn't really false
         
         nested2\test_sample2.py:41: AssertionError
   **teardown**
      PASSED


test_bad_modulus[p2]
++++++++++++++++++++


When modulus bits < 2048 using only FIPS primes, should return CKR_KEY_SIZE_RANGE


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


test_largest_valid_exponent[p2-186_3_PRIMES]
++++++++++++++++++++++++++++++++++++++++++++


Validate that AUX primes & regular primes sign/verify correctly
with the largest possible valid exponent.


.. topic:: Function Fixtures

   mech
      1


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


test_largest_valid_exponent[p2-186_3_AUX_PRIMES]
++++++++++++++++++++++++++++++++++++++++++++++++


Validate that AUX primes & regular primes sign/verify correctly
with the largest possible valid exponent.


.. topic:: Function Fixtures

   mech
      1


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      FAILED
      ::
         self = <tests.functional.nested2.test_sample2.TestRSABounds object at 0x0000000004B2E128>
         auth_session = 0, mech = 2
         
             @pytest.mark.parametrize('mech', [1, 2],
                                      ids=["186_3_PRIMES", "186_3_AUX_PRIMES"])
             def test_largest_valid_exponent(self, auth_session, mech):
                 """
                     Validate that AUX primes & regular primes sign/verify correctly
                     with the largest possible valid exponent.
                     """
         >       assert 1 == mech
         E       assert 1 == 2
         
         nested2\test_sample2.py:35: AssertionError
   **teardown**
      PASSED


test_bad_modulus_failing[p2]
++++++++++++++++++++++++++++


Fail this test, cause I want to see decent output.


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      FAILED
      ::
         self = <tests.functional.nested2.test_sample2.TestRSABounds object at 0x0000000004B1CE80>
         auth_session = 0
         
             def test_bad_modulus_failing(self, auth_session):
                 """
                     Fail this test, cause I want to see decent output.
                     """
         >       assert "False" == "This isn't really false"
         E       assert 'False' == "This isn't really false"
         E         - False
         E         + This isn't really false
         
         nested2\test_sample2.py:41: AssertionError
   **teardown**
      PASSED




