# backend/ops/sandbox/ortools/potato_interval_min_workstart.py
from ortools.sat.python import cp_model



def main() -> None:
    model = cp_model.CpModel()



    # 最悪ケースを想定した、探索時間の上限
    horizon = 10



    # 追加

    # 工場の稼働開始時間
    # この時刻より前は開始できない

    # 0 を 09:00 と見立てるなら
    # work_start = 5 は「09:05 以降に開始」
    work_start = 5



    # じゃがいも 2 個の皮むきという仕事を「区間タスク」として作る
    # 皮むきは 1 個 = 1 分 とする
    dur = 1



    s0 = model.new_int_var(0, horizon, "potato0_peel_start")
    e0 = model.new_int_var(0, horizon, "potato0_peel_end")

    """
    s0:  未確定の整数
    dur: 1 分で固定
    e0:  未確定の変数

    e0 = s0 + dur
    dur = 1 のとき
    s0 = 3 ⇒ e0 = 4
    """
    job0 = model.new_interval_var(s0, dur, e0, "potato0_peel")

    s1 = model.new_int_var(0, horizon, "potato1_peel_start")
    e1 = model.new_int_var(0, horizon, "potato1_peel_end")
    job1 = model.new_interval_var(s1, dur, e1, "potato1_peel")



    # 追加
    # 稼働開始前には作業を開始できない（開始可能時刻の制約）
    model.add(work_start <= s0)
    model.add(work_start <= s1)



    # 人を 1 人とし、皮むきは同時にできない (重なり禁止)
    model.add_no_overlap([job0, job1])



    makespan = model.new_int_var(0, horizon, "makespan")

    # makespan の定義: makespan = max(e0, e1)
    model.add_max_equality(makespan, [e0, e1])

    # 目的: 全部終わる時刻が一番早くなる並べ方を探す
    model.minimize(makespan)



    solver = cp_model.CpSolver()

    status = solver.solve(model)



    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No solution")

        return


    # work_start = 5 min
    print("work_start =", work_start, "min")

    # makespan = 7 min
    print("makespan =", solver.value(makespan), "min")


    # potato0 peel: 6 - 7
    print("potato0 peel:", solver.value(s0), "-", solver.value(e0))

    # potato1 peel: 5 - 6
    print("potato1 peel:", solver.value(s1), "-", solver.value(e1))



if __name__ == "__main__":
    main()
