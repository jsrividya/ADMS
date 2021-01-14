import json
import random
from collections import deque


def update_trend(patient_id, latest_reading):
    with open('glucose_trends.json', 'r') as f:
        glucose_readings = json.load(f)
        trend = glucose_readings['trends'][patient_id]
        trend.pop(0)
        trend.append(latest_reading)
        glucose_readings['trends'][patient_id] = trend
    with open('glucose_trends.json', 'w') as f:
        json.dump(glucose_readings, f, indent=4)
    with open('glucose_trends.json', 'r') as f:
        glucose_readings = json.load(f)
        trend = glucose_readings['trends'][patient_id]
    return trend


update_trend('1989052575035', random.randrange(50, 90, 5))
update_trend('1990081975035', random.randrange(50, 90, 5))
update_trend('1994090775035', random.randrange(50, 90, 5))

