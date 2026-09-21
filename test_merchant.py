from services.merchant_normalizer import normalize_merchant


test_merchants = [
    "AMAZON",
    "AMZN",
    "AMAZON PAY",
    "AMZN MKTPLACE",
    "FLIPKART",
    "SWIGGY INSTAMART",
    "UBER INDIA",
    "NETFLIX.COM",
    "RELIANCE JIO",
    "BHARTI AIRTEL",
    "IOCL",
    "ZERODHA BROKING",
    "RANDOM LOCAL SHOP"
]


for merchant in test_merchants:

    result = normalize_merchant(merchant)

    print(
        f"{merchant:25} -> {result}"
    )