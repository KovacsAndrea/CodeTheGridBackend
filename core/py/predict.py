import json
import random
import pandas as pd

qualifying = pd.read_csv('core/py/data/qualifying2025.csv')
race_results = pd.read_csv('core/py/data/raceResults2025.csv')

driver_mapping = {
    'albon': 23,  
    'sainz': 55,  
}

def get_driver_qualifying(driver_name):
    driver_id = driver_mapping.get(driver_name)
    df = qualifying[qualifying['No'] == driver_id].sort_values('Race', ascending=False)
    if df.empty:
        return random.randint(10, 20)  
    
    avg_q = df.head(5)['Q1'].apply(lambda x: float(x.split(":")[0]) + float(x.split(":")[1])/60).mean()
    return avg_q

def get_race_position(qualifying_time, historical_performance, car_strength):
    min_time = 1.30
    max_time = 1.60  
    norm = (qualifying_time - min_time) / (max_time - min_time)
    predicted_position = int(1 + norm * 19)  
    consistency_factor = historical_performance  

    adjusted_position = predicted_position * consistency_factor * float(car_strength)
    return int(adjusted_position)

driver_performance = {
    'albon': {'historical_performance': 0.7, 'car_strength': 1.5},  
    'sainz': {'historical_performance': 0.9, 'car_strength': 1.5}
}

alex_q_time = get_driver_qualifying('albon')
carlos_q_time = get_driver_qualifying('sainz')


alex_race_pos = get_race_position(alex_q_time, driver_performance['albon']['historical_performance'], driver_performance['albon']['car_strength'])
carlos_race_pos = get_race_position(carlos_q_time, driver_performance['sainz']['historical_performance'], driver_performance['sainz']['car_strength'])


def get_constructor_points(driver_positions):
    points_map = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    points = 0
    for pos in driver_positions:
        if pos <= 10:  
            points += points_map.get(pos, 0)
    return points

constructor_points = get_constructor_points([alex_race_pos, carlos_race_pos])

result = {
    "AlexAlbon": str(alex_race_pos),
    "CarlosSainz": str(carlos_race_pos),
    "ConstructorPoints": str(constructor_points)
}

print(json.dumps(result))