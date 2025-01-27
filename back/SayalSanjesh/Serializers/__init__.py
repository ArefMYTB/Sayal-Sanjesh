wrong_token_result = {
    "farsi_message": "توکن نامعتبر است.",
    "english_message": "Wrong Token."
}

status_success_result = {
    "farsi_message": "با موفقیت انجام شد.",
    "english_message": "Successfully Done."
}

wrong_data_result = {
    "farsi_message": "",
    "english_message": "",
    "code": 409
}


def wrong_result(fields):
    for filed in fields:

        if type(fields[filed][0]) != fields[filed][1]:
            wrong_data_result["farsi_message"] = f"صحیح نیست {filed} نوع داده وارد شده برای"
            wrong_data_result["english_message"] = f"wrong datatype for {filed}"
            return False, wrong_data_result
        elif fields[filed][0] == None:
            wrong_data_result["farsi_message"] = f"وارد کنید {filed} لطفا مقدار را برای"
            wrong_data_result["english_message"] = f"please enter value for  {filed}"
            return False, wrong_data_result
