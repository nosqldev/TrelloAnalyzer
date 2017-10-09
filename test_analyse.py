import nose
from analyse import *


def test_sum_workloads():
    filename = 'check_data\card_list.txt'
    cards_list = utils.read_cardinfo_from_json(filename)
    cards_dict = cardinfo_turn_to_dict(cards_list)
    workloads = sum_workloads(cards_dict, '广告平台测试')
    check_card_list = utils.read_cardinfo_from_json('check_data\check_card_list.txt')

    for i in workloads['member_stat'].keys():
        if None in workloads['member_stat'][i]['new_work_label']:
            workloads['member_stat'][i]['new_work_label']['None'] = workloads['member_stat'][i]['new_work_label'][None]
            del(workloads['member_stat'][i]['new_work_label'][None])

    assert workloads == check_card_list


# if __name__ == '__main__':
#     test_sum_workloads()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:
