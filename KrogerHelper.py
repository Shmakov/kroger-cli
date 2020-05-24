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
                           'address_line1', 'city', 'state', 'zip', 'age']
survey_field_labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email_address': 'Email Address',
                       'loyalty_card_number': 'Loyalty Card Number', 'mobile_phone': 'Mobile Phone',
                       'address_line1': 'Address Line 1', 'city': 'City', 'state': 'State (2 letters abbreviation)',
                       'zip': 'Zip Code', 'age': 'Age'}

survey_states_mapping = {'AL': 1, 'AK': 2, 'AZ': 3, 'AR': 4, 'CA': 5, 'CO': 6, 'CT': 7, 'DE': 8, 'DC': 9, 'FL': 10,
                         'GA': 11, 'HI': 12, 'ID': 13, 'IL': 14, 'IN': 15, 'IA': 16, 'KS': 17, 'KY': 18, 'LA': 19,
                         'ME': 20, 'MD': 21, 'MA': 22, 'MI': 23, 'MN': 24, 'MS': 25, 'MO': 26, 'MT': 27, 'NE': 28,
                         'NV': 29, 'NH': 30, 'NJ': 31, 'NM': 32, 'NY': 33, 'NC': 34, 'ND': 35, 'OH': 36, 'OK': 37,
                         'OR': 38, 'PA': 39, 'PR': 40, 'RI': 41, 'SC': 42, 'SD': 43, 'TN': 44, 'TX': 45, 'UT': 46,
                         'VT': 47, 'VA': 48, 'WA': 49, 'WV': 50, 'WI': 51, 'WY': 52}


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


def get_survey_injection_js(config):
    loyalty_card_number = config['profile']['loyalty_card_number']
    first_name = config['profile']['first_name']
    last_name = config['profile']['last_name']
    address_line1 = config['profile']['address_line1']
    address_line2 = config['profile']['address_line2']
    city = config['profile']['city']
    zip = config['profile']['zip']
    mobile_phone = config['profile']['mobile_phone']
    email_address = config['profile']['email_address']
    state_value = survey_states_mapping[config['profile']['state']]
    age = config['profile']['age']

    js = f"""
        () => {{
            items = document.getElementsByClassName('simpleInput');
            if (items.length == 2) {{
                items[1].checked = true;
            }}
            if (items.length != 0) {{
                for (let i=0; i < items.length; i++) {{
                    item = items[i]
                    item.style.display = "";
                    if (item.value == 4 || item.value == 9) {{
                        item.checked = true;
                    }}
                }}
            }}
            if (items.length == 11) {{
                items[2].checked = true;
            }}
            age = document.getElementById('R002004');
            if (age) {{
                age.value = {age};
            }}
            gender = document.getElementById('R002003');
            if (gender) {{
                gender.value = 9;
            }}
            adults1 = document.getElementById('R002017');
            if (adults1) {{
                adults1.value = 9;
            }}
            adults2 = document.getElementById('R002018');
            if (adults2) {{
                adults2.value = 9;
            }}
            education = document.getElementById('R002005');
            if (education) {{
                education.value = 99;
            }}
            income = document.getElementById('R002006');
            if (income) {{
                income.value = 99;
            }}
            employee = document.getElementById('R003002.2');
            if (employee) {{
                employee.checked = true;
            }}
            sweepstake = document.getElementById('R003003.1');
            if (sweepstake) {{
                sweepstake.checked = true;
            }}
            card = document.getElementById('R003005.1');
            if (card) {{
                card.checked = true;
            }}
            card_number = document.getElementById('R003006');
            if (card_number) {{
                card_number.value = '{loyalty_card_number}';
            }}

            first_name = document.getElementById('S003014');
            if (first_name) {{
                first_name.value = '{first_name}';
            }}
            last_name = document.getElementById('S003015');
            if (last_name) {{
                last_name.value = '{last_name}';
            }}
            address_line1 = document.getElementById('S003016');
            if (address_line1) {{
                address_line1.value = '{address_line1}';
            }}
            address_line2 = document.getElementById('S003017');
            if (address_line2) {{
                address_line2.value = '{address_line2}';
            }}
            city = document.getElementById('S003018');
            if (city) {{
                city.value = '{city}';
            }}
            zip = document.getElementById('S003020');
            if (zip) {{
                zip.value = '{zip}';
            }}
            mobile_phone = document.getElementById('S003021');
            if (mobile_phone) {{
                mobile_phone.value = '{mobile_phone}';
            }}
            email_address = document.getElementById('S003022');
            if (email_address) {{
                email_address.value = '{email_address}';
            }}
            email_address2 = document.getElementById('S003023');
            if (email_address2) {{
                email_address2.value = '{email_address}';
            }}
            state = document.getElementById('S003019');
            if (state) {{
                state.value = '{state_value}';
            }}
            
            return '';
        }}
    """

    return js
