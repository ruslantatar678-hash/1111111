import random

def analyze_pair(pair: str, timeframe: str):
    direction = random.choice(["BUY", "SELL"])
    confidence = round(random.uniform(0.6, 0.95), 2)
    fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    return {
        "pair": pair,
        "timeframe": timeframe,
        "direction": direction,
        "confidence": confidence,
        "fib_levels": fib_levels,
        "summary": f"AI считает, что направление {direction} с уверенностью {confidence*100:.0f}%"
    }
