# Testing Strategy for Bookstore API

## Overview

This document outlines the testing strategy employed for the Bookstore API, covering unit tests, integration tests, reliability, maintainability, and challenges encountered.

## Approach

### Unit Tests

* **Isolation:**
    * Unit tests were designed to test individual components (functions, classes) in isolation.
    * `pytest-mock` and `unittest.mock` were used to mock external dependencies, primarily database interactions and JWT decoding.
    * This ensured that tests focused solely on the logic of the unit under test.
* **Coverage:**
    * Efforts were made to achieve high code coverage (aiming for 80% or more).
    * Test cases were written to cover various scenarios, including normal execution paths, edge cases, and error conditions.
* **pytest Framework:**
    * `pytest` was chosen for its simplicity, powerful features (fixtures, parametrization), and excellent plugin ecosystem.
    * Fixtures were used to set up and tear down test environments, reducing code duplication.

### Integration Tests

* **End-to-End Testing:**
    * Integration tests were designed to verify the interaction between different components of the API, including database interactions, authentication, and API endpoints.
    * `httpx` was used to make HTTP requests to the FastAPI application, simulating real-world usage.
* **CRUD Operations and Authentication:**
    * Test cases were written to cover all major CRUD operations (Create, Read, Update, Delete) for book resources.
    * Authentication flows (signup, login, JWT validation) were thoroughly tested.
* **Test Database:**
    * An in memory sqlite database was used, to ensure that the main database was not effected by testing.
    * This also ensures that each test has a clean slate.
* **Asynchronous Testing:**
    * All integration tests were written to be asynchronous, due to the use of async httpx, and the async nature of the fastAPI application.

## Reliability and Maintainability

* **Clear and Descriptive Tests:**
    * Test functions and assertions were written with clear and descriptive names, making it easy to understand their purpose.
* **Test Organization:**
    * Tests were organized into logical modules and files (e.g., `tests/unit`, `tests/integration`).
* **Fixtures and Helper Functions:**
    * Fixtures were used to set up reusable test environments and data.
    * Helper functions were created to reduce code duplication and improve readability.
* **Continuous Integration:**
    * GitHub Actions was configured to automatically run tests on every push, ensuring that changes do not introduce regressions.
    * Code coverage reports are generated, and checked by the CI.

## Challenges and Solutions

* **Mocking Asynchronous Database Interactions:**
    * **Challenge:** Mocking asynchronous database operations required careful use of `pytest-mock` and `unittest.mock`.
    * **Solution:** Thoroughly studied mocking techniques, and created many different test cases to ensure that the mocks were working as expected.
* **Ensuring Comprehensive Test Coverage:**
    * **Challenge:** Covering all edge cases and ensuring high code coverage required a systematic approach.
    * **Solution:** Used code coverage tools to identify gaps in test coverage and wrote additional test cases to address them.
* **Setting up and Tearing down Test Databases:**
    * **Challenge:** Ensuring a clean test environment for each integration test.
    * **Solution:** Used in memory sqlite databases for testing.
* **JWT token verification in unit tests:**
    * **Challenge:** Properly mocking the JWT decode function, and handling exceptions.
    * **Solution:** Used patch to mock the jwt.decode function. Added tests to handle the different exceptions that could be thrown.
* **Correcting file pathing for CI/CD:**
    * **Challenge:** Ensuring the CI/CD pipeline correctly navigated the project structure to find the needed files.
    * **Solution:** Carefully adjusted the pathing in the github actions file, and tested the CI/CD pipeline until it ran without errors.

## Local Test Execution

To run the tests locally, follow these steps:

1.  Navigate to the project directory.
2.  Install the required dependencies: `pip install -r bookstore/requirements.txt` and `pip install -r bookstore/requirements-dev.txt`
3.  Run the tests using `pytest`: `pytest bookstore/tests` or `pytest --cov=bookstore/ --cov-report term-missing bookstore/tests/unit`

This testing strategy ensures that the Bookstore API is thoroughly tested, reliable, and maintainable.