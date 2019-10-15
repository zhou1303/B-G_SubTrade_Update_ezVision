import Constant
import Config_Post_Data


def get_shipment_report(session_requests, csrf, oid):
    # SEND FIRST POST REQUEST
    data_dict = Config_Post_Data.config_shipment_report_by_oid(csrf, oid)

    response = session_requests.post(
        Constant.url_list_shipments,
        data=data_dict
    )

    # SEND FOLLOWING GET REQUESTS

    get_urls = Constant.re_pattern_url_parse.findall(response.text)
    for url in get_urls:
        session_requests.get(Constant.url_tms_root + url)

    # SEND SECOND POST REQUEST
    data_dict['norefresh'] = ''
    data_dict['nSetNumber'] = 1

    response = session_requests.post(
        Constant.url_list_shipments,
        data=data_dict
    )

    return response


def parse_data(html_script, re_pattern):
    data_dict = dict()
    if re_pattern.search(html_script) is not None:
        data_list = re_pattern.findall(html_script)
        data_list = list(map(list, zip(*data_list)))

        for i, value in enumerate(Constant.list_col_name):
            data_dict[value] = (data_list[i])

    return data_dict


def read_login_credentials():
    login_userid = open('username.txt', mode='r')
    login_password = open('password.txt', mode='r')

    Constant.login_userid = login_userid.read()
    Constant.login_password = login_password.read()

    print('User credentials read successfully.')


def read_report_oid():
    report_oid = open('report_oid.txt', mode='r')
    Constant.oid_subtrade_flag_report = report_oid.read()
    print('Report OID read successfully.')
