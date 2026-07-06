PERFORMANCE_LABELS = {
    1: "Low",
    2: "Good",
    3: "Excellent",
    4: "Outstanding",
}

PERFORMANCE_COLORS = {
    1: "#e74c3c",
    2: "#f39c12",
    3: "#2ecc71",
    4: "#9b59b6",
}

PERFORMANCE_EMOJI = {
    1: "🔴",
    2: "🟡",
    3: "🟢",
    4: "⭐",
}


def rating_label(rating: int) -> str:
    emoji = PERFORMANCE_EMOJI.get(rating, "")
    label = PERFORMANCE_LABELS.get(rating, str(rating))
    return f"{emoji} {label}"


def rating_color(rating: int) -> str:
    return PERFORMANCE_COLORS.get(rating, "#888")
