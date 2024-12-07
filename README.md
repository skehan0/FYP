# FYP
My final year project repository

# Yahoo Finance
    period: data period to download (either use period parameter or use start and end) Valid periods are:
        “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
    interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
        “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
    start: If not using period – in the format (yyyy-mm-dd) or datetime.
    end: If not using period – in the format (yyyy-mm-dd) or datetime.
    prepost: Include Pre and Post regular market data in results? (Default is False)- no need usually to change this from False
    auto_adjust: Adjust all OHLC (Open/High/Low/Close prices) automatically? (Default is True)- just leave this always as true and don’t worry about it
    actions: Download stock dividends and stock splits events? (Default is True)
