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


def map_account_info(config, account_info):
    if account_info['firstName']:
        config['profile']['first_name'] = account_info['firstName']
    if account_info['lastName']:
        config['profile']['last_name'] = account_info['lastName']
    if account_info['emailAddress']:
        config['profile']['email_address'] = account_info['emailAddress']
    if account_info['loyaltyCardNumber']:
        config['profile']['loyalty_card_number'] = account_info['loyaltyCardNumber']
    if account_info['mobilePhoneNumber']:
        config['profile']['mobile_phone'] = account_info['mobilePhoneNumber']

    if account_info['address']['addressLine1']:
        config['profile']['address_line1'] = account_info['address']['addressLine1']
    if account_info['address']['addressLine2']:
        config['profile']['address_line2'] = account_info['address']['addressLine2']
    if account_info['address']['city']:
        config['profile']['city'] = account_info['address']['city']
    if account_info['address']['stateCode']:
        config['profile']['state'] = account_info['address']['stateCode']
    if account_info['address']['zip']:
        config['profile']['zip'] = account_info['address']['zip']

    return config
