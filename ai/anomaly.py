HEART_RATE_MIN = 40
HEART_RATE_MAX = 120
BP_MIN = 90
BP_MAX = 180

def check_record(record, previous=None):
    hr = record.get("heartRate", 0)
    bp = record.get("systolicBP", 0)
    age = record.get("age", 30)
    diagnosis = record.get("diagnosis", "").lower()

    reasons = []

    if hr < HEART_RATE_MIN or hr > HEART_RATE_MAX:
        reasons.append("Heart rate abnormal")

    if bp < BP_MIN or bp > BP_MAX:
        reasons.append("BP abnormal")

    if previous:
        if abs(hr - previous.get("heartRate", hr)) > 40:
            reasons.append("Sudden HR change")

    if age < 25 and "dementia" in diagnosis:
        reasons.append("Age-diagnosis mismatch")

    if reasons:
        return "SUSPICIOUS"
    return "NORMAL"


# TEST
print(check_record({
    "patientId": "P1",
    "heartRate": 80,
    "systolicBP": 120,
    "age": 30,
    "diagnosis": "normal"
}))

print(check_record({
    "patientId": "P2",
    "heartRate": 200,
    "systolicBP": 250,
    "age": 30,
    "diagnosis": "normal"
}))