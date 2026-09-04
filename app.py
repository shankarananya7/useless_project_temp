from flask import Flask, render_template, request

app = Flask(__name__)

def predict_scenery(route, side, seat):
    # Fun, intentionally "useless" prediction logic
    seed = sum(ord(c) for c in (route + side + seat).lower())
    score = round(5 + (seed % 41) / 10, 1)
    trees = 40 + (seed % 51)
    buildings = 10 + ((seed // 3) % 31)
    wall = max(1, 100 - trees - buildings)
    return score, trees, buildings, wall

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        route = request.form.get("route", "").strip()
        side = request.form.get("side", "")
        seat = request.form.get("seat", "").strip()
        if route and side and seat:
            score, trees, buildings, wall = predict_scenery(route, side, seat)
            result = {
                "route": route,
                "side": side.title(),
                "seat": seat.upper(),
                "score": score,
                "trees": trees,
                "buildings": buildings,
                "wall": wall
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
