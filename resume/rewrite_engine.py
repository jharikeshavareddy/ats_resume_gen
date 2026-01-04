def rewrite_summary(summary, keywords):
    if not keywords:
        return summary
    return summary + " Skilled in " + ", ".join(keywords[:4]) + "."
