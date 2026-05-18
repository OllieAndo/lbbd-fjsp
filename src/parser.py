import json
from dataclasses import dataclass

# Dataclass for type validation and structure
@dataclass
class FJSPInstance:
    name: str
    num_jobs: int
    num_machines: int
    num_operations: int
    jobs: dict[int, list[int]]                    # job_id → ordered operation IDs
    options: dict[int, list[tuple[int, int]]]     # op_id → [(machine, duration), ...]

def parse_instance(instance_path):

    # Load data
    with open(instance_path, 'r') as f:
        data = json.load(f)

    # get jobs from dict
    jobs = data.get("precedences", [])
    jobs_dict = {}
    for job in jobs:
        job_id = job[2]

        if job_id not in jobs_dict:
            # unique jobs
            jobs_dict[job_id] = set()
        jobs_dict[job_id].add(job[0])
        jobs_dict[job_id].add(job[1])
        

    # get number of jobs
    num_jobs = len(jobs_dict)
    
    # get options from dict
    options = data.get("operations", [])
    options_dict = {}
    for option in options:
        operation_id = option.get("operation")
        machine_id = option.get("machine")
        duration = option.get("duration")
        if operation_id not in options_dict:
            options_dict[operation_id] = []
        options_dict[operation_id].append((machine_id, duration))
    
    # get number of jobs operations
    num_jobs_operations = len(options_dict)    
    
    # get number of machines
    num_machines = max([max([op[0] for op in ops]) for ops in options_dict.values()]) + 1
    
    return FJSPInstance(
        name=data.get("instance", ""),
        num_jobs=num_jobs,
        num_machines=num_machines,
        num_operations=num_jobs_operations,
        jobs={k: sorted(v) for k, v in jobs_dict.items()},
        options=options_dict,
    )



if __name__ == "__main__":
    data = parse_instance("data/mk01.json")
    print(data)
