def gather_stats(results: dict[tuple[str, str], int]):
    ## Your code here
    dd = results[("depots", "depots")]
    dl = results[("depots", "laundromats")]
    ld = results[("laundromats", "depots")]
    ll = results[("laundromats", "laundromats")]

    n = dd + dl + ld + ll
    accuracy = (dd + ll) / n 
    recall = dd + ld
    recall = dd / recall 
    precision = dd + dl
    precision = dd / precision 
    f1 = precision + recall
    f1 = 2 * ((precision * recall) / f1)
    
    return {
        "n": n,
        "accuracy": accuracy,
        "recall": recall,
        "precision": precision,
        "f1": f1,
    }
