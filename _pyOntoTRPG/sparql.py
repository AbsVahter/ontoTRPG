from rdflib import Graph

g = Graph()
filepath = r"D:\Ontologies\Created ontologies\trpgontologies\gumshoe\cthulhu_confidential\inf.ttl"
g.parse(filepath)

query = """
PREFIX p:  <https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/gumshoe/cthulhu_confidential/PELGOC01.ttl#>
PREFIX bno: <https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/_basic/BasicNarrativeOnto.ttl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
 
SELECT ?b
WHERE {
    p:fatal_frequencies p:opener ?opener .
    ?opener bno:consequence+ ?a .
    ?a rdfs:label ?b .
}
ORDER BY ?b
"""

result = g.query(query)

print("")
for row in result:
    print(row.b)
