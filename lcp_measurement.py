from __future__ import annotations

import time
from typing import Dict, List, Optional

from selenium import webdriver
from selenium.common.exceptions import JavascriptException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options


DEFAULT_URLS = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://github.com",
    "https://www.python.org",
    "https://stackoverflow.com",
]


def classify_lcp(lcp_seconds: float) -> str:
    if lcp_seconds <= 2.5:
        return "Good"
    if lcp_seconds <= 4.0:
        return "Needs Improvement"
    return "Poor"



def create_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Selenium Manager automatically downloads/uses a compatible driver.
    return webdriver.Chrome(options=chrome_options)



def get_lcp_for_url(driver: webdriver.Chrome, url: str, timeout: int = 20) -> Optional[float]:
    lcp_script = """
    const callback = arguments[arguments.length - 1];

    try {
        let largestContentfulPaint = null;
        let finished = false;

        const done = (value) => {
            if (!finished) {
                finished = true;
                callback(value);
            }
        };

        const observer = new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            if (entries.length > 0) {
                const lastEntry = entries[entries.length - 1];
                largestContentfulPaint = lastEntry.startTime;
            }
        });

        observer.observe({ type: 'largest-contentful-paint', buffered: true });

        const finalizeMeasurement = () => {
            setTimeout(() => {
                observer.disconnect();
                done(largestContentfulPaint);
            }, 3000);
        };

        if (document.readyState === 'complete') {
            finalizeMeasurement();
        } else {
            window.addEventListener('load', finalizeMeasurement, { once: true });
        }

        setTimeout(() => {
            observer.disconnect();
            done(largestContentfulPaint);
        }, 15000);
    } catch (error) {
        callback(null);
    }
    """

    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        lcp_ms = driver.execute_async_script(lcp_script)

        if lcp_ms is None:
            return None

        return round(float(lcp_ms) / 1000, 2)
    except (TimeoutException, JavascriptException, WebDriverException):
        return None



def collect_urls() -> List[str]:
    print("Default URLs are listed below.")
    print("You can press Enter to keep the default URL or type a new one.\n")

    final_urls: List[str] = []
    for index, default_url in enumerate(DEFAULT_URLS, start=1):
        user_input = input(f"URL {index} [{default_url}]: ").strip()
        final_urls.append(user_input if user_input else default_url)
    return final_urls



def print_results(results: List[Dict[str, object]]) -> None:
    valid_results = [result for result in results if result["lcp"] is not None]

    print("\nResults:")
    for index, result in enumerate(results, start=1):
        url = result["url"]
        lcp = result["lcp"]
        category = result["category"]

        if lcp is None:
            print(f"{index}. {url} -> Measurement failed -> N/A")
        else:
            print(f"{index}. {url} -> {lcp:.2f} s -> {category}")

    if not valid_results:
        print("\nNo valid LCP result was measured.")
        return

    average_lcp = sum(result["lcp"] for result in valid_results) / len(valid_results)
    best_result = min(valid_results, key=lambda item: item["lcp"])
    worst_result = max(valid_results, key=lambda item: item["lcp"])

    print(f"\nAverage LCP: {average_lcp:.2f} s")
    print(f"Best Result: {best_result['url']} -> {best_result['lcp']:.2f} s")
    print(f"Worst Result: {worst_result['url']} -> {worst_result['lcp']:.2f} s")



def main() -> None:
    urls = collect_urls()
    results: List[Dict[str, object]] = []

    driver = create_driver()
    try:
        for url in urls:
            print(f"\nMeasuring LCP for: {url}")
            lcp_value = get_lcp_for_url(driver, url)

            if lcp_value is None:
                results.append(
                    {
                        "url": url,
                        "lcp": None,
                        "category": "N/A",
                    }
                )
            else:
                results.append(
                    {
                        "url": url,
                        "lcp": lcp_value,
                        "category": classify_lcp(lcp_value),
                    }
                )

            time.sleep(1)
    finally:
        driver.quit()

    print_results(results)


if __name__ == "__main__":
    main()
