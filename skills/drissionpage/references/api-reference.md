# DrissionPage API Reference

## Overview

This document provides a reference for the DrissionPage API used in the drissionpage skill. It covers the main classes and methods used for browser control and network requests.

## Core Classes

### DrissionPageSkills

The main class that encapsulates all functionality of the drissionpage skill.

#### Methods

- **init_browser()**
  - Initializes and returns a Chromium browser instance
  - Returns: Chromium browser object

- **init_session()**
  - Initializes and returns a SessionPage instance for network requests
  - Returns: SessionPage object

- **baidu_search(keyword)**
  - Performs a Baidu search for the given keyword
  - Args: keyword (str) - Search term
  - Returns: List[str] - Search result titles

- **http_get(url, headers=None)**
  - Sends an HTTP GET request to the specified URL
  - Args:
    - url (str) - Request URL
    - headers (dict, optional) - Request headers
  - Returns: dict - Response data

- **http_post(url, data=None, json=None, headers=None)**
  - Sends an HTTP POST request to the specified URL
  - Args:
    - url (str) - Request URL
    - data (dict, optional) - Form data
    - json (dict, optional) - JSON data
    - headers (dict, optional) - Request headers
  - Returns: dict - Response data

- **browser_navigate(url)**
  - Navigates to the specified URL using the browser
  - Args: url (str) - URL to navigate to
  - Returns: str - Page title

- **get_element_text(url, selector)**
  - Gets text content from a specific element on the page
  - Args:
    - url (str) - Page URL
    - selector (str) - Element selector
  - Returns: str - Element text

- **close_browser()**
  - Closes the browser instance

- **close_session()**
  - Closes the session instance

- **close_all()**
  - Closes all resources (browser and session)

## Chromium Browser Control

### Browser Instance

- **Chromium()**
  - Creates a new Chromium browser instance
  - Returns: Chromium browser object

- **browser.latest_tab**
  - Gets the most recently active tab
  - Returns: Tab object

- **browser.new_tab(url)**
  - Creates a new tab and navigates to the specified URL
  - Args: url (str) - URL to navigate to
  - Returns: Tab object

- **browser.get_tab(title)**
  - Gets a tab by title
  - Args: title (str) - Tab title
  - Returns: Tab object

- **browser.quit()**
  - Closes the browser

### Tab Operations

- **tab.get(url)**
  - Navigates to the specified URL
  - Args: url (str) - URL to navigate to

- **tab.title**
  - Gets the page title
  - Returns: str - Page title

- **tab.refresh()**
  - Refreshes the page

- **tab.back()**
  - Navigates back in history

- **tab.forward()**
  - Navigates forward in history

- **tab.ele(selector)**
  - Finds an element by selector
  - Args: selector (str) - Element selector
  - Returns: Element object

- **tab.eles(selector)**
  - Finds multiple elements by selector
  - Args: selector (str) - Element selector
  - Returns: List[Element] - List of element objects

### Element Operations

- **element.click()**
  - Clicks the element

- **element.input(text)**
  - Enters text into the element
  - Args: text (str) - Text to enter

- **element.text**
  - Gets the element's text content
  - Returns: str - Element text

## SessionPage Network Requests

### Session Instance

- **SessionPage()**
  - Creates a new SessionPage instance for network requests
  - Returns: SessionPage object

- **session.headers**
  - Gets or sets request headers
  - Type: dict

- **session.get(url)**
  - Sends an HTTP GET request
  - Args: url (str) - Request URL

- **session.post(url, data=None, json=None)**
  - Sends an HTTP POST request
  - Args:
    - url (str) - Request URL
    - data (dict, optional) - Form data
    - json (dict, optional) - JSON data

- **session.html**
  - Gets the response HTML content
  - Returns: str - HTML content

## Selector Syntax

DrissionPage supports various selector strategies:

- **CSS selectors**: `#id`, `.class`, `tag`
- **Tag selector**: `tag:tag_name`
- **Text selector**: `text:text_content`
- **XPath selector**: `xpath:xpath_expression`

## Error Handling

The skill includes the following exception classes:

- **DrissionPageSkillError**: Base exception for skill errors
- **BrowserError**: Errors related to browser operations
- **NetworkError**: Errors related to network requests
- **ElementNotFoundError**: Error when an element cannot be found

## Usage Examples

### Browser Control Example

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Navigate to a page
title = skills.browser_navigate("https://httpbin.org/get")
print(f"Page title: {title}")

# Get element text
text = skills.get_element_text("https://httpbin.org/html", "body")
print(f"Element text: {text[:100]}...")

# Close resources
skills.close_all()
```

### Network Request Example

```python
from drissionpage_skill import DrissionPageSkills

skills = DrissionPageSkills()

# Send GET request
response = skills.http_get("https://httpbin.org/get")
print(f"Response content: {response['content'][:100]}...")

# Send POST request
response = skills.http_post("https://httpbin.org/post", data={"key": "value"})
print(f"Response content: {response['content'][:100]}...")

# Close resources
skills.close_all()
```

## Best Practices

1. **Resource Management**: Always close resources after use with `close_all()`
2. **Error Handling**: Catch exceptions to handle unexpected situations
3. **Selector Strategy**: Use appropriate selector strategies for different elements
4. **Request Frequency**: Avoid sending too many requests in a short period
5. **Browser Performance**: Close unnecessary tabs and browser instances

## Troubleshooting

### Common Issues

1. **Browser Not Starting**: Ensure Chrome/Chromium is installed
2. **Element Not Found**: Use correct selector syntax and wait for page load
3. **Network Errors**: Check URL validity and network connection
4. **Request Timeouts**: Adjust timeout settings for slow connections

### Debugging Tips

- Enable logging to see detailed operation information
- Use try-except blocks to catch and handle exceptions
- Test selectors in browser developer tools before using them
- Check network responses for error messages

## Reference

- DrissionPage Official Documentation: https://www.drissionpage.cn/
- Python Official Documentation: https://docs.python.org/
