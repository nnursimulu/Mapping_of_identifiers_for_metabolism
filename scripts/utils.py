# Author: Nirvana Nursimulu

DELIMITER_LIST = ["<=>", "<->", "=>", "<=", "->", "<-", "="]

def is_number(string):

    try:
        float(string)
        return True
    except:
        return False


def get_cpds_only(eqn_string, type_of_db=None):
    """If type of db is BiGG, then, remove compartment information."""

    cpd_elems = set()
    temp_cpd_elems = eqn_string.split()
    for elem in temp_cpd_elems:
        if elem == "+":
            continue
        if is_number(elem):
            continue
        if type_of_db == "BiGG":
            elem = elem.split("_")[:-1]
            elem = "_".join(elem)
        if type_of_db == "SEED":
            elem = elem.split("[")[0]
        cpd_elems.add(elem)
    return cpd_elems


def encode_rxn_eqn(equation, type_of_db):
    """Return string of the form w A + x B -> y C + z D to be a dict with
    {1: ['A', 'B'], 2: ['C', 'D']}."""

    delimiter = None
    for curr_choice in DELIMITER_LIST:
        if curr_choice in equation:
            delimiter = curr_choice
            break
    if delimiter is None:
        raise Exception("Delimiter of interest is not found in list.")
    split = equation.split(delimiter)
    side_1, side_2 = split[0], split[1]
    cpds_side_1 = get_cpds_only(side_1, type_of_db)
    cpds_side_2 = get_cpds_only(side_2, type_of_db)
    eqn_dict = {1: cpds_side_1, 2: cpds_side_2}
    return eqn_dict


def read_rxn_formula(filename, type_of_db):
    """Read reaction ID to formula, encoded to be easily compared with others"""

    rxn_to_formula = {}
    with open(filename) as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            if line.startswith("#"):
                continue
            info = line.split("\t")
            rxn, formula = info[0], info[1]
            rxn_to_formula[rxn] = encode_rxn_eqn(formula, type_of_db)
    return rxn_to_formula


def read_db_to_other_identifiers(filename):
    """Read mapping of identifier from one database to another."""

    db_to_id1_to_id2 = {}
    with open(filename) as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            db = line.split(":")[0]
            id1 = line.split()[0].split(":")[1]
            id2 = line.split()[1]
            if db not in db_to_id1_to_id2:
                db_to_id1_to_id2[db] = {}
            if id1 not in db_to_id1_to_id2[db]:
                db_to_id1_to_id2[db][id1] = set()
            db_to_id1_to_id2[db][id1].add(id2)
    return db_to_id1_to_id2


def read_default_db_type_rxn_to_met():
    """Return default mapping from reaction database to metabolite database."""

    return {'biggR': ['biggM'], 'seedR': ['seedM'], 'keggR': ['keggC', 'keggG']}