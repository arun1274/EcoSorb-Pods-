"""Command-line interface: python -m ecosorb.cli --input ... --output ..."""
import argparse
import json
from pathlib import Path
from .planner import plan
from .simulator import simulate_pod


def main():
    parser=argparse.ArgumentParser(description='EcoSorb offline planning demonstration')
    parser.add_argument('--input',default='data/sample_spill.json')
    parser.add_argument('--output',default='output/mission.json')
    args=parser.parse_args()
    data=json.loads(Path(args.input).read_text(encoding='utf-8'))
    result=plan(data)
    for zone in result['zones']:
        zone['simulated_pod_run']=simulate_pod(zone['waypoints_local_m'], capacity_kg=data['cartridge_capacity_kg'])
    target=Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f"Saved {len(result['zones'])} demo zones to {target}")


if __name__=='__main__':
    main()
