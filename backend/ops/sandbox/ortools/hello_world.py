# backend/ops/sandbox/ortools/hello_world.py
from ortools.sat.python import cp_model



def main() -> None:
    # model: 変数、制約、目的を積んでいくルールブック
    model = cp_model.CpModel()



    # 変数 x の範囲
    x = model.new_int_var(0, 10, "x")

    # 制約を追加    
    model.add(x <= 7)

    # 目的は x を最大化
    model.maximize(x)



    # solver: ルールを満たす答えを探すもの
    solver = cp_model.CpSolver()

    # solve(): 探索実行
    # status: 解が見つかったか、最適解かなどの結果を含む
    status = solver.solve(model)



    # OPTIMAL: 最適解が見つかった
    # FEASIBLE: 解は見つかったが、最適性は未保証
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # x = 7
        print("x =", solver.value(x))

    else:
        print("No solution")



if __name__ == "__main__":
    main()
