import Constant


def is_subtrade_af(dest_code):
    if '1010' in dest_code:
        return True
    return False


def is_subtrade_at(origin_code):
    if '1010' in origin_code:
        return True
    return False


def is_subtrade_ff(origin_code, dest_code):
    if origin_code in Constant.subtrade_ff_origin_code \
            and dest_code in Constant.subtrade_ff_dest_code:
        return True
    return False


def is_subtrade_ft(origin_code, dest_code):
    if origin_code in Constant.subtrade_ft_origin_code \
            and dest_code not in Constant.subtrade_ft_dest_code:
        return True
    return False


def is_subtrade_f(origin_code, dest_code):
    if origin_code not in Constant.subtrade_f_origin_code \
            and dest_code in Constant.subtrade_f_dest_code:
        return True
    return False


def is_subtrade_t(origin_code, dest_code):
    if origin_code not in Constant.subtrade_t_origin_code \
            and dest_code not in Constant.subtrade_t_dest_code:
        return True
    return False


def assign_flag(data_dict):
    origin_codes = data_dict['origin_code']
    dest_codes = data_dict['dest_code']

    subtrade_flags = list()

    for i, origin_code in enumerate(origin_codes):
        if is_subtrade_af(dest_codes[i]):
            subtrade_flags.append('AF')
        elif is_subtrade_at(origin_code):
            subtrade_flags.append('AT')
        elif is_subtrade_f(origin_code, dest_codes[i]):
            subtrade_flags.append('F')
        elif is_subtrade_ff(origin_code, dest_codes[i]):
            subtrade_flags.append('FF')
        elif is_subtrade_ft(origin_code, dest_codes[i]):
            subtrade_flags.append('FT')
        elif is_subtrade_t(origin_code, dest_codes[i]):
            subtrade_flags.append('T')

    data_dict['subtrade_flag'] = subtrade_flags
    return data_dict

