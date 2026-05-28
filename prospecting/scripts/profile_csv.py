import csv, collections, sys
csv.field_size_limit(sys.maxsize)
CSV="data/us-software-saas-companies-cleaned.csv"
ind=collections.Counter(); sub=collections.Counter(); fund=collections.Counter()
size=collections.Counter(); country=collections.Counter(); n=0
with open(CSV, newline='', encoding='utf-8', errors='replace') as f:
    r=csv.DictReader(f)
    for row in r:
        n+=1
        ind[row.get('Industry','')]+=1
        sub[row.get('SubIndustry','')]+=1
        fund[row.get('Total Funding Range','')]+=1
        size[row.get('Employee Size Range','')]+=1
        country[row.get('Country','')]+=1
print("TOTAL ROWS:",n)
print("\n== Country (top 8) =="); [print(f"{c[:30]:32} {v}") for c,v in country.most_common(8)]
print("\n== Total Funding Range (all values) =="); [print(f"{c[:34]:36} {v}") for c,v in fund.most_common(30)]
print("\n== Employee Size Range (all) =="); [print(f"{c[:30]:32} {v}") for c,v in size.most_common(20)]
print("\n== Industry (top 35) =="); [print(f"{c[:40]:42} {v}") for c,v in ind.most_common(35)]
