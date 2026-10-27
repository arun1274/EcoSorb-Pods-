"""Offline *rectangular* spill mission planner using local-meter coordinates."""
from math import ceil


def rectangle_bounds(polygon):
    if len(polygon) != 4 or any(len(p) != 2 for p in polygon):
        raise ValueError('Demo requires a four-corner rectangle')
    xs = [float(p[0]) for p in polygon]
    ys = [float(p[1]) for p in polygon]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    if xmax <= xmin or ymax <= ymin or len(set(map(tuple, polygon))) != 4:
        raise ValueError('Polygon must have four unique, nondegenerate points')
    required = {(xmin,ymin),(xmin,ymax),(xmax,ymin),(xmax,ymax)}
    if set(zip(xs,ys)) != required:
        raise ValueError('This demonstrator supports axis-aligned rectangles only')
    return xmin, ymin, xmax, ymax


def lawnmower(xmin, ymin, xmax, ymax, swath):
    if swath <= 0:
        raise ValueError('swath_width_m must be positive')
    rows = max(1, ceil((ymax-ymin)/swath))
    route = []
    for i in range(rows):
        y = min(ymax, ymin + (i + 0.5) * (ymax-ymin) / rows)
        ends = ((xmin,y),(xmax,y)) if i%2 == 0 else ((xmax,y),(xmin,y))
        route.extend([list(pt) for pt in ends])
    return route


def plan(data):
    if data.get('coordinate_system') != 'local_meters':
        raise ValueError('Only local_meters coordinates supported; GPS is not supported')
    xmin,ymin,xmax,ymax = rectangle_bounds(data['polygon'])
    area = (xmax-xmin)*(ymax-ymin)
    thickness = float(data['oil_thickness_m'])
    density = float(data['oil_density_kg_m3'])
    capacity = float(data['cartridge_capacity_kg'])
    pods = int(data['available_pods'])
    swath = float(data['swath_width_m'])
    if any(v <= 0 for v in (thickness,density,capacity,swath)) or pods < 1 or pods > 1000:
        raise ValueError('Physical parameters and available_pods must be positive')
    mass = area*thickness*density
    loads = ceil(mass/capacity)
    zones = []
    for i in range(pods):
        x0 = xmin+(xmax-xmin)*i/pods
        x1 = xmin+(xmax-xmin)*(i+1)/pods
        zones.append({'zone_id':f'ZONE-{i+1:02}', 'pod_id':f'POD-{i+1:02}',
                      'bounds_m':[round(x0,3),ymin,round(x1,3),ymax],
                      'waypoints_local_m':lawnmower(x0,ymin,x1,ymax,swath)})
    return {'spill_id':data.get('spill_id','DEMO'), 'area_m2':round(area,3),
            'estimated_mass_kg':round(mass,3), 'estimated_cartridge_loads':loads,
            'available_pods':pods, 'assumptions':'fictional input; rectangular local-meter demo; no actual GEE/GPS or measured absorption',
            'zones':zones}
