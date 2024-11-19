
import os
from pathlib import Path
from uuid import uuid4
from dataclasses import dataclass

import rdflib
from rdflib.namespace import RDF, RDFS, XSD


HOME = Path.home()

CONFIG_DIR = HOME / ".config" / "a38"

STORE_CONF = CONFIG_DIR / "store.ttl"


BASE_URI = "https://github.com/lettis/a38"
URI_ONTOLOGY = BASE_URI + "/ontology#"
URI_UI_ONTOLOGY = BASE_URI + "/ui-ontology#"
URI_APP = BASE_URI + "/app#"
URI_STORE = BASE_URI + "/store#"


class UI:

    @dataclass
    class Placement:
        widget: str
        position: int | None



    def __init__(self):
        self.ui = rdflib.Namespace(URI_UI_ONTOLOGY)
        self.app = rdflib.Namespace(URI_APP)

        self.g = rdflib.Graph()
        self.g.parse("a38_ui_ontology.ttl")
        self.g.parse("a38_app.ttl")

    def screens(self):
        return [
            s
            for s in self.g.subjects(
                predicate=RDF.type,
                object=self.ui["Screen"])]

    def label(self, ref):
        return str(
            self.g.value(
                subject=ref,
                predicate=RDFS.label))

    def binding(self, ref):
        return str(
            self.g.value(
                subject=ref,
                predicate=self.ui["binding"]))

    def placements(self, containerRef):
        refs = [ref for ref in self.g.objects(
            subject=containerRef,
            predicate=self.ui["contains"])]

        plcts = []
        for i, ref in enumerate(refs):
            plct = UI.Placement(
                widget = self.g.value(subject=ref, predicate=self.ui["forWidget"]),
                position = self.g.value(subject=ref, predicate=self.ui["position"])
            )
            plcts.append(plct)

        return plcts





class Ontology:

    def __init__(self):
        self.a38 = rdflib.Namespace(URI_ONTOLOGY)
        self.g = rdflib.Graph()
        self.g.parse("a38_ontology.ttl")

        self.SUPPORTED_DTYPES = [
            self.a38["text"],
            XSD.string,
        ]

    def attributes(self, subject):
        """Get all attributes of 'subject', i.e.
           all predicates (including their datatype) associated with the given subject,
           which have a supported datatype as object"""

        triples = self.g.triples((
            self.a38[subject],
            None,
            None))

        return [(triple[1], triple[2]) for triple in triples if triple[2] in self.SUPPORTED_DTYPES]




class Store:

    def __init__(self):
        self.a38 = rdflib.Namespace(URI_ONTOLOGY)
        self.store = rdflib.Namespace(URI_STORE)


        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)

        self.g = rdflib.Graph()
        if os.path.isfile(STORE_CONF):
            self.g.parse(STORE_CONF)

    def singleton(self, typename):
        """
        Create or retrieve singleton instance of the given type.

        returns: a reference to the singleton
        """

        if (None, RDF.type, self.a38[typename]) in self.g:
            ref = self.g.value(
                predicate=RDF.type,
                object=self.a38[typename])
        else:
            ref = self.store[str(uuid4())]
            self.g.add((ref, RDF.type, self.a38[typename]))

        return ref


    def attribute(self, ref_entity, ref_attr, new_value: str = None):
        if new_value:
            self.g.add((ref_entity, ref_attr, rdflib.Literal(new_value)))
            return new_value
        else:
            val = self.g.value(
                subject=ref_entity,
                predicate=ref_attr)
            if val:
                return val
            return None


    def sync(self):
        self.g.bind("store", self.store)
        self.g.bind("a38", self.a38)
        self.g.serialize(STORE_CONF, format="ttl")



if __name__ == "__main__":
    onto = Ontology()
    store = Store()

    #user = store.singleton("User")
    #user_attrs = onto.attributes("User")

    #for attr in user_attrs:
    #    print(store.attribute(user, attr[0]))


    ui = UI()
    print(ui.screens())

    scr1 = ui.screens()[0]
    scr2 = ui.screens()[1]
    print(ui.placements(scr1))
    print(ui.placements(scr2))


