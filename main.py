# lb script is created on 19/12/2025 14:00:00
import ast

def safe_calculate(expression):
        #第一步：过滤非法字符，只保留数字、+-*/和括号
        allowed_chars = "0123456789+-*/()"
        filtered = [c for  c in expression if c in allowed_chars]
        filtered_exp = ''.join(filtered)

        if not filtered_exp:
            return "输入中无有效运算表达式"
        if expression != filtered_exp:
            print(f"提示：已自动剔除非法字符，实际计算：{filtered_exp}")

        try:
            tree = ast.parse(filtered_exp, mode='eval')
            result = eval(compile(tree, filename='', mode='eval'), {"__builtins__": None}, {})
            return result
        except SyntaxError:
            return "表达式语法错误（如缺少操作数、运算符不匹配）"
        except ZeroDivisionError:
            return "除数不能为0"
        except Exception as e:
            return f"计算错误：{str(e)}"

def report_bug(error_type):
    """根據傳入的錯誤類型列印提示（補充參數檢查）"""
    # 新增：避免未傳入錯誤類型時報錯
    if not error_type:
        print("未知錯誤：未指定錯誤類型")
        return
    if error_type == "NameError":
        print("NameError: 名稱拼寫錯誤或變數未定義")
    # print(f"NameError: name '{c[0]}' is not defined, lb_script report")
    elif error_type == "KeyError":
        print("KeyError: 找不到該鍵對應的值")
    else:
        print(f"未知錯誤類型：{error_type}")  # 新增：支援自訂錯誤提示

var_set = {}  # 用於儲存變數的字典

# ==============================================================================#
def run(token):
    # 宣告使用全域變數（避免UnboundLocalError）
    global user
    # 新增：分割前檢查指令是否為空（避免split報錯）
    if not user.strip():
        # print("提示：請輸入有效指令（例如 var/a=1、show.var/a）")
        pass
        return
    # ==============================================================================#
    if token == "show":
        # 新增：檢查是否有第二個參數（避免IndexError）
        if len(c) < 2:
            print("用法錯誤：show/後需跟內容（例如 show/Hello）")
            return
        else:
            print(c[1])
    # ==============================================================================#
    elif token == "get":
        if len(c) < 2:
            print("用法錯誤：get/後需跟變數名（例如 get.var/a）")
        else:
            var_name = c[1]
            # 優化：使用get時添加預設提示，更直觀
            print(f"變數 {var_name} 的值：{var_set.get(var_name, '未定義')}")
    # ==============================================================================#
    elif token == "enter":
        if len(c) < 2:
            print("用法錯誤：enter/後需跟輸入提示（例如 enter/請輸入姓名）")
        else:
            put = input(c[1] + "\n~< ")
            print("~> ", put)
    # ==============================================================================#
    elif "." in token and "enter" in token:
        done = token.split(".")
        value = input(f"{c[1]}\n~< ")
        name = done[1].strip()  # 新增：去除前後空格，增強容錯性
        var_set[name] = value
        print(f"var_name = {name}\nvar_value = {value}")
    # ==============================================================================#
    elif "=" in token:
        temporary = token.split('=')  # 直接用已分割的c，避免重複split
        if len(temporary) != 2:
            print("語法錯誤：請使用 '變數名=值' 格式（例如 a=123）")
            return
        name = temporary[0].strip()  # 新增：去除前後空格，增強容錯性
        value = temporary[1].strip()
        var_set[name] = value
        print(f"var_name = {name}\nvar_value = {value}")  # 優化：f-string更簡潔
    #==============================================================================#
    elif "+" in token or "-" in token or "*" in token or "/" in token:
        print(safe_calculate(token))
    #==============================================================================#
    elif token == "printall":
        print("所有儲存的變數：", var_set)  # 拆分print和printall，語義更清晰
    # ==============================================================================#
    elif token == " ":
        pass
    # ==============================================================================#
    else:
        # 調用report_bug時傳入錯誤類型（修復原程式參數缺失問題）
        report_bug("NameError")
    # ==============================================================================#
# 主迴圈：接收使用者輸入
while True:
    user = input("~")
    if user == "exit":
        print("程式結束～")  # 新增：退出提示，體驗更好
        break
    else:
        c = user.split("\\",1)
        run(c[0])
# ==============================================================================#