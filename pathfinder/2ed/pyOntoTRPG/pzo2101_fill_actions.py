import pandas as pd
from owlready2 import *
import main


def fill(pzo2101):
    with pzo2101:
        class Action(Thing): pass
        class need_training(Action>>bool, FunctionalProperty):
            comment = ("Anyone can use a skill’s untrained actions, but you can use trained actions only if you have a "
                       "proficiency rank of trained or better in that skill.")
        main.fill_onto_from_xml(pzo2101, "Actions", Action)