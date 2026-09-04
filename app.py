from flask import Flask, render_template, request

from data import ROUTES

from prediction import predict, find_best_seat


app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/predict", methods=["POST"])
def prediction():

    route_key = request.form["route"]

    train = request.form["train"]

    coach = request.form["coach"]

    seat = int(request.form["seat"])

    side = request.form["side"]

    time = request.form["time"]


    # Get information about the selected route
    route_data = ROUTES[route_key]


    # Ask our prediction brain to analyse the seat
    result = predict(
        route_data,
        seat,
        side,
        time,
        coach
    )


    # Send everything to the result page
    return render_template(

        "result.html",

        route=route_data["name"],

        train=train,

        coach=coach,

        seat=seat,

        side=side,

        time=time,

        result=result

    )

@app.route("/best-seat", methods=["POST"])
def best_seat():

    route_key = request.form["route"]
    coach = request.form["coach"]
    side = request.form["side"]
    time = request.form["time"]

    route_data = ROUTES[route_key]

    seat, result = find_best_seat(
        route_data,
        side,
        time,
        coach
    )

    return render_template(
        "bestseat.html",
        route=route_data["name"],
        coach=coach,
        side=side,
        time=time,
        seat=seat,
        result=result
    )
if __name__ == "__main__":

    app.run(debug=True)