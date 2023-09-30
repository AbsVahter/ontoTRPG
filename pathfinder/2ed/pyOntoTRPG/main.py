import xml.etree.ElementTree as ET

import pandas as pd
from owlready2 import *

import pzo2101_fill_actions
import pzo2101_fill_age_of_lost_omens
import pzo2101_fill_ancestries
import pzo2101_fill_art
import pzo2101_fill_backgrounds
import pzo2101_fill_characteristics
import pzo2101_fill_classes
import pzo2101_fill_equipment
import pzo2101_fill_feats
import pzo2101_fill_rules
import pzo2101_fill_spells
import pzo2101_fill_traits
import pzo2101_hierarchy
import visualization

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    path = r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed"
    onto_path.append(path)
    pzo2101 = get_ontology(
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")

    pzo2101_hierarchy.create(pzo2101)
    pzo2101_fill_characteristics.fill(pzo2101)
    pzo2101_fill_rules.fill(pzo2101)
    pzo2101_fill_feats.fill(pzo2101)
    pzo2101_fill_traits.fill(pzo2101)
    pzo2101_fill_actions.fill(pzo2101)
    pzo2101_fill_ancestries.fill(pzo2101)
    pzo2101_fill_backgrounds.fill(pzo2101)
    pzo2101_fill_equipment.fill(pzo2101)
    pzo2101_fill_classes.fill(pzo2101)
    pzo2101_fill_spells.fill(pzo2101)
    pzo2101_fill_age_of_lost_omens.fill(pzo2101)
    pzo2101_fill_art.fill(pzo2101)

    # visualization.show(pzo2101, path)

    pzo2101.save()


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


def set_relations(onto, subj, data_xml):
    with onto:
        annotations_lst = ['comment', 'image', 'abbreviation']
        for prop in data_xml:
            pred = onto[prop.tag]
            is_str = prop.tag in annotations_lst or (pred and any(x in pred.range for x in [str, int, bool]))
            obj_text = render_text(prop.text, prop.tag, prop.get('object_class'), is_str)
            if prop.tag in annotations_lst:
                obj = obj_text
            else:
                if is_str:
                    obj = pred.range[0](obj_text)
                else:
                    obj = onto[obj_text] or pred.range[0](obj_text)
            if pred and FunctionalProperty in pred.is_a:
                setattr(subj, pred.name, obj)
            else:
                getattr(subj, prop.tag).append(obj)
            val = prop.get('value')
            if pred and val:
                onto.relation_value[subj, pred, obj] = val


def render_text(s, prop_name=None, object_class=None, is_str=False):
    if is_str:
        return s
    else:
        scenario = object_class or prop_name
        match scenario:
            case x if "Language" in x:
                return f"{prepare_name(s)}_language"
            case "Icon":
                return f"art_{prepare_name(s)}_icon"
            case "Map":
                return f"art_{prepare_name(s)}_map"
            case "Art":
                return f"art_{prepare_name(s)}"
            case "has_trait" | "Specialization_effect" | "Trait":
                return f"{prepare_name(s)}_trait"
            case "spell":
                return f"{prepare_name(s)}_spell"
            case "Cleric_domain":
                return f"{prepare_name(s)}_domain"
            case "Archetype":
                return f"{prepare_name(s)}_archetype"
            case _:
                return prepare_name(s)


def fill_onto_from_xml(onto, file_name, subj_class):
    with onto:
        for child in iterate_xml_tree(file_name):
            #print(child.get('name'))
            subclass_name = child.get('subclass')
            cl = onto[subclass_name] if subclass_name else subj_class
            if subclass_name and not cl:
                cl = types.new_class(subclass_name, (subj_class,))
            subj = cl(render_text(child.get('name'), object_class = cl.name))
            set_relations(onto, subj, child)