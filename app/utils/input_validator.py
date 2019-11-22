
import re


# The common advice about email validation is don't:
# send a confirmation code to the email given and look
# if the email sender return an error
def valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if(re.search(regex, email)):
        return True, None

    return False, "Invalid email"


def valid_password(password):

    valid_long = len(password) >= 8 & len(password) <= 30
    contain_number = bool(re.search('[0-9]', password))
    contain_capital_letter = bool(re.search('[A-Z]', password))

    print(valid_long, contain_number, contain_capital_letter)
    if not (valid_long & contain_number & contain_capital_letter):
        return False, "Your password must contain at least one lowercase letter, one capital letter and one number, 8-30 characters long"

    return True, None


def validate_input(inputs):
    for input_type, value in inputs.items():
        if input_type == "email":
            is_valid_email, error = valid_email(value)

            if not is_valid_email:
                return is_valid_email, error

        if input_type == "password":
            is_valid_password, error = valid_password(value)

            if not is_valid_password:
                return is_valid_password, error

    return True, None
