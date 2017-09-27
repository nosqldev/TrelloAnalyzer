import nose
from burndowndata import *


def test_glob_file_name():
    iteration_snapshot_filename, daily_file_names = glob_file_name('广告平台测试')

    assert iteration_snapshot_filename == 'data\iteration-snapshot-广告平台测试-2017-09-17.txt'
    assert daily_file_names == ['data\daily-广告平台测试-2017-09-18.txt', 'data\daily-广告平台测试-2017-09-19.txt', 'data\daily-广告平台测试-2017-09-20.txt']

    return iteration_snapshot_filename, daily_file_names


def test_do_compute_cards_stat():
    iteration_snapshot_filename, daily_file_names = test_glob_file_name()
    iteration_card_info = utils.read_cardinfo_from_json(iteration_snapshot_filename)
    daily_card_list = batch_read_cardinfo_from_json(daily_file_names)
    daily_stat = compute_daily_stat(iteration_card_info, daily_card_list, daily_file_names)
    check_daily_stat = utils.read_cardinfo_from_json('check_data\check.txt')

    assert daily_stat == check_daily_stat


if __name__ == '__main__':
    nose.run()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:
