# from flask import Flask
# from flask_wtf import FLa
#
# app = Flask(__name__)
#
# @app.route("/calc")
# def hello_world():
#     return "<p>Hello, World!</p>"
#
#
from flask import Flask, render_template, request

from get_carbon_impact import get_carbon_impact_dict, get_fuel_impact
from co2_impacts import co2_impacts
from co2_impacts_poore import ghg_poore as ghg

app = Flask(__name__)

food_options = co2_impacts


@app.route("/")
def index():
    return render_template("index.html", food_options=food_options)


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        foods = request.form.getlist("food[]")
        quantities = request.form.getlist("quantity[]")
        total_CO2 = 0.0
        results = "<h2>Results:</h2>"

        # You can now process the foods and quantities as needed
        for food, quantity in zip(foods, quantities):
            incremental_co2_impact = "{:.2f}".format(
                get_carbon_impact_dict(food, float(quantity))
            )
            total_CO2 += float(incremental_co2_impact)
            results += f"<p>Food: {food}, Quantity: {quantity}. The carbon impact of this ingredient is {incremental_co2_impact} Kg CO<sub>2</sub>e.</p>"

        results += f"<p>The total CO2 impact of this meal was {'{:.2f}'.format(total_CO2)} Kg CO<sub>2</sub>e.</p>"

        return results

        # (f"Food: {food}, Quantity: {quantity}. The carbon impact of this ingredient is {incremental_co2_impact} Kg of CO2e.\n"
        #    f"The total CO2 impact of this meal was {'{:.2f}'.format(total_CO2)} Kg of CO2e.")


if __name__ == "__main__":
    app.run(debug=True)
