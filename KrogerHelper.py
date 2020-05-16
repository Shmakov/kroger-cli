default_dict = {
    'total': 0.00,
    'total_savings': 0.00,
    'store_visits': 0,
}


def process_purchases_summary(purchases):
    years = {}
    total = dict(default_dict)
    first_purchase = None
    last_purchase = None

    for purchase in purchases:
        if first_purchase is None:
            first_purchase = purchase

        last_purchase = purchase

        year = int(purchase['transactionTime'][:4])
        if year not in years:
            years[year] = dict(default_dict)

        if 'total' in purchase:
            years[year]['total'] += purchase['total']
            years[year]['store_visits'] += 1
            total['total'] += purchase['total']
            total['store_visits'] += 1

        if 'totalSavings' in purchase:
            years[year]['total_savings'] += purchase['totalSavings']
            total['total_savings'] += purchase['totalSavings']

    if last_purchase is None:
        return None

    return {
        'years': years,
        'total': total,
        'first_purchase': first_purchase,
        'last_purchase': last_purchase,
    }
