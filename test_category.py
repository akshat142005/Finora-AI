from services.category_model import predict_category_with_confidence


test_transactions = [
    "SWIGGY ORDER",
    "AMAZON PURCHASE",
    "UBER TRIP",
    "NETFLIX SUBSCRIPTION",
    "ELECTRICITY BILL",
    "APOLLO PHARMACY",
    "UDEMY COURSE",
    "MAKEMYTRIP HOTEL",
    "GROWW SIP",
    "LIC PREMIUM",
    "ATM CASH WITHDRAWAL",
    "SALARY CREDIT",
    "UNKNOWN XYZ PAYMENT"
]


for transaction in test_transactions:

    category, confidence = predict_category_with_confidence(
        transaction
    )

    print(
        f"{transaction:30} -> "
        f"{category:20} "
        f"Confidence: {confidence:.2f}"
    )