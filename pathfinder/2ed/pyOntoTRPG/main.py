import xml.etree.ElementTree as ET

import pandas as pd
from owlready2 import *

import pzo2101_fill
import visualization

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    path = r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed"
    onto_path.append(path)
    pzo2101 = pzo2101_fill.fill()
    pzo2101.save()

    #visualization.show()


def prepare_name(s):
    return re.sub('\W+', '_', s.lower().strip())


def iri_for_search(s):
    return f"*{prepare_name(s)}"


def read_text_for_parse(file_name):
    return pd.read_csv(get_resource_path(file_name + '.txt'), sep = '\t').iterrows()


def iterate_xml_tree(file_name):
    tree = ET.parse(f'resources/{file_name}.xml')
    return tree.getroot()


def get_resource_path(file_name):
    return f'resources/{file_name}'


def set_relation_annotation(ontology, relation, child_xml, property_name):
    property_value = child_xml.get(property_name)
    relation_annotation = ontology[property_value] or ontology[get_id(property_value)] or property_value
    relation.append(relation_annotation)


def set_relation_annotations(ontology, child_xml, subject, predicate, obj):
    if predicate:
        for property_name in child_xml.attrib:
            if property_name != "object_class":
                relation = getattr(ontology, f"relation{property_name.capitalize()}")[subject, predicate, obj]
                set_relation_annotation(ontology, relation, child_xml, property_name)


def create_new_entity(ontology, predicate, obj_text, object_class):
    if object_class:
        cl = ontology[object_class]
    elif len(predicate.range) > 0:
        cl = predicate.range[0]
    else:
        cl = list(filter(lambda x: len(x.range) > 0, predicate.ancestors()))[0].range[0]
    return cl(obj_text)


def set_relations(ontology, subject, data_xml):
    with ontology:
        annotations_lst = ['comment', 'image', 'abbreviation']
        for child_xml in data_xml:
            predicate = ontology[child_xml.tag]
            is_str = child_xml.tag in annotations_lst or (
                    predicate and any(x in predicate.range for x in [str, int, bool]))
            object_class = child_xml.get('object_class')
            obj_text = get_id(child_xml.text, child_xml.tag, object_class, is_str)
            if child_xml.tag in annotations_lst:
                obj = obj_text
            else:
                if is_str:
                    obj = predicate.range[0](obj_text)
                else:
                    obj = ontology[obj_text] or create_new_entity(ontology, predicate, obj_text, object_class)
            if predicate and FunctionalProperty in predicate.is_a:
                setattr(subject, predicate.name, obj)
            else:
                getattr(subject, child_xml.tag).append(obj)
            set_relation_annotations(ontology, child_xml, subject, predicate, obj)


def get_id(s, prop_name=None, object_class=None, is_str=False):
    if is_str:
        return s
    else:
        scenario = object_class or prop_name
        match scenario:
            case str(x) if "Language" in x:
                return f"{prepare_name(s)}_language"
            case "Icon":
                return f"art_{prepare_name(s)}_icon"
            case "Map":
                return f"art_{prepare_name(s)}_map"
            case "Art":
                return f"art_{prepare_name(s)}"
            case "trait" | "SpecializationEffect" | "Trait":
                return f"{prepare_name(s)}_trait"
            case str(x) if "DamageType" in x:
                return f"{prepare_name(s)}_trait"
            case "spell" | "Spell":
                return f"{prepare_name(s)}_spell"
            case "ClericDomain":
                return f"{prepare_name(s)}_domain"
            case "Archetype":
                return f"{prepare_name(s)}_archetype"
            case "SpellByMagicalTradition" | "Tradition":
                return f"{prepare_name(s).capitalize()}Tradition"
            case "SpellBySchool" | "School":
                return f"{prepare_name(s).capitalize()}School"
            case "Statement":
                return f'{prepare_name(s)}_statement'
            case _:
                return prepare_name(s)


def render_label(s):
    if s.isupper():
        return s.capitalize()
    else:
        return s


def fill_onto_from_xml(onto, file_name, subj_class):
    with onto:
        for child in iterate_xml_tree(file_name):
            #print(child.get('name'))
            subclass_name = child.get('subclass')
            cl = onto[subclass_name] if subclass_name else subj_class
            if subclass_name and not cl:
                cl = types.new_class(subclass_name, (subj_class,))
            subj = cl(get_id(child.get('name'), object_class = cl.name),
                      label = render_label(child.get('name')))
            set_relations(onto, subj, child)


def add_class_restriction(onto, subject_name, predicate_name, object_names_for_render, is_inverse=False, object_class = None):
    subject = onto[subject_name]
    for object_name_for_render in object_names_for_render:
        predicate = onto[predicate_name] if not is_inverse else Inverse(onto[predicate_name])
        object = onto[get_id(object_name_for_render, predicate_name, object_class)]
        subject.is_a.append(predicate.value(object))
