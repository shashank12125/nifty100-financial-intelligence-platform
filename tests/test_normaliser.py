from src.etl.normaliser import normalize_ticker, normalize_year

print(normalize_ticker(" abb "))
print(normalize_ticker("adanient"))

print(normalize_year("Mar 2014"))
print(normalize_year("Dec 2012"))
print(normalize_year("Mar-24"))
print(normalize_year("FY24"))
print(normalize_year("2023"))