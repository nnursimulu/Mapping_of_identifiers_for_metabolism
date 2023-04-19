# Author: Nirvana Nursimulu

# Currently, script finds reaction equivalencies only between BiGG and KEGG.

from argparse import ArgumentParser
import utils

def get_id1_to_id2(db_to_id1_to_id2, db_names):

    id1_to_id2 = {}
    for db_name in db_names:
        curr_id1_to_id2 = db_to_id1_to_id2[db_name]
        for id1, id2 in curr_id1_to_id2.items():
            id1_to_id2[id1] = id2
    return id1_to_id2


def translate_from_db1_to_db2(rxn_equation_db_1, id1_to_id2, db2_met_names):
    """Translate reaction equation from nomenclature of db1 to db2."""

    rxn_equation_db_2 = {1: [], 2: []}
    for eqn_side in [1, 2]:
        for elem in rxn_equation_db_1[eqn_side]:
            translated_elems_tmp = list(id1_to_id2[elem])
            translated_elems = []
            for elem in translated_elems_tmp:
                for db2_met_name in db2_met_names:
                    if not elem.startswith(db2_met_name):
                        continue
                    translated_elems.append(elem.split(":")[1])
            rxn_equation_db_2[eqn_side].append(translated_elems)
    return rxn_equation_db_2


def compare_rxn_formula_component(components_1, components_2):
    """Return whether component_1 = component_2 (EQUAL), component_2 is a subset of component_1 (2_SUBSET_1), or
    return CONFLICT if components_2 is not a subset of components_1.
    Note that both components_1 and components_2 are assumed to consist of a list of lists."""

    num_same_in_list_2 = 0
    for elem2_list in components_2:
        found_same = False
        for elem_2 in elem2_list:
            # compare elems in list 2's sublist to each sublist in list 1.
            # if found equivalent, then say we found it.
            if found_same:
                break
            for elem_1 in components_1:
                if elem_2 in elem_1:
                    num_same_in_list_2 += 1
                    found_same = True
                    break
        # if couldn't find equivalent for this compound, then, conflict.
        if not found_same:
            return "CONFLICT"
    # If found fewer equivalent, then, list2 is a subset of list1.
    if num_same_in_list_2 < len(components_1):
        return "2_SUBSET_1"
    # Otherwise, exactly the same.
    return "EQUAL"
            

def is_empty_formula(rxn_eqn):

    return len(rxn_eqn[1]) == 0 and len(rxn_eqn[2]) == 0


def compare_rxn_formulae(formula_1_translated_db2, formula_2):
    """Compare reactant (1) and product sides (2) of formula_1 and formula_2"""

    # For compatibility with comparison code downstream, reformat eqn of form {1: [A, B], 2: [C, D]}
    # where A + B -> C + D to {1: [[A], [B]], 2: [[C], [D]]}
    formula_2_with_sublist = {1: [], 2: []}
    for elem in formula_2[1]:
        formula_2_with_sublist[1].append([elem])
    for elem in formula_2[2]:
        formula_2_with_sublist[2].append([elem])
    valid_eqs = ["EQUAL", "2_SUBSET_1"]

    # Compare where formula_2's elements could be subsets of formula_1.
    compare_1 = compare_rxn_formula_component(formula_1_translated_db2[1], formula_2_with_sublist[1])
    compare_2 = compare_rxn_formula_component(formula_1_translated_db2[2], formula_2_with_sublist[2])
    compare_3 = compare_rxn_formula_component(formula_1_translated_db2[1], formula_2_with_sublist[2])
    compare_4 = compare_rxn_formula_component(formula_1_translated_db2[2], formula_2_with_sublist[1])

    # Compare where formula_1's elements could be subsets of formula_2.
    compare_5 = compare_rxn_formula_component(formula_2_with_sublist[1], formula_1_translated_db2[1])
    compare_6 = compare_rxn_formula_component(formula_2_with_sublist[2], formula_1_translated_db2[2])
    compare_7 = compare_rxn_formula_component(formula_2_with_sublist[1], formula_1_translated_db2[2])
    compare_8 = compare_rxn_formula_component(formula_2_with_sublist[2], formula_1_translated_db2[1])

    if is_empty_formula(formula_1_translated_db2):
        return "Conflict"
    if (compare_1 == "EQUAL" and compare_2 == "EQUAL"):
        return "Same; same direction"
    if (compare_3 == "EQUAL" and compare_4 == "EQUAL"):
        return "Same; opposite direction"
    if (compare_1 in valid_eqs and compare_2 in valid_eqs) or (compare_5 in valid_eqs and compare_6 in valid_eqs):
        return "Possibly same; same direction"
    if (compare_3 in valid_eqs and compare_4 in valid_eqs) or (compare_7 in valid_eqs and compare_8 in valid_eqs):
        return "Possible same; opposite direction"
    return "Conflict"

def match_up_rxn_formulae(db1_rxn_to_formula, db2_rxn_to_formula, db1_rxn_db_name, db2_rxn_db_name, \
    db2_met_names, db_type_rxn_to_met, rxn_db_to_id1_to_id2, met_db_to_id1_to_id2):
    """
    Matches up the reaction formulae from db1 to db2 with additional information about what the match looks like.

    db1_rxn_to_formula: rxn to formula dictionary for db1
    db2_rxn_to_formula: rxn to formula dictionary for db2
    db1_rxn_db_name: name of db1 for reactions
    db2_rxn_db_name: name of db2 for reactions
    db2_met_names: name of db2 for compounds (multiple as for KEGG can have multiple)
    db_type_rxn_to_met: says what the metabolite identifier name from one type of reaction database is.
    rxn_db_to_id1_to_id2: reaction database to identifier from this database to another.
    met_db_to_id1_to_id2: metabolite database to identifier from this database to another.
    """

    rxn_db1_to_db2_match = {}

    # Get the mapping from one database to another for reactions.
    rxn_db_id1_to_id2 = rxn_db_to_id1_to_id2[db1_rxn_db_name]

    # Start with getting the metabolite IDs associated with the reaction ID for db1.
    # Then, get the mapping from one database to another for metabolites.
    db1_met_db_names = db_type_rxn_to_met[db1_rxn_db_name]
    met_db_id1_to_id2 = get_id1_to_id2(met_db_to_id1_to_id2, db1_met_db_names)

    # Now, for each reaction identifier from one database to the other, compare the formulae.
    for rxn_1, rxn_2_set in rxn_db_id1_to_id2.items():
        rxn_1 = rxn_1.split("#")[0] # This is for those special reactions with the "#" only relevant for metanetx.
        formula_1 = db1_rxn_to_formula[rxn_1]
        for rxn_2 in rxn_2_set:
            if not rxn_2.startswith(db2_rxn_db_name):
                continue
            rxn_2 = rxn_2.split(":")[1]
            rxn_2 = rxn_2.split("#")[0] # This is for those special reactions with the "#" only relevant for metanetx.
            if rxn_2 not in db2_rxn_to_formula:
                rxn_db1_to_db2_match[rxn_1 + "!" + rxn_2] = "Could not compare"
                continue
            formula_2 = db2_rxn_to_formula[rxn_2]

            # Translate the equation for reaction 1 into db2, then compare overlap
            formula_1_translated_db2 = translate_from_db1_to_db2(formula_1, met_db_id1_to_id2, db2_met_names)
            overlap_conclusion = compare_rxn_formulae(formula_1_translated_db2, formula_2) #TODO
            rxn_db1_to_db2_match[rxn_1 + "!" + rxn_2] = overlap_conclusion
    return rxn_db1_to_db2_match


def add_to_dict(key_value, key, value):

    if key not in key_value:
        key_value[key] = set()
    key_value[key].add(value)


def write_out_equiv_conclusions(output_kegg_bigg_equiv, db1_to_db2_equiv):

    # Invert dictionary to make it easy to deal with this.
    results_to_db1_to_db2 = {}
    for db1_to_db2_item, result in db1_to_db2_equiv.items():
        add_to_dict(results_to_db1_to_db2, result, db1_to_db2_item)

    with open(output_kegg_bigg_equiv, "w") as writer:
        # First write stats.
        writer.write("# Statistics of the equivalencies found:\n")
        for result in sorted(results_to_db1_to_db2):
            num_items = len(results_to_db1_to_db2[result])
            writer.write("# " + result + "\t" + str(num_items) + "\n")
        writer.write("\n# Now for the equivalencies found\n")

        # Now write the equivalencies found.
        for result in sorted(results_to_db1_to_db2):
            db1_to_db2_items = results_to_db1_to_db2[result]
            for curr_item in sorted(db1_to_db2_items):
                split = curr_item.split("!")
                db1_item, db2_item = split[0], split[1]
                writer.write("\t".join([db1_item, db2_item, result]) + "\n")


if __name__ == '__main__':

    parser = ArgumentParser(description="Determines reaction reversibility equivalencies.")
    parser.add_argument("--parsed-info", type=str, help="Folder that contains the parsed info from MetaNetX.")
    parser.add_argument("--parsed-split-rxn-info", type=str, \
        help="Folder that contains the parsed and formattedinformation specific to reactions.")

    args = parser.parse_args()
    parsed_info_folder = args.parsed_info
    parsed_split_rxn_info = args.parsed_split_rxn_info

    rxn_mapping_file = parsed_info_folder + "/PARSED_reaction_mapping.out"
    met_mapping_file = parsed_info_folder + "/PARSED_metabolite_mapping.out"
    output_kegg_bigg_equiv = parsed_split_rxn_info + "/COMPUTED_kegg_bigg_equiv.out"

    #TODO: expand to SEED reaction definitions
    bigg_rxn_def_file = parsed_info_folder + "/PARSED_BiGG_rxn_formula.out"
    kegg_rxn_def_file = parsed_info_folder + "/PARSED_KEGG_rxn_formula.out"

    # 0a. Parse mapping of reaction and metabolite from one database to another.
    rxn_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(rxn_mapping_file)
    met_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(met_mapping_file)

    # 0b. Get mapping of what kind of database reaction identifiers map to metabolite identifiers.
    db_type_rxn_to_met = utils.read_default_db_type_rxn_to_met()
    
    # 1. Load reaction definitions.
    bigg_rxn_to_formula = utils.read_rxn_formula(bigg_rxn_def_file, "BiGG")
    kegg_rxn_to_formula = utils.read_rxn_formula(kegg_rxn_def_file, "KEGG")

    # 2. Find reaction equivalencies.
    # biggR is the database name for BiGG.
    # kegg.reaction is how KEGG reactions are identified in PARSED_reaction_mapping.out
    # kegg.compound is how KEGG compounds are identified in PARSED_metabolite_mapping.out
    kegg_to_bigg_equiv = match_up_rxn_formulae(bigg_rxn_to_formula, kegg_rxn_to_formula,\
        "biggR", "kegg.reaction", ["kegg.compound", "kegg.glycan"], \
            db_type_rxn_to_met, rxn_db_to_id1_to_id2, met_db_to_id1_to_id2)

    # 3. Write out results of comparing reactions.
    write_out_equiv_conclusions(output_kegg_bigg_equiv, kegg_to_bigg_equiv)