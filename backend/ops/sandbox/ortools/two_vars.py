# backend/ops/sandbox/ortools/two_vars.py
from ortools.sat.python import cp_model



def main() -> None:
    model = cp_model.CpModel()


    # 変数 x, y の範囲
    x = model.new_int_var(0, 10, "x")
    y = model.new_int_var(0, 10, "y")

    # 制約
    model.add(x + y <= 10)

    # 目的は x + y を最大化
    model.maximize(x + y)



    solver = cp_model.CpSolver()

    status = solver.solve(model)



    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        xv = solver.value(x)
        yv = solver.value(y)

        # 最適解 (x, y) の組が 11 通りある

        # 今回の実行結果: x = 0
        print("x =", xv)

        # 今回の実行結果: y = 10
        print("y =", yv)

        

        # 最適値 (x + y) 10 で一意である
        
        # x + y = 10
        print("x + y =", xv + yv)

    else:
        print("No solution")



if __name__ == "__main__":
    main()
