"""Deterministic mock of pod state transitions. No hardware integration."""

def simulate_pod(waypoints, initial_battery_pct=100, capacity_kg=8, collected_per_waypoint_kg=0.5,
                 battery_use_per_waypoint_pct=5, return_battery_pct=30):
    if not 0 <= return_battery_pct < initial_battery_pct <= 100 or capacity_kg <= 0:
        raise ValueError('Invalid battery or cartridge configuration')
    battery = float(initial_battery_pct)
    collected = 0.0
    events = []
    status = 'MISSION_COMPLETE'
    for idx, waypoint in enumerate(waypoints):
        if battery - battery_use_per_waypoint_pct < return_battery_pct:
            status = 'RETURN_LOW_BATTERY'
            break
        if collected + collected_per_waypoint_kg > capacity_kg:
            status = 'RETURN_CARTRIDGE_FULL'
            break
        battery -= battery_use_per_waypoint_pct
        collected += collected_per_waypoint_kg
        events.append({'waypoint_index':idx, 'position_local_m':waypoint,
                       'battery_pct':round(battery,1),'estimated_collected_kg':round(collected,2)})
    return {'status':status,'telemetry':events,'final_battery_pct':round(battery,1),
            'estimated_collected_kg':round(collected,2)}
