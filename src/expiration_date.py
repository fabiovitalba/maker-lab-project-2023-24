from datetime import date, timedelta

from const import ADD_DAY, ADD_WEEK, ADD_MONTH, CONFIRM, REM_DAY, REM_WEEK, REM_MONTH

def handle_exp_date_input(input_str: str, exp_date: date):
    next_input = False
    if (CONFIRM in input_str):
        new_exp_date = exp_date
        next_input = True
    elif (ADD_DAY in input_str):
        new_exp_date = exp_date + timedelta(days=1)
    elif (ADD_WEEK in input_str):
        new_exp_date = exp_date + timedelta(weeks=1)
    elif (ADD_MONTH in input_str):
        new_exp_date = exp_date + timedelta(days=30)
    elif (REM_DAY in input_str):
        new_exp_date = exp_date + timedelta(days=-1)
    elif (REM_WEEK in input_str):
        new_exp_date = exp_date + timedelta(weeks=-1)
    elif (REM_MONTH in input_str):
        new_exp_date = exp_date + timedelta(days=-30)
    else:
        new_exp_date = exp_date
    return [new_exp_date, next_input]
