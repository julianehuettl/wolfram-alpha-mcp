<mcp>
name: wolfram-alpha-test
description: A test prompt for the Wolfram Alpha MCP Server
arguments:
  - name: test_type
    description: The type of test (math, science, conversion, formula)
    required: true
</mcp>

# Wolfram Alpha MCP Server Test

This prompt demonstrates the capabilities of the Wolfram Alpha MCP Server. The server can:

1. Perform mathematical calculations
2. Answer scientific questions
3. Conduct data analysis
4. Provide unit conversions
5. Solve equations

## Test Scenario

Please perform the following tests:

1. **Mathematical Calculation**:
   - Calculate: 2 + 2
   - Calculate: 3 * 4
   - Calculate: 10 / 2

2. **Scientific Question**:
   - What is the speed of light?
   - What is the mass of the Earth?
   - What is the temperature of the sun?

3. **Unit Conversion**:
   - Convert 100 degrees Celsius to Fahrenheit
   - Convert 1 kilometer to miles
   - Convert 1 kilogram to pounds

4. **Equation Solving**:
   - Solve the quadratic equation: x^2 + 2x + 1 = 0

## Instructions

1. Use the `query` tool for each request
2. Formulate requests in natural language
3. Present results clearly and understandably
4. Add explanations when needed

## Expected Result

The server should:
- Process all requests correctly
- Provide clear and precise answers
- Provide additional information when needed
- Handle errors appropriately 