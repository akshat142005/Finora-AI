import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# =========================================================
# TRAINING DATA
# =========================================================

training_data = [

    # Food
    ("SWIGGY", "Food"),
    ("ZOMATO", "Food"),
    ("DOMINOS", "Food"),
    ("PIZZA HUT", "Food"),
    ("MCDONALDS", "Food"),
    ("KFC", "Food"),
    ("RESTAURANT", "Food"),
    ("CAFE", "Food"),
    ("FOOD", "Food"),
    ("DUNZO FOOD", "Food"),

    # Transport
    ("UBER", "Transport"),
    ("OLA", "Transport"),
    ("RAPIDO", "Transport"),
    ("METRO", "Transport"),
    ("IRCTC", "Transport"),
    ("INDIAN OIL", "Transport"),
    ("HP PETROL", "Transport"),
    ("BPCL", "Transport"),
    ("PETROL", "Transport"),
    ("FUEL", "Transport"),

    # Shopping
    ("AMAZON", "Shopping"),
    ("FLIPKART", "Shopping"),
    ("MYNTRA", "Shopping"),
    ("AJIO", "Shopping"),
    ("MEESHO", "Shopping"),
    ("SHOPPING", "Shopping"),
    ("RELIANCE RETAIL", "Shopping"),
    ("DMART", "Shopping"),
    ("WALMART", "Shopping"),

    # Bills
    ("ELECTRICITY", "Bills"),
    ("ELECTRICITY BILL", "Bills"),
    ("WATER BILL", "Bills"),
    ("GAS BILL", "Bills"),
    ("MOBILE BILL", "Bills"),
    ("AIRTEL", "Bills"),
    ("JIO", "Bills"),
    ("VI ", "Bills"),
    ("BROADBAND", "Bills"),
    ("INTERNET", "Bills"),
    ("RENT", "Bills"),

    # Entertainment
    ("NETFLIX", "Entertainment"),
    ("PRIME VIDEO", "Entertainment"),
    ("HOTSTAR", "Entertainment"),
    ("SPOTIFY", "Entertainment"),
    ("YOUTUBE PREMIUM", "Entertainment"),
    ("BOOKMYSHOW", "Entertainment"),
    ("PVR", "Entertainment"),
    ("INOX", "Entertainment"),
    ("MOVIE", "Entertainment"),
    ("GAME", "Entertainment"),

    # Salary
    ("SALARY", "Salary"),
    ("PAYROLL", "Salary"),
    ("MONTHLY SALARY", "Salary"),
    ("SALARY CREDIT", "Salary"),
    ("EMPLOYER", "Salary"),

    # Refund
    ("REFUND", "Refund"),
    ("CASHBACK", "Refund"),
    ("REVERSAL", "Refund"),
    ("RETURN", "Refund"),

    # Healthcare
    ("HOSPITAL", "Healthcare"),
    ("PHARMACY", "Healthcare"),
    ("MEDICAL", "Healthcare"),
    ("APOLLO", "Healthcare"),
    ("MEDPLUS", "Healthcare"),
    ("DOCTOR", "Healthcare"),
    ("CLINIC", "Healthcare"),

    # Education
    ("COLLEGE", "Education"),
    ("UNIVERSITY", "Education"),
    ("SCHOOL", "Education"),
    ("COURSE", "Education"),
    ("UDEMY", "Education"),
    ("COURSERA", "Education"),
    ("EDUCATION", "Education"),
    ("EXAM FEE", "Education"),

    # Travel
    ("HOTEL", "Travel"),
    ("BOOKING.COM", "Travel"),
    ("MAKEMYTRIP", "Travel"),
    ("GOIBIBO", "Travel"),
    ("AIRBNB", "Travel"),
    ("FLIGHT", "Travel"),
    ("AIRLINES", "Travel"),
    ("TRAVEL", "Travel"),

    # Investments
    ("MUTUAL FUND", "Investment"),
    ("SIP", "Investment"),
    ("ZERODHA", "Investment"),
    ("GROWW", "Investment"),
    ("UPSTOX", "Investment"),
    ("DEMAT", "Investment"),
    ("STOCK", "Investment"),
    ("INVESTMENT", "Investment"),

    # Insurance
    ("INSURANCE", "Insurance"),
    ("LIC", "Insurance"),
    ("POLICY", "Insurance"),
    ("PREMIUM", "Insurance"),

    # ATM / Cash
    ("ATM", "Cash Withdrawal"),
    ("CASH WITHDRAWAL", "Cash Withdrawal"),
    ("CASH WITHDRAW", "Cash Withdrawal"),

    # Other income
    ("INTEREST CREDIT", "Other Income"),
    ("BONUS", "Other Income"),
    ("INCENTIVE", "Other Income"),
]


training_df = pd.DataFrame(
    training_data,
    columns=["description", "category"]
)


# =========================================================
# ML MODEL
# =========================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000
        )
    )
])


model.fit(
    training_df["description"],
    training_df["category"]
)


# =========================================================
# MERCHANT / KEYWORD RULES
# =========================================================

CATEGORY_KEYWORDS = {

    "Food": [
        "SWIGGY",
        "ZOMATO",
        "DOMINOS",
        "PIZZA",
        "KFC",
        "MCDONALDS",
        "RESTAURANT",
        "CAFE",
        "FOOD"
    ],

    "Transport": [
        "UBER",
        "OLA",
        "RAPIDO",
        "METRO",
        "PETROL",
        "FUEL",
        "BPCL",
        "HPCL",
        "INDIAN OIL"
    ],

    "Shopping": [
        "AMAZON",
        "FLIPKART",
        "MYNTRA",
        "AJIO",
        "MEESHO",
        "DMART",
        "SHOPPING"
    ],

    "Bills": [
        "ELECTRICITY",
        "WATER BILL",
        "GAS BILL",
        "MOBILE BILL",
        "BROADBAND",
        "INTERNET",
        "RENT",
        "AIRTEL",
        "JIO"
    ],

    "Entertainment": [
        "NETFLIX",
        "SPOTIFY",
        "HOTSTAR",
        "PRIME VIDEO",
        "BOOKMYSHOW",
        "PVR",
        "INOX",
        "MOVIE"
    ],

    "Healthcare": [
        "HOSPITAL",
        "PHARMACY",
        "MEDICAL",
        "APOLLO",
        "MEDPLUS",
        "DOCTOR",
        "CLINIC"
    ],

    "Education": [
        "COLLEGE",
        "UNIVERSITY",
        "SCHOOL",
        "UDEMY",
        "COURSERA",
        "COURSE",
        "EDUCATION",
        "EXAM FEE"
    ],

    "Travel": [
        "HOTEL",
        "BOOKING.COM",
        "MAKEMYTRIP",
        "GOIBIBO",
        "AIRBNB",
        "FLIGHT",
        "AIRLINES",
        "TRAVEL"
    ],

    "Investment": [
        "MUTUAL FUND",
        "SIP",
        "ZERODHA",
        "GROWW",
        "UPSTOX",
        "DEMAT",
        "STOCK",
        "INVESTMENT"
    ],

    "Insurance": [
        "INSURANCE",
        "LIC",
        "POLICY",
        "PREMIUM"
    ],

    "Cash Withdrawal": [
        "ATM",
        "CASH WITHDRAWAL",
        "CASH WITHDRAW"
    ],

    "Salary": [
        "SALARY",
        "PAYROLL",
        "MONTHLY SALARY",
        "SALARY CREDIT"
    ],

    "Refund": [
        "REFUND",
        "CASHBACK",
        "REVERSAL",
        "RETURN"
    ]
}


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_description(description):

    if description is None:
        return ""

    description = str(description).upper()

    description = re.sub(
        r"\s+",
        " ",
        description
    )

    return description.strip()


# =========================================================
# RULE-BASED CATEGORY
# =========================================================

def rule_based_category(description):

    description = clean_description(description)

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in description:
                return category

    return None


# =========================================================
# ML CATEGORY
# =========================================================

def predict_category(description):

    description = clean_description(description)

    if not description:
        return "Other"

    # First use merchant/keyword rules
    rule_category = rule_based_category(description)

    if rule_category:
        return rule_category

    # Otherwise use ML
    try:

        prediction = model.predict(
            [description]
        )[0]

        return prediction

    except Exception:
        return "Other"


# =========================================================
# CATEGORY CONFIDENCE
# =========================================================

def predict_category_with_confidence(description):

    description = clean_description(description)

    if not description:
        return "Other", 0.0

    rule_category = rule_based_category(description)

    if rule_category:
        return rule_category, 1.0

    try:

        probabilities = model.predict_proba(
            [description]
        )[0]

        max_probability = max(probabilities)

        prediction = model.classes_[
            probabilities.argmax()
        ]

        return prediction, float(max_probability)

    except Exception:

        return "Other", 0.0