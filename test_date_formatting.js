/**
 * Test script to verify frontend date formatting
 */
const testDateFormatting = () => {
  console.log("Testing frontend date formatting logic...\n");

  // Simulate the formatDateToDateTime function logic
  const formatDateToDateTime = (dateString: string | null | undefined): string | null => {
    if (!dateString) {
      return null;
    }

    // If dateString is already in ISO datetime format, return as is
    if (dateString.includes('T')) {
      return dateString;
    }

    // Convert date string (YYYY-MM-DD) to datetime (YYYY-MM-DDT00:00:00)
    return `${dateString}T00:00:00`;
  };

  // Test cases
  const testCases = [
    { input: "2026-01-29", expected: "2026-01-29T00:00:00" },
    { input: "2026-01-29T10:30:00", expected: "2026-01-29T10:30:00" }, // Already datetime
    { input: "", expected: null },
    { input: null, expected: null },
    { input: undefined, expected: null }
  ];

  console.log("Test cases:");
  testCases.forEach((testCase, index) => {
    const result = formatDateToDateTime(testCase.input as any);
    const passed = result === testCase.expected;

    console.log(`${index + 1}. Input: ${JSON.stringify(testCase.input)}`);
    console.log(`   Expected: ${JSON.stringify(testCase.expected)}`);
    console.log(`   Got: ${JSON.stringify(result)}`);
    console.log(`   Status: ${passed ? '✅ PASS' : '❌ FAIL'}\n`);
  });

  // Test the exact scenario from the error
  console.log("Testing the exact failing scenario:");
  const originalDate = "2026-01-29";
  const formattedDate = formatDateToDateTime(originalDate);
  console.log(`Original: "${originalDate}"`);
  console.log(`Formatted: "${formattedDate}"`);
  console.log(`This formatted date should be accepted by the updated backend!`);
};

// Run the test
testDateFormatting();