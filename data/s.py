
import requests
from bs4 import BeautifulSoup


def get_investing_ratios_psx(company_name):
    try:
        # Construct a URL for the PSX page for the company (you'll need the correct URL structure)
        base_url = "https://dps.psx.com.pk/company/{company_name}/"
        # search_url = f"{base_url}{company_name.replace(' ', '-')}"

        # Send a request to the webpage
        response = requests.get(base_url)

        # Check if the page was fetched successfully
        print(response.text)
        if response.status_code == 200:
            # Parse the HTML of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the relevant financial data from the page
            # (Note: The actual HTML tags/classes will depend on the page structure. Adjust accordingly.)

            ratios = {
                "Market Cap": "N/A",
                "PE Ratio": "N/A",
                "EPS": "N/A",
                "Dividend Yield": "N/A",
                "Price to Book Ratio": "N/A",
                "52 Week High": "N/A",
                "52 Week Low": "N/A",
                "Beta": "N/A",
                "Enterprise Value": "N/A",
            }

            # Assuming the ratios are in table rows <tr>, loop through them and extract values
            for row in soup.find_all("tr"):
                columns = row.find_all("td")
                if len(columns) == 2:
                    key = columns[0].text.strip()
                    value = columns[1].text.strip()
                    if key in ratios:
                        ratios[key] = value

            # Print the extracted ratios
            print(f"--- Investing Ratios for {company_name} ---")
            for ratio, value in ratios.items():
                print(f"{ratio}: {value}")
        else:
            print(
                f"Error: Couldn't retrieve data for {company_name}. HTTP Status Code: {response.status_code}"
            )

    except Exception as e:
        print(f"Error: Could not retrieve data for {company_name}. Reason: {e}")


if __name__ == "__main__":
    company_name = (
        input("Enter the company's name (as listed on PSX): ").strip().title()
    )
    get_investing_ratios_psx(company_name)
exit()
import yfinance as yf


def get_investing_ratios(company_name):
    try:
        # Download the company data using yfinance
        company = yf.Ticker(company_name)
        stock_info = company.info

        # Extract important ratios and financial data
        print(
            f"--- Investing Ratios for {stock_info.get('longName', company_name)} ---"
        )
        print(f"Market Cap: {stock_info.get('marketCap', 'N/A')}")
        print(f"PE Ratio: {stock_info.get('trailingPE', 'N/A')}")
        print(f"EPS (Earnings Per Share): {stock_info.get('trailingEps', 'N/A')}")
        print(f"Dividend Yield: {stock_info.get('dividendYield', 'N/A')}")
        print(f"Price to Book Ratio: {stock_info.get('priceToBook', 'N/A')}")
        print(f"52 Week High: {stock_info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52 Week Low: {stock_info.get('fiftyTwoWeekLow', 'N/A')}")
        print(f"Beta: {stock_info.get('beta', 'N/A')}")
        print(f"Enterprise Value: {stock_info.get('enterpriseValue', 'N/A')}")
    except Exception as e:
        print(f"Error: Could not retrieve data for {company_name}. Reason: {e}")


if __name__ == "__main__":
    company_name = (
        input("Enter the company's stock ticker symbol (e.g., AAPL for Apple): ")
        .strip()
        .upper()
    )
    get_investing_ratios(company_name)

exit()
import pyautogui as gui
import time

time.sleep(10)
while True:
    gui.click()
    time.sleep(5)
