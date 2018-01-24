.. toctree::
   :hidden: 
   :includehidden: 

tests.functional.nested.test_sample
-----------------------------------


Test file for preconditions & the like

.. topic:: Module Fixtures

   None!


test_module_level_test
++++++++++++++++++++++


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


test_module_level_test2
+++++++++++++++++++++++


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      PASSED
   **teardown**
      PASSED


TestRSABounds
~~~~~~~~~~~~~


RSA Bound checking.


.. topic:: Class Fixtures

   auth_session
      
      Allocates a ClientNode based off of the following specs in order:
      
         1. ped/pwd/rped class markers (multiple for parametrization) - used for HSM allocation.
         2. CLIENT_NODE_PARAMS class constant (for Client allocation)
         3. HSM_PARAMS class constant - for HSM allocation -- can be a list or a dictionary.
         4. Command line client specifications (--os, --bus, etc)
      
      .. note:: For HSM allocation & parameters
      
          * If `HSM_PARAMS` is set on test class
              * If it is a list, it will look for a client with HSMs matching each dictionary
                parameters (e.g. `[{'auth': PED}, {'auth': PED}]` will attempt to allocate a client
                node with 2 PED-auth HSMs attached)
              * If it is a dictionary, it will look for a client with at least ONE HSM matching
                the dictionary parameters. (e.g. `{'auth': PED}` will attempt to allocate a client
                node with at least one PED-auth HSM attached)
          * If the class is marked w/ ped or pwd, it will allocate an HSM of the current product
            type with the specified auth (if both are marked, test will be parametrized)
      
      
      :return: Allocated :class:`~LunaTAP.core.client.node.ClientNode`
      


test_bad_modulus
++++++++++++++++


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


test_largest_valid_exponent[186_3_PRIMES]
+++++++++++++++++++++++++++++++++++++++++


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


test_largest_valid_exponent[186_3_AUX_PRIMES]
+++++++++++++++++++++++++++++++++++++++++++++


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


test_bad_modulus_failing
++++++++++++++++++++++++


Fail this test, cause I want to see decent output.


.. topic:: Function Fixtures

   None!


.. topic:: Test Results

   **setup**
      PASSED
   **call**
      FAILED
      ::
         self = <tests.functional.nested.test_sample.TestRSABounds object at 0x0000000004AD9C88>
         auth_session = 0
         
             def test_bad_modulus_failing(self, auth_session):
                 """
                     Fail this test, cause I want to see decent output.
                     """
         >       assert "False" == "This isn't really false"
         E       assert 'False' == "This isn't really false"
         E         - False
         E         + This isn't really false
         
         nested\test_sample.py:65: AssertionError
   **teardown**
      PASSED




