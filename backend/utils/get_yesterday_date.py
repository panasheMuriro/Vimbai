from datetime import datetime, timedelta

def get_yesterday_date(site_key: str) -> str:
    """
    Returns yesterday's date in the specific format required for each site.

    Supported site_key values:
    - 'pindula'        -> /YYYY/MM/DD/
    - 'zimeye'         -> DD Month, YYYY
    - 'new_zimbabwe'   -> DDth Month YYYY
    - 'news_day'       -> Mon. DD, YYYY
    - 'news_dze_zimbabwe' -> Weekday, Month DD, YYYY
    """
    
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    day = yesterday.day

    def get_day_suffix(d):
        if 11 <= d <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

    if site_key == "pindula":
        return yesterday.strftime("/%Y/%m/%d/")

    elif site_key == "zimeye":
        return yesterday.strftime(f"%-d %B, %Y") if not is_windows() else yesterday.strftime(f"{day} %B, %Y")

    elif site_key == "new_zimbabwe":
        suffix = get_day_suffix(day)
        return yesterday.strftime(f"%-d{suffix} %B %Y") if not is_windows() else f"{day}{suffix} {yesterday.strftime('%B %Y')}"

    elif site_key == "news_day":
        return yesterday.strftime(f"%b. {day}, %Y")

    elif site_key == "news_dze_zimbabwe":
        return yesterday.strftime(f"%A, %B {day}, %Y")

    else:
        raise ValueError(f"Unsupported site_key: {site_key}")

def is_windows():
    import platform
    return platform.system().lower().startswith("win")

# Example usage:
# print(get_yesterday_date("pindula"))
# print(get_yesterday_date("zimeye"))
# print(get_yesterday_date("new_zimbabwe"))
# print(get_yesterday_date("news_day"))
# print(get_yesterday_date("news_dze_zimbabwe"))
