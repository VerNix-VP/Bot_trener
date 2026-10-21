def one_rep_max(w, r):
    if r == 1:
        return w
    return w * (1 + r / 30)


def round_to_plates(w):
    return round(w / 2.5) * 2.5


def make_plan(rm):
    plan = []
    for p, r in [(0.7, 5), (0.8, 3), (0.9, 1)]:
        plan.append((round_to_plates(rm * p), r))
    return plan


def best_max(entries):
    best = 0
    for e in entries:
        rm = one_rep_max(e["weight"], e["reps"])
        if rm > best:
            best = rm
    return best
