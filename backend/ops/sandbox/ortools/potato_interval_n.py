# backend/ops/sandbox/ortools/potato_interval_n.py
from ortools.sat.python import cp_model



def main() -> None:
    model = cp_model.CpModel()



    # じゃがいも個数
    # 変更したければここだけ触る
    n_potatoes = 5



    # 時間上限 (分)
    # n_potatoes に合わせて雑に広げる
    # 厳密でなくて OK
    horizon = n_potatoes * 2 + 10



    # 皮むき 1 個 = 1 分
    dur = 1



    # 変数・区間タスクを「リスト」で管理する
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



    # 制約: 人を 1 人とし、皮むきは同時にできない (重なり禁止)
    model.add_no_overlap(intervals)



    makespan = model.new_int_var(0, horizon, "makespan")

    # makespan の定義: makespan = max(ends)
    model.add_max_equality(makespan, ends)

    # 目的: 全部終わる時刻が一番早くなる並べ方を探す
    model.minimize(makespan)



    solver = cp_model.CpSolver()

    status = solver.solve(model)



    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No solution")

        return



    # n_potatoes = 5
    print("n_potatoes =", n_potatoes)

    # makespan = 5 min
    print("makespan =", solver.value(makespan), "min")



    # potato0 peel: 1-2
    # potato1 peel: 0-1
    # potato2 peel: 2-3
    # potato3 peel: 4-5
    # potato4 peel: 3-4
    for i in range(n_potatoes):
        print\
        (
            f"potato{i} peel: "
            f"{solver.value(starts[i])}-{solver.value(ends[i])}"
        )



if __name__ == "__main__":
    main()
