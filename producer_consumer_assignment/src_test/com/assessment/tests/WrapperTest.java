package com.assessment.tests;

import static org.junit.Assert.assertTrue;
import org.junit.Test;

// JUnit wrapper class that allows the custom test harness (TestSharedQueue)
// to be executed as part of a standard JUnit build pipeline.
public class WrapperTest {

    @Test
    public void runMainTest() throws Exception {
        // Delegate the actual testing to the custom harness.
        // We assert true only if the entire suite returns success.
        boolean success = TestSharedQueue.runTests();
        assertTrue("One or more manual tests failed. Check console output.", success);
    }
}
