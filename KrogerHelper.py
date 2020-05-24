stores = {
    1: {
        'label': 'Kroger',
        'domain': 'kroger.com'
    },
    2: {
        'label': 'Ralphs',
        'domain': 'ralphs.com'
    },
    3: {
        'label': 'Baker’s',
        'domain': 'bakersplus.com'
    },
    4: {
        'label': 'City Market',
        'domain': 'citymarket.com'
    },
    5: {
        'label': 'Dillons',
        'domain': 'dillons.com'
    },
    6: {
        'label': 'Food 4 Less',
        'domain': 'food4less.com'
    },
    7: {
        'label': 'Fred Meyer',
        'domain': 'fredmeyer.com'
    },
    8: {
        'label': 'Fry’s',
        'domain': 'frysfood.com'
    },
    9: {
        'label': 'Smith’s Food and Drug',
        'domain': 'smithsfoodanddrug.com'
    },
}

survey_mandatory_fields = ['first_name', 'last_name', 'email_address', 'loyalty_card_number', 'mobile_phone',
                           'address_line1', 'city', 'state', 'zip']
survey_field_labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email_address': 'Email Address',
                       'loyalty_card_number': 'Loyalty Card Number', 'mobile_phone': 'Mobile Phone',
                       'address_line1': 'Address Line 1', 'city': 'City', 'state': 'State (2 letters abbreviation)',
                       'zip': 'Zip Code'}


def process_purchases_summary(purchases):
    default_dict = {
        'total': 0.00,
        'total_savings': 0.00,
        'store_visits': 0,
    }
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
