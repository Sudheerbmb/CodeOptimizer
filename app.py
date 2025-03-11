from flask import Flask, render_template, request
import markdown
from langchain_groq import ChatGroq

app = Flask(__name__)

groq_api_key = "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"

models = ["llama-3.1-8b-instant"]

def get_optimized_code(code, model_name):
    llm = ChatGroq(api_key=groq_api_key, model=model_name)
    prompt = f"""
    Optimize the provided Python code for time and space complexity, using the most efficient algorithms and data structures. 
    Provide the optimized code along with time and space complexities for both original and optimized versions. 
    Briefly explain the key improvements and alternatives considered.
    Code to optimize: {code}
    """
    response = llm.invoke(prompt)
    return markdown.markdown(response.content) if response else "Error optimizing code."



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]
        model = request.form["model"]
        optimized_code = get_optimized_code(code, model)
        return render_template("index.html", models=models, optimized_code=optimized_code, code=code)
    return render_template("index.html", models=models, optimized_code=None, code=None)

if __name__ == "__main__":
    app.run(debug=True)
