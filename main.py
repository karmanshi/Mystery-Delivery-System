import json 
import math

# Calculate distance between two points
def calculate_distance(point1, point2):
    x1,y1 = point1 
    x2,y2 = point2 
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance 

#  Convert warehouses/agents into a common dictionary format
def normalize_entities(data):
    if isinstance(data,dict):
        return data 
    result = {}

    for item in data:
        result[item["id"]] = item ["location"]
    return result    

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

def run(data_file_path):
    with open(data_file_path,"r") as file:
        data = json.load(file)

    warehouses = normalize_entities(
        data["warehouses"]
    )

    agents = normalize_entities(data["agents"])

    packages = data["packages"]   

    assignments = {}

    # Assign every package
    for package in packages:
        package_id = package["id"]
        if "warehouse_id" in package:
            warehouse_id = package["warehouse_id"]
        else:
            warehouse_id = package["warehouse"]

        warehouse_position = warehouses[warehouse_id]

        nearest_agent = find_nearest_agent(
            warehouse_position,
            agents
        )

        assignments[package_id] = nearest_agent

    agent_packages = {}
    for agent_id in agents:
        agent_packages[agent_id] = []
    for package in packages:
        package_id = package["id"]
        agent_id = assignments[package_id]
        agent_packages[agent_id].append(package)

    # Keep track of agent positions
    agent_positions ={}
    for agent_id, position in agents.items():
        agent_positions[agent_id] = position.copy()

    # Tracking information

    total_distances = {}
    packages_delivered = {}
    for agent_id in agents:
        total_distances[agent_id] = 0.0
        packages_delivered[agent_id] = 0

    # Simulate delivery
    for agent_id,agent_package_list in agent_packages.items():
        for package in agent_package_list:
            if "warehouse_id" in package:
                warehouse_id = package["warehouse_id"]
            else:
                warehouse_id = package["warehouse"]

            warehouse_position = warehouses[warehouse_id]

            destination = package["destination"]


            # Agent travels to warehouse
            distance_to_warehouse = calculate_distance(
                agent_positions[agent_id],
                warehouse_position
            )
            total_distances[agent_id] += distance_to_warehouse

            agent_positions[agent_id] = warehouse_position.copy()


            # Warehouse → Destination
            distance_to_destination = calculate_distance(
                agent_positions[agent_id],
                destination
            )
            total_distances[agent_id] += distance_to_destination

            agent_positions[agent_id] = destination.copy()
            packages_delivered[agent_id] += 1

    # Create the report
    report ={}
    for agent_id in agents:
        distance = total_distances[agent_id]
        count = packages_delivered[agent_id]
        if count > 0:
            efficiency = distance / count
        else:
            efficiency = 0

        report[agent_id] = {
            "packages_delivered": count,
            "total_distance": round(distance, 2),
            "efficiency": round(efficiency, 2)
        }

    # Find best agent
    active_agents = [
        agent_id
        for agent_id in agents
        if packages_delivered[agent_id] > 0
    ]


    if active_agents:

        best_agent = min(
            active_agents,
            key=lambda agent_id:
                report[agent_id]["efficiency"]
        )

        report["best_agent"] = best_agent

    else:
        report["best_agent"] = None

    # Save report.json
    file_name=data_file_path.replace(".json", "").split("/")[-1]
    output_file_path=f"reports/report_{file_name}.json"
    with open(output_file_path, "w") as file:
        json.dump(report, file, indent=4)

    print("Report is Generated successfully and stored at: ", output_file_path)


if __name__=="__main__":
    file_path=input("Enter file path: ")
    run(file_path)