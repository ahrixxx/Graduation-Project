import os
import requests

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

SECTOR_NAME_MAP = {
    "technology": "Information Technology",
    "energy": "Energy",
    "financial_markets": "Financials",
    "healthcare": "Health Care",
}

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def get_sector_return_rate(sector_key: str) -> float:
    response = requests.get(
        ALPHA_VANTAGE_URL,
        params={
            "function": "SECTOR",
            "apikey": ALPHA_VANTAGE_API_KEY,
        },
        timeout=5,
    )
    response.raise_for_status()
    data = response.json()

    sector_name = SECTOR_NAME_MAP.get(sector_key)
    if not sector_name:
        return 0.0

    rate_str = data["Rank A: Real-Time Performance"][sector_name]
    return float(rate_str.replace("%", ""))
