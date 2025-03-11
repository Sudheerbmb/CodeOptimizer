from flask import Flask, render_template, request
import markdown
from langchain_groq import ChatGroq

app = Flask(__name__)

groq_api_key = "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"

models = ["llama-3.1-8b-instant"]

def get_optimized_code(code, model_name):
    llm = ChatGroq(api_key=groq_api_key, model=model_name)
    prompt = f"""
    You are an expert in algorithm design and performance optimization. Your task is to analyze the provided Python code for potential improvements in efficiency, scalability, and overall performance. Focus on both time and space complexity, as well as best practices for optimization.

    **Instructions**:
    1. **Code Analysis**: Thoroughly analyze the given code to identify:
        - Any bottlenecks or performance inefficiencies.
        - Opportunities to improve time complexity (e.g., reducing algorithmic complexity or optimizing loops).
        - Opportunities to reduce memory usage, such as using more efficient data structures or algorithms.
        - Any parts of the code that could benefit from parallelization, concurrency, or memoization.
        - Potential areas where Python-specific optimizations (e.g., list comprehensions, built-in functions) can be leveraged.

    2. **Optimized Code**: Provide an optimized version of the code that incorporates your suggestions. The code should be refactored to:
        - Reduce time complexity where possible.
        - Reduce space complexity by using memory-efficient data structures and techniques.
        - Ensure that the solution is scalable and can handle larger inputs or more complex use cases.

    3. **Explanations**:
        - **Time Complexity**: Include a detailed explanation of the time complexity of both the original and optimized code. Specify how you reduced the time complexity and why the new approach is better.
        - **Space Complexity**: Similarly, explain the space complexity of the original vs. optimized code. Discuss any changes made to reduce memory usage and optimize the code’s footprint.
        - **Best Practices**: Discuss any Python best practices that were applied to make the code cleaner, more maintainable, and more efficient.

    4. **Edge Cases**: Consider any potential edge cases or input variations that could affect the performance of the code. How would the code perform with very large inputs, complex data structures, or highly concurrent operations? Suggest further improvements if necessary.

    5. **Additional Considerations**: If applicable, recommend any relevant libraries or tools that could further optimize or improve the code, especially for performance, debugging, or profiling.

    Code to optimize:
    python
    {code}
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
