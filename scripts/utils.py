# Author: Nirvana Nursimulu

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