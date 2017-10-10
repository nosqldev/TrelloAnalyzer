from analyse import *


def read_cards_dict():
    filename = 'check_data\card_list.txt'
    cards_list = utils.read_cardinfo_from_json(filename)
    cards_dict = cardinfo_turn_to_dict(cards_list)

    for card_id in cards_dict.keys():
        if 'None' in str(cards_dict[card_id]['label_name']):
            cards_dict[card_id]['label_name'] = 'None'

    return cards_dict


def test_build_members_stat():
    cards_dict = read_cards_dict()
    member_stat = build_members_stat('广告平台测试', cards_dict)
    print(member_stat)
    check_member_stat = utils.read_cardinfo_from_json('check_data\check_member_stat.txt')

    assert member_stat == check_member_stat


def test_sum_workloads():
    cards_dict = read_cards_dict()
    workloads = sum_workloads(cards_dict, '广告平台测试')
    check_card_list = utils.read_cardinfo_from_json('check_data\check_card_list.txt')

    assert workloads == check_card_list


# if __name__ == '__main__':
#     test_sum_workloads()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:
