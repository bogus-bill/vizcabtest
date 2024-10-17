from .data_loader import load_data


# Load relevant data files
batiments = load_data('batiments.json')
zones = load_data('zones.json')
usages = load_data('usages.json')
construction_elements = load_data('construction_elements.json')


def compute_building_surface(building_id):
    """
    Compute the total surface of a building based on its zones.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    total_surface = 0
    for zone_id in building['zoneIds']:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        total_surface += zone['surface']

    return total_surface


def compute_building_usage(building_id):
    """
    Compute the primary usage of a building based on its zones.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    zone_data_map = {}
    for zone_id in building["zoneIds"]:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        usage_id = zone["usage"]
        zone_data_map[usage_id] = max(zone_data_map.get(usage_id, 0), zone["surface"])

    max_usage_id = max(zone_data_map, key=zone_data_map.get)  # just get the id from the map
    max_usage_label = usages[str(max_usage_id)]

    return max_usage_label


def compute_building_carbon_footprint(building_id):
    """
    Compute the total carbon footprint of a building.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    total_impact = 0
    for zone_id in building['zoneIds']:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        if zone:
            for element in zone['constructionElements']:
                quantity = element['quantite']
                construction_element = next((e for e in construction_elements if e['id'] == element['id']), None)

                impacts = construction_element['impactUnitaireRechauffementClimatique']
                production_impact = impacts['production'] * quantity
                construction_impact = impacts['construction'] * quantity

                rp_factor = max(1, building["periodeDeReference"] / construction_element["dureeVieTypique"])

                # exploitation_impact = impacts['exploitation'] * quantity
                exploitation_impact = (
                    (rp_factor * impacts["exploitation"] + (rp_factor - 1))
                     * (impacts["production"] + impacts['construction'] + impacts['finDeVie'])
                     * quantity
                )

                end_of_life_impact = impacts['finDeVie'] * quantity

                total_impact += production_impact + construction_impact + exploitation_impact + end_of_life_impact

    return total_impact
