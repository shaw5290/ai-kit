---
name: drissionpage
description: Web automation and network request tool based on DrissionPage. Use when you need to control browsers (Chromium) for web interaction or send HTTP/HTTPS requests (SessionPage) to servers. Supports element manipulation, form submission, and network data retrieval.
---

# DrissionPage

## Overview

DrissionPage is a powerful web automation tool that combines browser control and network request capabilities. This skill enables you to control Chromium browsers for web interaction and send HTTP/HTTPS requests directly to servers using SessionPage.

## Quick Start

### Basic Usage

```python
from drissionpage_skill import DrissionPageSkills

# Create skill instance
skills = DrissionPageSkills()

# 1. Baidu search
results = skills.baidu_search("DrissionPage")
print("Search results:")
for i, result in enumerate(results[:5], 1):
    print(f"{i}. {result}")

# 2. HTTP GET request
response = skills.http_get("https://httpbin.org/get")
print("\nGET request result:")
print(response['content'][:200] + "...")

# 3. HTTP POST request
response = skills.http_post("https://httpbin.org/post", data={"key": "value"})
print("\nPOST request result:")
print(response['content'][:200] + "...")

# 4. Browser navigation
title = skills.browser_navigate("https://httpbin.org/get")
print("\nPage title:")
print(title)

# 5. Get element text
text = skills.get_element_text("https://httpbin.org/html", "body")
print("\nPage content:")
print(text[:200] + "...")

# Close all resources
skills.close_all()
```

## Core Capabilities

### 1. Browser Control

- **Browser Instance Management**: Start and close Chromium browsers
- **Tab Operations**: Create new tabs, switch between tabs
- **Page Navigation**: Visit URLs, refresh pages, navigate back/forward
- **Element Interaction**: Locate elements, click, input text, submit forms
- **Page Information**: Get page title, source code

### 2. Network Requests

- **HTTP GET**: Send GET requests to retrieve data
- **HTTP POST**: Send POST requests with form data or JSON
- **Request Headers**: Customize request headers
- **Response Handling**: Process response content and headers

### 3. Skill Examples

- **Baidu Search**: Search for keywords on Baidu and return results
- **Page Navigation**: Visit websites and get page titles
- **Element Text Extraction**: Get text content from specific elements
- **HTTP Requests**: Send and receive data via HTTP/HTTPS

## Installation

### Prerequisites

- Python 3.12.9
- Anaconda environment management
- DrissionPage 4.1.1.2

### Setup Steps

1. Create Python environment:
   ```bash
   conda create -n py312_9 python=3.12.9
   conda activate py312_9
   ```

2. Install dependencies:
   ```bash
   pip install DrissionPage
   ```

## Usage Guidelines

### Browser Control Best Practices

- Allow time for browser startup
- Respect website terms of service
- Handle exceptions gracefully
- Close resources after use

### Network Request Best Practices

- Follow robots.txt guidelines
- Avoid excessive requests
- Handle rate limiting
- Validate input and output

## Troubleshooting

### Common Issues

1. **Browser Not Starting**:
   - Check if Chrome/Chromium is installed
   - Verify network connectivity
   - Try restarting the environment

2. **Element Not Found**:
   - Use correct selector syntax
   - Wait for page to load completely
   - Try different selector strategies

3. **Network Request Failures**:
   - Check URL validity
   - Verify network connection
   - Handle HTTP errors appropriately

## Resources

This skill includes the following resources:

### references/
- **api-reference.md**: DrissionPage API reference
- **best-practices.md**: Usage best practices

### assets/
- **example-scripts/**: Sample code snippets

---

**Note**: This skill is designed for educational and legitimate web automation purposes only. Please use responsibly and respect website terms of service.