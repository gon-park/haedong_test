def increase_the_number_of_digits(max_array, cur_array):
    cur_array[-1] += 1
    for i in range(len(cur_array) - 1, -1, -1):
        if cur_array[i] > max_array[i]:
            if i == 0:
                return False
            cur_array[i] = 0
            cur_array[i - 1] += 1
        else:
            break
    return True


def calc_divide_count(start, end, interval):
    ''' [10, 40, 5] 일 경우 6을 return 해주는 코드, [0, 0, 0]이면 1이아니라 0을 리턴한다.
        테스트 stv의 max_array를 만들기 위해 사용 됨 '''
    if start == end: return 0
    if interval == 0: return 0
    return int((end - start) / interval)


def get_divide_value(sei_list, index):
    ''' start, end, interval list = sei_list '''
    return sei_list[0] + (sei_list[2] * index)


def set_strategy_var(max_array, cur_array, params):
    if type(params[0]) is list:
        for var in params:
            set_strategy_var(max_array, cur_array, var)

    else:
        max_array.append(calc_divide_count(params[0], params[1], params[2]))
        cur_array.append(0)


def get_strategy_var(cur_array, idx, params):
    sum = 0
    if type(params[0]) is list:
        res = []
        for i in range(0, len(params)):
            cnt, value = get_strategy_var(cur_array, idx, params[i])
            idx = idx + cnt
            sum = sum + cnt
            res.append(value)

        return sum, res

    else:
        return 1, get_divide_value(params, cur_array[idx])