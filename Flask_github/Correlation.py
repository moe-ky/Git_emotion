from scipy.stats.stats import pearsonr


def correlation():
    price = [101.610001, 105.199997, 103.470001, 104.56999999999999]
    contentment = [120, 204, 226, 141]

    correl = pearsonr(price, contentment)
    print(correl[0])

    if correl[0] >= 0.5:
        print("BUY")
        return "BUY"
    else:
        print("No BUY")
        return "NO BUY"


correlation()