def overviewOffers(log):
    total_offers_made = log[log['concept:name'] == 'O_Created']
    print("Total amount of made offers:", len(total_offers_made))
    offer_counts = log[log['concept:name'] == 'O_Created'].groupby('case:concept:name').size()

    more_than_one_offer = offer_counts[offer_counts > 1].index.tolist()
    print("More than 1 offer:", len(more_than_one_offer))

    for i in range(0, 11):
        var_name = f"offer_{i}"
        locals()[var_name]= offer_counts[offer_counts == i].index.tolist()
        print(f'{var_name}: {len(locals()[var_name])}')

    more_offers = offer_counts[offer_counts > 10].index.tolist()
    print("More than 10 offers:", len(more_offers))


def analysis(log):
    overviewOffers(log)