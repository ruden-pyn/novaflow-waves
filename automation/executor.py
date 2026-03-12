from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

def run_search(query, count):
    results = {
        "success": False,
        "query": query,
        "opened_urls": [],
        "errors": []
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            page.goto("https://duckduckgo.com")
            page.wait_for_selector("input[name=q]")
            page.fill("input[name=q]", query)
            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle")
            
            results_locator = page.locator("h2 a")
            
            for i in range(count):
                try:
                    new_page = context.new_page()
                    result_href = results_locator.nth(i).get_attribute("href")
                    
                    if result_href:
                        new_page.goto(result_href)
                        new_page.wait_for_load_state("networkidle", timeout=10000)
                        current_url = new_page.url
                        results["opened_urls"].append(current_url)
                        print(f"Opened result {i+1}: {current_url}")
                        new_page.close()
                    else:
                        error_msg = f"Result {i+1} has no URL"
                        print(error_msg)
                        results["errors"].append(error_msg)
                    
                except PlaywrightTimeout as e:
                    error_msg = f"Timeout on result {i+1}"
                    print(error_msg)
                    results["errors"].append(error_msg)
                    if 'new_page' in locals():
                        try:
                            new_page.close()
                        except:
                            pass
                    continue
                    
                except Exception as e:
                    error_msg = f"Error on result {i+1}: {str(e)}"
                    print(error_msg)
                    results["errors"].append(error_msg)
                    if 'new_page' in locals():
                        try:
                            new_page.close()
                        except:
                            pass
                    continue
            
            browser.close()
            results["success"] = len(results["opened_urls"]) > 0
            
    except Exception as e:
        results["errors"].append(f"Fatal error: {str(e)}")
    return results
