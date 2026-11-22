
import gdown
from pathlib import Path

FILE_ID = "19RP-1bvzuPd8SWHNKqMx-6hbhsJWjymu"
OUTPUT = Path("data/05_pharmacy_sales_data.csv")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

url = f"https://drive.google.com/uc?id={FILE_ID}"
gdown.download(url, str(OUTPUT), quiet=False)

print(f"Sales dataset downloaded to {OUTPUT}")
