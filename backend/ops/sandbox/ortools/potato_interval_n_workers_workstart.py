# backend/ops/sandbox/ortools/potato_interval_n_workers_workstart.py
from ortools.sat.python import cp_model



def main() -> None:
    model = cp_model.CpModel()

    # 前提
    n_potatoes = 5
    workers = 2
    work_start = 5

    dur = 1

    horizon = work_start + n_potatoes * dur + 10



    starts: list[cp_model.IntVar] = []
    ends: list[cp_model.IntVar] = []
    intervals: list[cp_model.IntervalVar] = []

    for i in range(n_potatoes):
        s = model.new_int_var(0, horizon, f"potato{i}_peel_start")
        e = model.new_int_var(0, horizon, f"potato{i}_peel_end")
        job = model.new_interval_var(s, dur, e, f"potato{i}_peel")

        # 追加
        # 稼働開始前には開始できない
        model.add(work_start <= s)

        starts.append(s)
        ends.append(e)
        intervals.append(job)

    # 資源制約: 同時に workers 個まで皮をむける
    # 各仕事は人数 1 を消費
    model.add_cumulative(intervals, [1] * n_potatoes, workers)



    # 目的: 全部終わる時刻 (最大終了) を最小化
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

    # work_start = 5 min
    print("work_start =", work_start, "min")

    # makespan = 8 min
    print("makespan =", solver.value(makespan), "min")



    # potato0 peel: 5-6
    # potato1 peel: 5-6
    # potato2 peel: 6-7
    # potato3 peel: 7-8
    # potato4 peel: 6-7
    for i in range(n_potatoes):
        print(f"potato{i} peel: {solver.value(starts[i])}-{solver.value(ends[i])}")



if __name__ == "__main__":
    main()
