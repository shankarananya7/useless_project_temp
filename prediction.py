import random


# How valuable each scenery type is
SCENERY_VALUES = {

    "trees": 9,

    "water": 10,

    "fields": 8,

    "mountains": 10,

    "buildings": 4,

    "walls": 1

}


# Different window sides slightly change the prediction
SIDE_FACTORS = {

    "Left": {

        "trees": 1.10,
        "water": 1.15,
        "fields": 1.05,
        "mountains": 1.10,
        "buildings": 0.90,
        "walls": 0.90

    },

    "Right": {

        "trees": 0.95,
        "water": 0.90,
        "fields": 0.95,
        "mountains": 0.90,
        "buildings": 1.05,
        "walls": 1.05

    }

}


# Different coaches get tiny adjustments
COACH_FACTORS = {

    "S1": 1.00,
    "S2": 1.02,
    "S3": 1.01,
    "S4": 0.98,
    "S5": 1.04,
    "S6": 0.97

}


def apply_side_factor(scenery, side):

    adjusted = {}

    for item, value in scenery.items():

        factor = SIDE_FACTORS[side][item]

        adjusted[item] = value * factor

    return adjusted


def calculate_scenery_score(scenery):

    score = 0

    for item, probability in scenery.items():

        score += probability * SCENERY_VALUES[item]

    return score


def calculate_seat_factor(seat):

    random.seed(seat)

    return random.uniform(-0.35, 0.35)


def calculate_photo_score(scenery):

    score = (

        scenery["water"] * 100 * 0.30

        + scenery["mountains"] * 100 * 0.30

        + scenery["trees"] * 100 * 0.20

        + scenery["fields"] * 100 * 0.10

        + (1 - scenery["buildings"]) * 100 * 0.10

    )

    return round(min(100, score))


def calculate_regret(score):

    regret = 100 - (score * 10)

    return round(max(1, min(99, regret)))


def calculate_confidence():

    return random.randint(87, 96)


def sun_exposure(time, side):

    hour = int(time.split(":")[0])


    if 6 <= hour <= 9:

        if side == "Left":

            return "HIGH"

        else:

            return "LOW"


    elif 16 <= hour <= 18:

        if side == "Right":

            return "HIGH"

        else:

            return "LOW"


    else:

        return "MODERATE"


def generate_verdict(score):

    if score >= 9:

        return "PERFECT SEAT. DO NOT LET YOUR FRIENDS KNOW."

    elif score >= 8:

        return "EXCELLENT VIEW. MAIN-CHARACTER ENERGY DETECTED."

    elif score >= 7:

        return "GOOD SEAT. KEEP YOUR PHONE CHARGED."

    elif score >= 5:

        return "DECENT VIEW. YOU WILL SURVIVE."

    elif score >= 3:

        return "BUILDINGS HAVE ENTERED THE CHAT."

    else:

        return "CONGRATULATIONS. YOU GOT THE WALL."


def friend_jealousy(score):

    jealousy = score * 10 + 5

    return round(min(99, jealousy))


def predict(route_data, seat, side, time, coach):

    # Get route scenery
    scenery = route_data["scenery"]


    # Adjust scenery according to window side
    scenery = apply_side_factor(scenery, side)


    # Calculate basic score
    score = calculate_scenery_score(scenery)


    # Tiny seat-specific variation
    score += calculate_seat_factor(seat)


    # Coach adjustment
    score *= COACH_FACTORS.get(coach, 1)


    # Keep score between 1 and 10
    score = max(1, min(10, score))


    # Calculate percentages
    total = sum(scenery.values())

    percentages = {}

    for item, value in scenery.items():

        percentages[item] = round(
            (value / total) * 100
        )


    # Other predictions
    photo_score = calculate_photo_score(scenery)

    regret = calculate_regret(score)

    confidence = calculate_confidence()

    sun = sun_exposure(time, side)

    verdict = generate_verdict(score)

    jealousy = friend_jealousy(score)


    return {

        "score": round(score, 1),

        "percentages": percentages,

        "photo_score": photo_score,

        "regret": regret,

        "confidence": confidence,

        "sun": sun,

        "verdict": verdict,

        "jealousy": jealousy

    }
def find_best_seat(route_data, side, time, coach):

    best_seat = 1
    best_result = None

    for seat in range(1, 73):

        result = predict(
            route_data,
            seat,
            side,
            time,
            coach
        )

        if best_result is None or result["score"] > best_result["score"]:

            best_seat = seat
            best_result = result

    return best_seat, best_result