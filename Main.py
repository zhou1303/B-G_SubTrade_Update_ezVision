import Constant
import Get_Data
import Post_Data
import Assign_SubTrade_Flag
import time
import G_API


if __name__ == '__main__':

    #START COUNTING RUNNING TIME
    start = time.time()

    count = 0

    #LOGIN TMS
    Get_Data.read_login_credentials()
    session_requests, csrf = Post_Data.login_tms()

    print('Now adding subtrade flags...')
    print('Check shipment report B&G SubTrade Flag Update for missing required information if the program doesn\'t '
          'complete within 5 minutes.')

    while True:

        #GET SHIPMENT REPORT OBJECT
        response = Get_Data.get_shipment_report(session_requests, csrf, Constant.oid_subtrade_flag_report)

        #PARSE HTML SCRIPT
        html_script = response.text

        #GET SHIPMENT DATA
        data_dict = Get_Data.parse_data(html_script, Constant.re_pattern_all_cols)

        # CHECK IF THERE IS ANY SHIPMENT LEFT
        if len(data_dict) == 0:
            break

        #ASSIGN SUBTRADE FLAG
        data_dict = Assign_SubTrade_Flag.assign_flag(data_dict)
        menu_values = data_dict['menu_value']

        #ADD SUBTRADE FLAG

        for i, subtrade_flag in enumerate(data_dict['subtrade_flag']):
            response = Post_Data.add_ref(session_requests, csrf, menu_values[i],
                                         Constant.menu_value_ref_type_subtrade, subtrade_flag)
            count += 1

    print('SubTrade flag is added to ', count, ' number of shipments.')

    #END TIME
    end = time.time()

    #UPDATE LOG REPORT ON GOOGLE SHEETS
    duration = end - start
    workbook_log = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_log)
    worksheet_log = G_API.get_worksheet_by_id(workbook_log, Constant.g_sheets_worksheet_id_log)
    Post_Data.log_event(worksheet_log, duration)

    time.sleep(30)

# save_file = open(Constant.root_path + 'test.html', 'w+')
# save_file.write(html_script)
# save_file.close()