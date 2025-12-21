# backend/ops/sandbox/ortools/potato_interval_n_workers.py
from ortools.sat.python import cp_model



def main() -> None:
    model = cp_model.CpModel()

    # 皮むき対象のじゃがいも個数
    n_potatoes = 5

    # 皮むき担当人数
    workers = 2

    # 時間上限
    horizon = n_potatoes * 2 + 10

    # 皮むき 1 個 = 1 分
    dur = 1



    starts: list[cp_model.IntVar] = []
    ends: list[cp_model.IntVar] = []
    intervals: list[cp_model.IntervalVar] = []

    for i in range(n_potatoes):
        s = model.new_int_var(0, horizon, f"potato{i}_peel_start")
        e = model.new_int_var(0, horizon, f"potato{i}_peel_end")
        job = model.new_interval_var(s, dur, e, f"potato{i}_peel")

        starts.append(s)
        ends.append(e)
        intervals.append(job)



    # 資源制約: 同時に workers 個まで皮をむける
    # 
    # demands: 各仕事が消費する人数 = [1, 1, 1, 1, 1]
    # capacity: 同時に使える人数 = workers
    model.add_cumulative(intervals, [1] * n_potatoes, workers)

    # model.add_no_overlap(intervals)



    makespan = model.new_int_var(0, horizon, "makespan")

    model.add_max_equality(makespan, ends)

    model.minimize(makespan)



    solver = cp_model.CpSolver()

    status = solver.solve(model)



    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No solution")

        return



    # n_potatoes = 5
    print("n_potatoes =", n_potatoes)

    # workers = 2
    print("workers =", workers)

    # makespan = 3 min
    print("makespan =", solver.value(makespan), "min")



    # potato0 peel: 0-1
    # potato1 peel: 0-1
    # potato2 peel: 1-2
    # potato3 peel: 2-3
    # potato4 peel: 1-2
    for i in range(n_potatoes):
        print(f"potato{i} peel: {solver.value(starts[i])}-{solver.value(ends[i])}")



if __name__ == "__main__":
    main()
