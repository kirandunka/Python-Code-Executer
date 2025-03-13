from flask import Flask, render_template, request, jsonify
import ast, io, contextlib

app = Flask(__name__)

def analyze_code(code):
    """
    Analyzes the provided Python code using AST and returns a friendly explanation.
    """
    explanation = []
    try:
        tree = ast.parse(code)
        explanation.append("Hey there! Let’s break down your code together:")
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                explanation.append("• I see a 'for' loop – perfect for iterating over items!")
            elif isinstance(node, ast.While):
                explanation.append("• There's a 'while' loop – great for running code until a condition changes!")
            elif isinstance(node, ast.If):
                explanation.append("• An 'if' statement is in use – this helps make decisions in your code!")
            elif isinstance(node, ast.FunctionDef):
                explanation.append(f"• You defined a function called '{node.name}' – functions keep your code neat!")
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id'):
                    explanation.append(f"• You're calling the function '{node.func.id}' – nice work!")
                elif hasattr(node.func, 'attr'):
                    explanation.append(f"• A method '{node.func.attr}' is being used – cool!")
        explanation.append("Keep up the great work!")
        return "\n".join(explanation)
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

def run_code(code):
    """
    Executes the given Python code and captures its output.
    (Note: This is for learning purposes in a controlled environment.)
    """
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {})
    except Exception as e:
        buffer.write(f"\nError while running code: {str(e)}")
    return buffer.getvalue()

def code_insights(code):
    """
    Computes unique metrics of the code such as number of lines, functions, loops, etc.
    """
    insights = {}
    try:
        tree = ast.parse(code)
        insights["Lines of Code"] = len(code.splitlines())
        insights["Functions"] = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
        insights["Loops"] = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
        insights["Conditionals"] = sum(isinstance(node, ast.If) for node in ast.walk(tree))
        insights["Function Calls"] = sum(isinstance(node, ast.Call) for node in ast.walk(tree))
    except Exception as e:
        insights["error"] = str(e)
    return insights

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    code = data.get("code", "")
    explanation = analyze_code(code)
    output = run_code(code)
    insights = code_insights(code)
    return jsonify({
        "explanation": explanation,
        "output": output,
        "insights": insights
    })

if __name__ == "__main__":
    app.run(debug=True)
