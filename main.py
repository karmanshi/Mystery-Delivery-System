import json 
import math

with open("base_case.json","r") as file:
    data = json.load(file)

warehouses_data = data["warehouses"]
warehouses={}
for x in warehouses_data:
  warehouses[x['id']]=x['location']

agents_data = data["agents"]
agents={}
for x in agents_data:
  warehouses[x['id']]=x['location']

packages = data["packages"]   


def calculate_distance(point1, point2):
    x1,y1 = point1 
    x2,y2 = point2 
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance 


# Find nearest agent
def find_nearest_agent(warehouse_poisition, agents):
    nearest_agent = None 
    minimum_distance = float("inf")

    for agent_id, agent_position in agents.items():
        distance = calculate_distance(
            agent_position,
            warehouse_poisition
        )
        if distance <minimum_distance:
            minimum_distance = distance
            nearest_agent = agent_id
    return nearest_agent        
