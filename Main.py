import Constant
import Get_Data
import Post_Data
import Assign_SubTrade_Flag
import time
import G_API

if __name__ == '__main__':

    # -----------------------------------------------------------------------------------------------------------------
    # Start to count execution time and number of shipments in the process.
    start = time.time()
    count = 0
    # -----------------------------------------------------------------------------------------------------------------
    # Collect report OID, login username and password from .txt files.
    Get_Data.read_report_oid()
    Get_Data.read_login_credentials()
    # -----------------------------------------------------------------------------------------------------------------
    # Use username and password combinations to log into TMS and extract login token from HTML response.
    session_requests, csrf = Post_Data.login_tms()

    print('Now adding subtrade flags...')
    print('Check shipment report B&G SubTrade Flag Update for missing required information if the program doesn\'t '
          'complete within 5 minutes.')

    # -----------------------------------------------------------------------------------------------------------------
    # Create an infinite loop to run through each page of the report until no shipment is found.
    while True:

        # -------------------------------------------------------------------------------------------------------------
        # Request the first page of the report in HTML format. Extract the response in text format.
        html_script = Get_Data.get_shipment_report(session_requests, csrf, Constant.oid_subtrade_flag_report).text
        # -------------------------------------------------------------------------------------------------------------
        # Parse response, save each data column into a single list object with a dict object to include them all.
        data_dict = Get_Data.parse_data(html_script, Constant.re_pattern_all_cols)
        # -------------------------------------------------------------------------------------------------------------
        # Check if there is any object left on the report.
        if len(data_dict) == 0:
            break
        # -------------------------------------------------------------------------------------------------------------
        # Assign subtrade flag value based on values in data columns, add them as a list object into the dict object.
        data_dict = Assign_SubTrade_Flag.assign_flag(data_dict)
        # -------------------------------------------------------------------------------------------------------------
        # Extract the special 'menu value' list for POST request URL concatenation.
        menu_values = data_dict['menu_value']
        # -------------------------------------------------------------------------------------------------------------
        # Begin to push Ref: SubTrade update to each shipment.
        for i, subtrade_flag in enumerate(data_dict['subtrade_flag']):
            Post_Data.add_ref(session_requests, csrf, menu_values[i],
                              Constant.menu_value_ref_type_subtrade, subtrade_flag)
            count += 1

    print('SubTrade flag is added to ', count, ' number of shipments.')
    # -----------------------------------------------------------------------------------------------------------------
    # Record the end time of this execution.
    end = time.time()
    # -----------------------------------------------------------------------------------------------------------------
    # Create a log and upload it to Google Sheets.
    duration = end - start
    workbook_log = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_log)
    worksheet_log = G_API.get_worksheet_by_id(workbook_log, Constant.g_sheets_worksheet_id_log)
    Post_Data.log_event(worksheet_log, duration)
    # -----------------------------------------------------------------------------------------------------------------
    # Hold the system from closing in 30 seconds.
    time.sleep(30)

# save_file = open(Constant.root_path + 'test.html', 'w+')
# save_file.write(html_script)
# save_file.close()
