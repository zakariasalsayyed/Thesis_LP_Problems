import pulp
import datetime
# Az alaphalmazt megadom:
print(datetime.datetime.now())
base_Set = "A B C D E F G H I".split()
max_Subset_Size = len(base_Set)
# Létrehozom az összes lehetséges részhalmazt az alaphalmazon:
possible_Sets = [tuple(c) for c in pulp.allcombinations(base_Set, max_Subset_Size)]
setAll = set(possible_Sets)
# Az x vektor elemei a halmazok lesznek, csak 0-1 értéket rendelünk hozzájuk
x = pulp.LpVariable.dicts("set", possible_Sets, lowBound=0, upBound=1, cat=pulp.LpInteger)
set_Model = pulp.LpProblem("Sperner Set System Model", pulp.LpMaximize)
set_Model += pulp.lpSum([ x[it_set] for it_set in possible_Sets])
# Ebben a lépésben határozom meg a feltételeket
for subSetA in setAll:
    for subSetB in setAll:
        subSetA = set(subSetA)
        subSetB = set(subSetB)
        if subSetA.issubset(subSetB) and subSetA != subSetB:
            subSetA = tuple(sorted(tuple(subSetA)))
            subSetB = tuple(sorted(tuple(subSetB)))
            set_Model += (pulp.lpSum([x[subSetA] + x[subSetB]]) <= 1)
# Itt fut a modell megoldása
print(datetime.datetime.now())
set_Model.solve()
print(datetime.datetime.now())
# Kiírom, hogy hány halmazkombináció volt összesen és aztán felsorolom őket
print(f"The choosen sets are out of a total of {len(possible_Sets)}:")
for table in possible_Sets:
    if x[table].value() == 1.0:
        print(table)
print(datetime.datetime.now())