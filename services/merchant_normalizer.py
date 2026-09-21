import re


# =========================================================
# MERCHANT ALIASES
# =========================================================

MERCHANT_ALIASES = {

    "Amazon": [
        "AMAZON",
        "AMZN",
        "AMAZON PAY",
        "AMAZONPAY",
        "AMAZON.IN",
        "AMZN MKTPLACE",
        "AMZN MKTP",
        "AMAZON MARKETPLACE"
    ],

    "Flipkart": [
        "FLIPKART",
        "FLIPKART INTERNET",
        "FLIPKART PAY"
    ],

    "Swiggy": [
        "SWIGGY",
        "SWIGGY INSTAMART",
        "SWIGGY FOOD"
    ],

    "Zomato": [
        "ZOMATO",
        "ZOMATO LTD",
        "ZOMATO FOOD"
    ],

    "Uber": [
        "UBER",
        "UBER INDIA",
        "UBER TRIP",
        "UBER BV"
    ],

    "Ola": [
        "OLA",
        "OLA CABS",
        "OLA CAB"
    ],

    "Rapido": [
        "RAPIDO",
        "RAPIDO BIKE",
        "RAPIDO CAB"
    ],

    "Netflix": [
        "NETFLIX",
        "NETFLIX.COM"
    ],

    "Spotify": [
        "SPOTIFY",
        "SPOTIFY INDIA"
    ],

    "YouTube": [
        "YOUTUBE",
        "YOUTUBE PREMIUM",
        "GOOGLE YOUTUBE"
    ],

    "Google": [
        "GOOGLE",
        "GOOGLE PAY",
        "GPAY",
        "G PAY"
    ],

    "PhonePe": [
        "PHONEPE",
        "PHONE PE"
    ],

    "Paytm": [
        "PAYTM",
        "PAYTM PAYMENTS",
        "PAYTM MALL"
    ],

    "Myntra": [
        "MYNTRA",
        "MYNTRA DESIGNS"
    ],

    "Ajio": [
        "AJIO",
        "AJIO.COM"
    ],

    "Meesho": [
        "MEESHO",
        "MEESHO.COM"
    ],

    "DMart": [
        "DMART",
        "DMART READY",
        "AVENUE SUPERMART"
    ],

    "Airtel": [
        "AIRTEL",
        "BHARTI AIRTEL",
        "AIRTEL PAYMENT"
    ],

    "Jio": [
        "JIO",
        "RELIANCE JIO",
        "JIO TELECOM"
    ],

    "Indian Oil": [
        "INDIAN OIL",
        "IOCL",
        "INDIANOIL"
    ],

    "BPCL": [
        "BPCL",
        "BHARAT PETROLEUM"
    ],

    "HP Petrol": [
        "HPCL",
        "HINDUSTAN PETROLEUM",
        "HP PETROL"
    ],

    "BookMyShow": [
        "BOOKMYSHOW",
        "BOOK MY SHOW"
    ],

    "PVR": [
        "PVR",
        "PVR INOX"
    ],

    "Apollo": [
        "APOLLO",
        "APOLLO PHARMACY",
        "APOLLO HOSPITAL"
    ],

    "MedPlus": [
        "MEDPLUS",
        "MEDPLUS MART"
    ],

    "LIC": [
        "LIC",
        "LIFE INSURANCE CORPORATION"
    ],

    "Zerodha": [
        "ZERODHA",
        "ZERODHA BROKING"
    ],

    "Groww": [
        "GROWW",
        "GROWW INVEST"
    ],

    "Upstox": [
        "UPSTOX",
        "UPSTOX SECURITIES"
    ],

    "MakeMyTrip": [
        "MAKEMYTRIP",
        "MAKE MY TRIP",
        "MMT"
    ],

    "Goibibo": [
        "GOIBIBO",
        "GOIBIBO.COM"
    ]
}


# =========================================================
# CLEAN MERCHANT TEXT
# =========================================================

def clean_merchant_text(text):

    if text is None:
        return ""

    text = str(text).upper()

    # Remove special characters
    text = re.sub(
        r"[^A-Z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# NORMALIZE MERCHANT
# =========================================================

def normalize_merchant(description):

    cleaned_text = clean_merchant_text(
        description
    )

    if not cleaned_text:
        return "Unknown Merchant"

    # Check known merchant aliases
    for merchant, aliases in MERCHANT_ALIASES.items():

        for alias in aliases:

            cleaned_alias = clean_merchant_text(
                alias
            )

            if cleaned_alias in cleaned_text:

                return merchant

    # If merchant is unknown,
    # return cleaned original description
    return cleaned_text


# =========================================================
# SHORT MERCHANT NAME
# =========================================================

def get_merchant_name(description):

    merchant = normalize_merchant(
        description
    )

    # Limit extremely long bank narrations
    if len(merchant) > 50:

        merchant = merchant[:50].strip()

    return merchant