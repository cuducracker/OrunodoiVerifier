from matcher import NameMatcher

matcher = NameMatcher(70)

family = [

    "PAWAN KEOT",

    "NIHA KEOT",

    "SANJUMONI KEOT",

    "SABITRI KEOT"

]

result = matcher.compare(

    "PAWAN KUMAR KEOT",

    family

)

print(result)