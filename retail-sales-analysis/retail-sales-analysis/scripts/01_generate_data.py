"""Generate a Superstore-style dataset (same columns as the Kaggle 'Superstore Sales' file).
If you download the real Kaggle file, save it as data/superstore_raw.csv and SKIP this script."""
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
N = 10000
catalog = {
    "Furniture": {"Chairs": (150, .12), "Tables": (400, .02), "Bookcases": (250, .05), "Furnishings": (45, .15)},
    "Office Supplies": {"Binders": (25, .22), "Paper": (20, .25), "Storage": (90, .1), "Art": (15, .2), "Labels": (12, .3)},
    "Technology": {"Phones": (300, .15), "Accessories": (60, .2), "Copiers": (1200, .25), "Machines": (700, .03)},
}
regions = {"West": ["California", "Washington", "Oregon"], "East": ["New York", "Pennsylvania", "Ohio"],
           "Central": ["Texas", "Illinois", "Michigan"], "South": ["Florida", "Georgia", "Virginia"]}
cities = {"California": "Los Angeles", "Washington": "Seattle", "Oregon": "Portland", "New York": "New York City",
          "Pennsylvania": "Philadelphia", "Ohio": "Columbus", "Texas": "Houston", "Illinois": "Chicago",
          "Michigan": "Detroit", "Florida": "Miami", "Georgia": "Atlanta", "Virginia": "Richmond"}
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
first = ["Aarav","Priya","Rohan","Sneha","Karthik","Anita","Vikram","Meera","John","Emma","Liam","Olivia","Noah","Sophia","Ethan","Mia"]
last = ["Sharma","Reddy","Patel","Nair","Smith","Brown","Davis","Wilson","Clark","Lewis","Walker","Hall"]
customers = [(f"CU-{i:04d}", f"{rng.choice(first)} {rng.choice(last)}", str(rng.choice(segments))) for i in range(1, 801)]

rows = []
for i in range(N):
    cat = str(rng.choice(list(catalog), p=[.3, .45, .25]))
    sub = str(rng.choice(list(catalog[cat])))
    price, margin = catalog[cat][sub]
    region = str(rng.choice(list(regions), p=[.32, .28, .22, .18]))
    state = str(rng.choice(regions[region]))
    cid, cname, seg = customers[rng.integers(len(customers))]
    qty = int(rng.integers(1, 8))
    discount = float(rng.choice([0, 0, 0, .1, .2, .3, .4, .5], p=[.3,.2,.1,.12,.12,.08,.05,.03]))
    unit = price * rng.uniform(.8, 1.2)
    sales = round(unit * qty * (1 - discount), 2)
    # profit falls as discount rises (the business insight hidden in the data)
    profit = round(sales * (margin + .12 - discount * 1.0 + rng.normal(0, .04)), 2)
    od = pd.Timestamp("2021-01-01") + pd.Timedelta(days=int(rng.integers(0, 4*365)))
    mode = str(rng.choice(ship_modes, p=[.6, .2, .15, .05]))
    sd = od + pd.Timedelta(days={"Standard Class": 5, "Second Class": 3, "First Class": 2, "Same Day": 0}[mode] + int(rng.integers(0, 3)))
    rows.append([f"CA-{od.year}-{100000+i}", od.strftime("%m/%d/%Y"), sd.strftime("%m/%d/%Y"), mode, cid, cname, seg,
                 "United States", cities[state], state, region, f"{cat[:3].upper()}-{sub[:3].upper()}-{rng.integers(1000,9999)}",
                 cat, sub, f"{sub} Model {rng.integers(1,40)}", sales, qty, discount, profit])

cols = ["Order ID","Order Date","Ship Date","Ship Mode","Customer ID","Customer Name","Segment","Country","City","State",
        "Region","Product ID","Category","Sub-Category","Product Name","Sales","Quantity","Discount","Profit"]
df = pd.DataFrame(rows, columns=cols)

# make the data a little messy on purpose, so the cleaning step has real work to do
df = pd.concat([df, df.sample(60, random_state=1)], ignore_index=True)            # duplicates
df.loc[df.sample(80, random_state=2).index, "Segment"] = None                      # missing values
idx = df.sample(50, random_state=3).index
df.loc[idx, "Customer Name"] = df.loc[idx, "Customer Name"].str.upper()            # inconsistent case
idx = df.sample(40, random_state=4).index
df.loc[idx, "Region"] = " " + df.loc[idx, "Region"] + " "                          # stray spaces

Path("data").mkdir(exist_ok=True)
df.to_csv("data/superstore_raw.csv", index=False)
print(f"Created data/superstore_raw.csv with {len(df):,} rows")
