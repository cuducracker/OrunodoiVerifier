from cache import RCCache

cache = RCCache()

members = [

    "PAWAN KEOT",

    "NIHA KEOT",

    "SABITRI KEOT"

]

cache.save(

    "181003001234",

    members

)

print(cache.has("181003001234"))

print(cache.get("181003001234"))

print(cache.size())

cache.clear()

print(cache.size())