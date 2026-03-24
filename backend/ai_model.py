def predict_risk(age: int, bp: int, sugar: int):
    score = 0

    if age > 45:
        score += 1
    if bp > 130:
        score += 1
    if sugar > 140:
        score += 1

    if score >= 2:
        return "HIGH RISK"
    return "LOW RISK"