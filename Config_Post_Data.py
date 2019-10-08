import Constant


def config_shipment_report_by_oid(csrf, oid):
    data_dict = Constant.post_data_open_report.copy()
    data_dict['_csrf'] = csrf
    data_dict['reportoid'] = oid

    return data_dict


def config_add_ref_by_select(csrf, obj_menu_value, ref_menu_value, ref_value):
    data_dict = Constant.post_data_add_ref.copy()
    data_dict['_csrf'] = csrf
    data_dict['sidOwner'] = obj_menu_value
    data_dict['sReference1'] = ref_value
    data_dict['sidReferenceType1'] = ref_menu_value
    return data_dict

