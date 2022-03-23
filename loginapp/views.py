from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# importing other view functions

# importing models.py files.
from loginapp import models as login_models
from profileapp import models as profile_models

# importing security modules.
from django.middleware import csrf
import bcrypt
from loginapp import validation_check
from backend_functions import backend_handling_functions


def homePage(request):
    "home page: a static file."
    if request.POST or len(request.POST) > 0 or len(request.GET) > 0:
        return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/"'/></body>''')
    return render(request, "home_page.html")


def signUpPage(request):
    "asking for signup page"
    if request.POST or len(request.POST) > 0 or len(request.GET) > 0:
        return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/signup/"'/></body>''')

    # Sessions and tokens.
    csrf_token = csrf.get_token(request)

    return render(request, 'signup_page.html', {"csrf_token": csrf_token, "error_signing": False, "user_exist": False})


def signUpPosted(request):
    "action on posted signup page"

    # Security check for method-interchange vaulnerablity: https://blog.nvisium.com/method-interchange-forgotten
    if request.GET or len(request.GET) > 0:
        return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/signup/"'/></body>''')

    # Sessions and Tokens.
    csrf_token = csrf.get_token(request)

    if (not request.POST) or len(request.POST) != 11:
        # Some inputs are missing.
        return HttpResponse('''<body><script>alert("Some required values were missing")</script><meta http-equiv="refresh" content='0; url="/signup/"'/></body>''')

    # Incoming data.
    input_data = request.POST

    """Default values are such that, if the value (for a key) is not in the request.POST (dictionary-like), then
		the validation will not be True. Thus lead to "error_signing".
		This above technique resolve the issue of middleman attack where data is tempered or removed (while sending
		request) by tools like burpsuite."""

    # Stripping and Validating data.
    first_name, last_name = input_data.get("first_name", "").strip(
    ).lower(), input_data.get("last_name", "").strip().lower()
    first_name_check = validation_check.nameCheck(first_name)
    last_name_check = validation_check.nameCheck(last_name)

    user_class, user_section = input_data.get(
        "user_class", "0").strip(), input_data.get("user_section", "NaN").strip()
    user_class_check = validation_check.classCheck(user_class)
    user_section_check = validation_check.sectionCheck(user_section)

    user_contact, r_number = input_data.get(
        "contact_detail", "0").strip(), input_data.get("r_number", "0").strip()
    contact_check = validation_check.contactCheck(user_contact)
    r_number_check = validation_check.rCheck(r_number)

    school_name, user_category = input_data.get("school_name", "").strip(
    ).lower(), input_data.get("user_category", "").strip().upper()
    school_name_check = validation_check.schoolNameCheck(school_name)
    user_category_check = validation_check.categoryCheck(user_category)

    email_address, password = input_data.get(
        "email_address", "").strip().lower(), input_data.get("pswd", "").strip()
    password_check = validation_check.passwordCheck(password)
    email_address_check = validation_check.emailCheck(email_address)

    if not (first_name_check and last_name_check and user_class_check and user_section_check and contact_check and r_number_check and school_name_check and user_category_check and email_address_check and password_check):
        # handling tempered data.
        # The incoming data was corrupted (maybe using burpsuite.) (This is because, all the above validations were done at frontend, but still the value arent valid values.)
        return render(request, 'signup_page.html', {"csrf_token": csrf_token, "error_signing": True, "user_exist": False})

    """----------Now all the input values are valid.---------------"""

    """otp handling to be done"""

    # data formatting.
    first_name = first_name[0].upper() + first_name[1:]
    last_name = last_name[0].upper() + last_name[1:]
    user_section = user_section.upper()
    if len(user_class) != 2:
        user_class = "0" + user_class
    user_category = user_category.upper()

    # backend database working
    class_course_field = backend_handling_functions.auto_assign_course(
        user_class, user_section, user_category)

    """----------password encryption.---------------"""
    # password hashing and salting to be done here.
    # Refer Here: https://security.stackexchange.com/questions/8596/https-security-should-password-be-hashed-server-side-or-client-side

    if len(login_models.USER_SIGNUP_DATABASE.objects.filter(email_address=email_address)) > 0:
        """----------user already exist.---------------"""
        return render(request, 'signup_page.html', {"csrf_token": csrf_token, "error_signing": False, "user_exist": True})

    """----------Now it is confirmed the user is new.---------------"""
    try:

        setting_user = login_models.USER_SIGNUP_DATABASE(first_name=first_name, last_name=last_name, user_class=user_class, user_section=user_section, user_contact=user_contact,
                                                         user_r_number=r_number, school_name=school_name, user_category=user_category, email_address=email_address, password=password, class_course_field=class_course_field)
        setting_user.save()
        setting_profile = profile_models.USER_PROFILE_DATABASE(
            user_signup_db_mapping=setting_user)
        setting_profile.save()

        if setting_user.user_category == "TEACHER":
            backend_handling_functions.course_instructor_assigning(
                setting_user)
    except:
        """----------Some error while setting user.---------------"""
        return render(request, 'signup_page.html', {"csrf_token": csrf_token, "error_signing": True, "user_exist": False})

    """----------User Succesfully Created.---------------"""
    return render(request, 'signup_success.html')


def signupOTPVerfied(request):

    return render(request, 'signup_success.html')


def contactPage(request):
    # Sessions and tokens.
    csrf_token = csrf.get_token(request)
    return render(request, 'contact_page.html', {"csrf_token": csrf_token, "query_submitted": False, "upload_error": False})


def contactPageSubmitted(request):
    # Sessions and tokens.
    csrf_token = csrf.get_token(request)

    if request.GET:
        return render(request, 'contact_page.html', {"csrf_token": csrf_token, "query_submitted": False, "upload_error": True})

    input_data = request.POST

    # need to change, as we are not using url anymore but we are using name.
    query_email_address = input_data.get("query_email", "").strip().lower()
    query_email_check = validation_check.emailCheck(query_email_address)

    query_url = input_data.get("query_url", None).strip()

    query_description = input_data.get("query_description", "").strip()
    # As it acts similar to a school name.
    query_content_check = validation_check.schoolNameCheck(query_description)

    if not (query_email_check and query_content_check):
        # handling tempered data.
        return render(request, 'contact_page.html', {"csrf_token": csrf_token, "query_submitted": False, "upload_error": True})

    try:
        setting_query = login_models.QueryStore(
            query_email_address=query_email_address, query_url=query_url, query_description=query_description)
        setting_query.save()
    except:
        return render(request, 'contact_page.html', {"csrf_token": csrf_token, "query_submitted": False, "upload_error": True})

    return render(request, 'contact_page.html', {"csrf_token": csrf_token, "query_submitted": True, "upload_error": False})


def loginPage(request):
    # Sessions and tokens.
    csrf_token = csrf.get_token(request)

    return render(request, "login_page.html", {"csrf_token": csrf_token, "error_login": False, "user_not_exist": False, "invalid_password": False})


def loginPageCheck(request):
    if request.GET and len(request.GET) > 0:
        return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

    # Sessions and tokens.
    csrf_token = csrf.get_token(request)

    if len(request.POST) == 3 and request.POST.get("entered_email", False) and request.POST.get("entered_password", False):
        Authentication = False

        input_data = request.POST
        enter_user_name = input_data.get("entered_email", False)
        enter_user_name_check = validation_check.emailCheck(enter_user_name)

        enter_password = input_data.get("entered_password", False)
        enter_password_check = validation_check.passwordCheck(enter_password)

        if not(enter_user_name_check and enter_password_check):
            # hadling tempered data.

            return render(request, "login_page.html", {"csrf_token": csrf_token, "error_login": True, "user_not_exist": False, "invalid_password": False})

        if len(login_models.USER_SIGNUP_DATABASE.objects.filter(email_address=enter_user_name)) == 0:
            # User does not exist.

            return render(request, "login_page.html", {"csrf_token": csrf_token, "error_login": False, "user_not_exist": True, "invalid_password": False})

        """----------password encryption.---------------"""
        # password hashing and salting to be done here.

        extracted_user = login_models.USER_SIGNUP_DATABASE.objects.filter(
            email_address=enter_user_name)[0]

        if extracted_user.password == enter_password:
            Authentication = True

        if Authentication:
            # FOr the login we directly send the page. however in case of other time (when section is active.) we will use session id and use the profileApp's viewfunctions.
            request.session['user_id'] = extracted_user.id
            return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/profile/"'/></body>''')
        else:
            return render(request, "login_page.html", {"csrf_token": csrf_token, "error_login": False, "user_not_exist": False, "invalid_password": True})
    return render(request, "login_page.html", {"csrf_token": csrf_token, "error_login": True, "user_not_exist": False, "invalid_password": False})
