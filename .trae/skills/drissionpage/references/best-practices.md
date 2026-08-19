# DrissionPage Best Practices

## Overview

This document provides best practices for using the DrissionPage skill effectively and efficiently. Following these guidelines will help you avoid common pitfalls and maximize the performance of your web automation scripts.

## Browser Control Best Practices

### 1. Resource Management

- **Always close resources**: Use `close_all()` or `close_browser()` after operations to free up system resources
- **Reuse browser instances**: Avoid creating multiple browser instances unnecessarily
- **Limit tab usage**: Keep the number of open tabs to a minimum

### 2. Performance Optimization

- **Use headless mode**: For non-interactive tasks, consider using headless mode to reduce resource usage
- **Optimize waits**: Use appropriate wait strategies instead of fixed sleeps
- **Batch operations**: Group similar operations together to reduce browser overhead

### 3. Reliability

- **Handle exceptions**: Always wrap browser operations in try-except blocks
- **Verify page loads**: Check if elements exist before interacting with them
- **Use robust selectors**: Prefer stable selectors like IDs over fragile ones like XPaths
- **Implement retries**: For flaky operations, implement retry logic with exponential backoff

### 4. Ethical Usage

- **Respect robots.txt**: Always check and follow website robots.txt rules
- **Limit request frequency**: Avoid sending too many requests in a short period
- **Identify yourself**: Use appropriate user-agent strings
- **Follow terms of service**: Comply with website terms of service

### 5. Debugging

- **Enable logging**: Use the built-in logging to track script execution
- **Take screenshots**: Capture screenshots on failure for debugging
- **Inspect network traffic**: Use browser developer tools to analyze network requests
- **Test selectors**: Verify selectors in browser developer tools before using them

## Network Request Best Practices

### 1. Request Management

- **Use session pooling**: Reuse SessionPage instances for multiple requests
- **Set timeouts**: Always specify reasonable timeouts for requests
- **Handle redirects**: Properly handle HTTP redirects
- **Manage cookies**: Use cookies appropriately for authenticated sessions

### 2. Headers and Authentication

- **Set appropriate headers**: Use realistic headers to avoid detection
- **Handle authentication**: Implement proper authentication flows
- **Rotate user agents**: Use different user agents for different requests
- **Use proxies**: Consider using proxies for high-volume scraping

### 3. Response Handling

- **Validate responses**: Always check response status codes
- **Handle different content types**: Properly handle HTML, JSON, XML, etc.
- **Parse data efficiently**: Use appropriate parsing techniques for different data formats
- **Cache responses**: Cache frequent requests to reduce network traffic

### 4. Error Handling

- **Catch HTTP errors**: Handle 4xx and 5xx errors appropriately
- **Handle network errors**: Deal with timeouts, connection errors, etc.
- **Implement circuit breakers**: Stop making requests if errors persist
- **Log errors**: Record detailed error information for debugging

## Selector Best Practices

### 1. Selector Strategies

- **Prefer specific selectors**: Use the most specific selector possible
- **Fallback strategies**: Implement multiple selector strategies for robustness
- **Avoid dynamic selectors**: Stay away from selectors that change frequently
- **Use data attributes**: Prefer data-* attributes for stable element identification

### 2. Selector Examples

| Element Type | Recommended Selector | Example |
|-------------|---------------------|---------|
| Buttons | ID or text selector | `#submit` or `text:Submit` |
| Input fields | ID or name attribute | `#username` or `name:email` |
| Navigation links | Text or CSS selector | `text:Home` or `.nav-link` |
| Forms | ID or class selector | `#login-form` or `.form-container` |
| Tables | Class or tag selector | `.data-table` or `tag:table` |

### 3. Selector Testing

- **Test in browser**: Verify selectors in browser developer tools
- **Use selector playgrounds**: Use browser extensions to test selectors
- **Validate across browsers**: Test selectors in different browsers
- **Document selectors**: Keep a record of important selectors

## Code Organization Best Practices

### 1. Modularity

- **Separate concerns**: Split code into logical modules
- **Use functions**: Encapsulate reusable code in functions
- **Create classes**: Use classes for complex functionality
- **Organize by feature**: Group code by feature or functionality

### 2. Readability

- **Use descriptive names**: Choose meaningful function and variable names
- **Add comments**: Document complex logic and important decisions
- **Follow PEP 8**: Adhere to Python coding standards
- **Use type hints**: Add type annotations for better readability

### 3. Testing

- **Write unit tests**: Test individual components
- **Write integration tests**: Test end-to-end workflows
- **Use mocks**: Mock external dependencies
- **Test edge cases**: Test boundary conditions and error scenarios

### 4. Deployment

- **Use virtual environments**: Isolate dependencies
- **Document dependencies**: Use requirements.txt or poetry
- **Version control**: Use git for version management
- **Continuous integration**: Implement CI/CD pipelines

## Common Use Cases and Patterns

### 1. Form Submission

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Navigate to login page
skills.browser_navigate("https://example.com/login")

# Find form elements
username_field = skills.browser_client.find_element("#username")
password_field = skills.browser_client.find_element("#password")
submit_button = skills.browser_client.find_element("#submit")

# Fill form
username_field.input("user@example.com")
password_field.input("password123")

# Submit form
submit_button.click()

# Verify login
skills.close_all()
```

### 2. Data Extraction

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Navigate to data page
skills.browser_navigate("https://example.com/data")

# Extract data
rows = skills.browser_client.find_elements(".data-row")
data = []

for row in rows:
    cells = row.eles(".data-cell")
    row_data = [cell.text for cell in cells]
    data.append(row_data)

print(data)
skills.close_all()
```

### 3. API Interaction

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Get data from API
response = skills.http_get("https://api.example.com/data")
print(response['content'])

# Post data to API
payload = {"key": "value", "number": 42}
response = skills.http_post("https://api.example.com/data", json=payload)
print(response['content'])
skills.close_all()
```

### 4. Pagination Handling

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Navigate to first page
skills.browser_navigate("https://example.com/products")

# Process pages
while True:
    # Extract products
    products = skills.browser_client.find_elements(".product")
    print(f"Found {len(products)} products")
    
    # Check for next page
    try:
        next_button = skills.browser_client.find_element(".next-page")
        next_button.click()
    except:
        # No more pages
        break

skills.close_all()
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Browser not starting | Chrome/Chromium not installed | Install Chrome/Chromium |
| Element not found | Selector incorrect or page not loaded | Fix selector or add wait |
| Network request failed | Invalid URL or network issue | Check URL and network connection |
| Page loading slowly | Network issues or heavy page | Increase timeout or optimize page |
| Script blocked | Website detecting automation | Use headless mode, rotate user agents, or use proxies |
| Memory usage high | Too many browser instances or tabs | Close unused instances and tabs |
| Authentication failed | Invalid credentials or CAPTCHA | Use correct credentials or implement CAPTCHA solving |

### Debugging Steps

1. **Reproduce the issue**: Try to reproduce the problem consistently
2. **Check logs**: Look at the generated logs for clues
3. **Inspect elements**: Use browser developer tools to inspect elements
4. **Test selectors**: Verify selectors in browser developer tools
5. **Check network traffic**: Analyze network requests and responses
6. **Isolate the issue**: Narrow down the problem to a specific part of the code
7. **Try different approaches**: Experiment with different methods
8. **Consult documentation**: Check DrissionPage documentation for solutions
9. **Ask for help**: Seek assistance from the community if needed

## Performance Optimization Tips

### Browser Control Optimization

- **Use headless mode**: For non-visual tasks
- **Limit extensions**: Disable unnecessary browser extensions
- **Optimize JavaScript**: Block unnecessary JavaScript execution
- **Use CDP protocol**: For more efficient browser control
- **Batch operations**: Group similar operations together

### Network Optimization

- **Use HTTP/2**: Take advantage of HTTP/2 features
- **Compress data**: Use gzip compression for requests and responses
- **Minimize redirects**: Avoid unnecessary redirects
- **Use persistent connections**: Keep connections alive
- **Optimize DNS lookups**: Cache DNS responses

### Code Optimization

- **Use async/await**: For concurrent operations
- **Optimize loops**: Use efficient loop structures
- **Minimize memory usage**: Avoid unnecessary object creation
- **Use generators**: For memory-efficient data processing
- **Profile code**: Identify and fix performance bottlenecks

## Conclusion

By following these best practices, you can create more reliable, efficient, and maintainable web automation scripts using the DrissionPage skill. Remember to always use these tools responsibly and ethically, respecting website terms of service and legal requirements.

Happy automating!
