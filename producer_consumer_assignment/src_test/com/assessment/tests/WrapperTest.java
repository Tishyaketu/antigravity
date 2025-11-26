package com.assessment.tests;

import static org.junit.Assert.assertTrue;
import org.junit.Test;

public class WrapperTest {
    @Test
    public void runMainTest() throws Exception {
        // Call the main method of the existing test class
        boolean success = TestBlockingQueue.runTests();
        assertTrue("One or more manual tests failed. Check console output.", success);
    }
}
