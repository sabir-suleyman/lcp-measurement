# LCP Measurement with Selenium

This project measures the **Largest Contentful Paint (LCP)** performance metric for multiple web pages using Python and Selenium.

## Overview

The script allows users to input up to 5 URLs and automatically:
- Measures LCP for each page
- Classifies results as **Good**, **Needs Improvement**, or **Poor**
- Calculates **average**, **best**, and **worst** performance

## Technologies Used

- Python 3
- Selenium WebDriver
- Chrome / Chromium
- JavaScript Performance API

## How It Works

1. The user provides up to 5 URLs (or uses default ones).
2. Each page is opened using Selenium.
3. LCP value is extracted using JavaScript.
4. Results are categorized:
   - **Good**: LCP ≤ 2.5s
   - **Needs Improvement**: 2.5s < LCP ≤ 4.0s
   - **Poor**: LCP > 4.0s
5. Final statistics are calculated.

## Example Output
https://www.google.com
 -> 0.50 s -> Good
https://www.wikipedia.org
 -> 0.40 s -> Good
https://github.com
 -> 1.16 s -> Good
https://www.python.org
 -> 0.87 s -> Good
https://stackoverflow.com
 -> 2.10 s -> Good

Average LCP: 1.01 s
Best Result: https://www.wikipedia.org
 -> 0.40 s
Worst Result: https://stackoverflow.com
 -> 2.10 s


## Installation

```bash
git clone https://github.com/your-username/lcp-measurement.git
cd lcp-measurement
python3 -m venv venv
source venv/bin/activate
pip install selenium
```
## Usage
python3 lcp_measurement.py

You can either:

Press Enter to use default URLs
Or input your own URLs

## Project Structure
```
lcp-measurement/
│
├── lcp_measurement.py
├── README.md
└── report.docx
```

## Notes
LCP is one of Google's Core Web Vitals metrics.
Results may vary depending on network speed and system performance.

## 👤 Author

Sabir Suleymanli
E-mail: suleymanlisabir3@gmail.com
