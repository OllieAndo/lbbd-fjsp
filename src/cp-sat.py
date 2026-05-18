from ortools.sat.python import cp_model
from parser import parse_instance

def solve(instance_path):
    instance = parse_instance(instance_path)
    model = cp_model.CpModel()

    horizon = sum(max(d for _, d in ops) for ops in instance.options.values())
    print(f"Horizon: {horizon}")

    # Binary assignment variables
    x = {}
    for op_id, ops in instance.options.items():
        for machine, duration in ops:
            x[(op_id, machine)] = model.NewBoolVar(f"x_{op_id}_{machine}")

    for op_id, ops in instance.options.items():
        model.AddExactlyOne(x[(op_id, machine)] for machine, _ in ops)

    # Start/end times and optional interval variables
    starts = {}
    ends = {}
    intervals = {}
    machine_intervals = {m: [] for m in range(instance.num_machines)}

    for op_id, ops in instance.options.items():
        starts[op_id] = model.NewIntVar(0, horizon, f"start_{op_id}")
        ends[op_id] = model.NewIntVar(0, horizon, f"end_{op_id}")

        for machine, duration in ops:
            intervals[op_id, machine] = model.NewOptionalIntervalVar(
                starts[op_id], duration, ends[op_id],
                x[op_id, machine],
                f"interval_{op_id}_{machine}"
            )
            machine_intervals[machine].append(intervals[op_id, machine])

    # No-overlap constraints for each machine
    for m in range(instance.num_machines):
        model.AddNoOverlap(machine_intervals[m])

    # Precedence constraints for each job
    for job_id, ops in instance.jobs.items():
        for i in range(len(ops) - 1):
            model.Add(ends[ops[i]] <= starts[ops[i + 1]])

    # Objective: minimise makespan
    makespan = model.NewIntVar(0, horizon, 'makespan')
    for op_id in instance.options:
        model.Add(makespan >= ends[op_id])
    model.Minimize(makespan)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Makespan: {int(solver.Value(makespan))}")
    else:
        print("No solution found")

    return int(solver.Value(makespan)) if status == cp_model.OPTIMAL else None

if __name__ == "__main__":
    solve("data/mk01.json")

