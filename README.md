# Mystery Delivery System

A Python application that assigns delivery packages to the nearest agent based on geographic distance and generates a summary report for each agent.

## What the application does

The script reads a JSON input file containing warehouses, agents, and package delivery data. For each package, it:

- identifies the package's warehouse
- finds the agent closest to that warehouse using Euclidean distance
- assigns the package to that agent
- simulates the trip from the agent's current position to the warehouse and then to the package destination
- tracks each agent's total distance traveled, number of deliveries, and efficiency
- writes a performance report to the reports folder

## Input format

The application expects a JSON file with this structure:

```json
{
  "warehouses": {
    "W1": [0, 0],
    "W2": [50, 75]
  },
  "agents": {
    "A1": [5, 5],
    "A2": [60, 60]
  },
  "packages": [
    {"id": "P1", "warehouse": "W1", "destination": [30, 40]},
    {"id": "P2", "warehouse_id": "W2", "destination": [70, 90]}
  ]
}
```

### Notes

- `warehouses` is a dictionary of warehouse ID to `[x, y]` coordinates.
- `agents` is a dictionary of agent ID to `[x, y]` coordinates.
- `packages` is a list of delivery tasks.
- Each package can use either `warehouse` or `warehouse_id` as the warehouse reference.
- The destination field is expected to be a coordinate pair `[x, y]`.

## How the assignment logic works

For every package:

1. lookup the warehouse coordinates
2. calculate Euclidean distance from each agent to that warehouse
3. choose the nearest agent
4. keep the package assigned to that agent

After assignment, the app simulates travel for each agent:

- from the agent's current position to the warehouse
- from the warehouse to the package destination
- adds both distances to the agent's total
- increases the delivered package count

## Running the application

From the project root, run:

```bash
python main.py
```

When prompted, enter the path to the JSON input file, for example:

```text
Enter file path: test-cases/base.json
```

The script reads the file, processes the packages, and writes the output report to:

```text
reports/report_<input_name>.json
```

For example, `test-cases/base.json` creates:

```text
reports/report_base.json
```

## Output report format

The generated report contains one entry per agent plus the best-performing agent:

```json
{
  "A1": {
    "packages_delivered": 2,
    "total_distance": 121.21,
    "efficiency": 60.61
  },
  "A2": {
    "packages_delivered": 2,
    "total_distance": 79.21,
    "efficiency": 39.6
  },
  "best_agent": "A2"
}
```

### Report fields

- `packages_delivered`: total number of packages completed by the agent
- `total_distance`: cumulative Euclidean travel distance for that agent
- `efficiency`: total_distance / packages_delivered
- `best_agent`: the active agent with the lowest efficiency value

> If no agent delivers a package, `best_agent` is set to `null`.

## Files in the project

- `main.py` — application logic
- `test-cases/` — example input JSON files
- `reports/` — generated report files

## Example workflow

```bash
python main.py
# Enter file path: test-cases/base.json
```

This generates a detailed report in the `reports` directory based on the nearest-agent delivery assignment strategy.
