from .data_loader import load_data


# Load relevant data files
batiments = load_data('batiments.json')
zones = load_data('zones.json')
usages = load_data('usages.json')
construction_elements = load_data('construction_elements.json')


def get_building_surface(building_id):
    """
    Calculate the total surface of a building based on its zones.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    total_surface = 0
    for zone_id in building['zoneIds']:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        if zone:
            total_surface += zone['surface']

    return total_surface


def get_building_usage(building_id):
    """
    Determine the primary usage of a building based on its zones.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    usage_surface_map = {}

    for zone_id in building['zoneIds']:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        if zone:
            usage_id = zone['usage']
            usage_surface_map[usage_id] = usage_surface_map.get(usage_id, 0) + zone['surface']

    # Find the usage with the largest surface
    primary_usage_id = max(usage_surface_map, key=usage_surface_map.get)
    primary_usage = next((u for u in usages if u['id'] == primary_usage_id), {}).get('label')

    return primary_usage


def get_building_carbon_footprint(building_id):
    """
    Calculate the total carbon footprint of a building.
    """
    building = next((b for b in batiments if b['id'] == building_id), None)
    if not building:
        return None

    total_impact = 0
    for zone_id in building['zoneIds']:
        zone = next((z for z in zones if z['id'] == zone_id), None)
        if zone:
            for element in zone['constructionElements']:
                element_id = element['id']
                quantity = element['quantite']
                construction_element = next((e for e in construction_elements if e['id'] == element_id), None)

                if construction_element:
                    impacts = construction_element['impactUnitaireRechauffementClimatique']
                    production_impact = impacts['production'] * quantity
                    construction_impact = impacts['construction'] * quantity
                    exploitation_impact = impacts['exploitation'] * quantity
                    end_of_life_impact = impacts['finDeVie'] * quantity

                    total_impact += production_impact + construction_impact + exploitation_impact + end_of_life_impact

    return total_impact
