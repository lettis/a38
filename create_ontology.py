from rdflib import Graph, Literal, Namespace, BNode
from rdflib.namespace import RDF, RDFS, XSD

g = Graph()

a38 = Namespace("https://github.com/lettis/a38/ontology#")


g.add((a38["text"], RDFS.comment, Literal("A type derived from XSD::string to define a long text.")))
g.add((a38["text"], RDF.type, XSD.string))


g.add((a38["User"], RDFS.comment, Literal("A user, who might define or execute processes.")))
g.add((a38["User"], a38["email"], XSD.string))


g.add((a38["Process"], RDFS.comment, Literal("A process description.")))
g.add((a38["Process"], a38["createdBy"], a38["User"]))
g.add((a38["Process"], a38["createdAt"], XSD.dateTime))
g.add((a38["Process"], a38["lastModifiedAt"], XSD.dateTime))
g.add((a38["Process"], a38["description"], a38["text"]))



g.add((a38["Step"], RDFS.comment, Literal("A single process step to be performed.")))
g.add((a38["Process"], a38["startsWith"], a38["Step"]))
g.add((a38["Step"], a38["next"], a38["Step"]))
g.add((a38["Step"], RDFS.label, XSD.string))
g.add((a38["Step"], a38["description"], a38["text"]))


g.add((a38["Execution"], RDFS.comment, Literal("An execution of a given process.")))
g.add((a38["Execution"], a38["definedBy"], a38["Process"]))
g.add((a38["Execution"], a38["runBy"], a38["User"]))
g.add((a38["Execution"], a38["startedAt"], XSD.dateTime))
g.add((a38["Execution"], a38["endedAt"], XSD.dateTime))
g.add((a38["Execution"], a38["currentStep"], a38["Step"]))


g.bind("a38", a38)
g.serialize("a38_ontology.ttl")


############

g = Graph()

ui = Namespace("https://github.com/lettis/a38/ui-ontology#")

g.add((ui["Screen"], RDFS.comment, Literal("A full-size screen object")))
g.add((ui["Screen"], ui["binding"], XSD.string))
g.add((ui["Screen"], ui["contains"], ui["Placement"]))

g.add((ui["Widget"], RDFS.comment, Literal("Any kind of UI widget")))

g.add((ui["Form"], RDFS.comment, Literal("An input form container")))
g.add((ui["Form"], RDF.type, ui["Widget"]))
g.add((ui["Form"], ui["forEntity"], XSD.anyURI))
g.add((ui["Form"], ui["asSingleton"], XSD.boolean))
g.add((ui["Form"], ui["exceptAttribute"], XSD.anyURI))

g.add((ui["Placement"], RDFS.comment, Literal("Placement information of a widget.")))
g.add((ui["Placement"], ui["forWidget"], ui["Widget"]))
g.add((ui["Placement"], ui["order"], XSD.integer))


g.bind("ui", ui)
g.serialize("a38_ui_ontology.ttl")


############

g = Graph()

app = Namespace("https://github.com/lettis/a38/app#")

g.add((app["UserForm"], RDF.type, ui["Form"]))
g.add((app["UserForm"], ui["forEntity"], a38["User"]))
g.add((app["UserForm"], ui["asSingleton"], Literal(True)))

g.add((app["UserScreen"], RDF.type, ui["Screen"]))
g.add((app["UserScreen"], RDFS.label, Literal("user")))
g.add((app["UserScreen"], ui["binding"], Literal("u")))

frm = BNode()
g.add((frm, RDF.type, ui["Placement"]))
g.add((frm, ui["forWidget"], app["UserForm"]))
g.add((frm, ui["position"], Literal(1)))
g.add((app["UserScreen"], ui["contains"], frm))


g.add((app["ProcessScreen"], RDF.type, ui["Screen"]))
g.add((app["ProcessScreen"], RDFS.label, Literal("processes")))
g.add((app["ProcessScreen"], ui["binding"], Literal("p")))




g.bind("app", app)
g.bind("a38", a38)
g.bind("ui", ui)
g.serialize("a38_app.ttl")


