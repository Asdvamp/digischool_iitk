import datetime

NAME_LIMIT = 40
USER_CLASS = {"class_length": [1, 2], "class_range":[1, 12], "section_length": 1, "values":["A", "B", "C","D","E", "F"]}
USER_CONTACT = {"contact_length": [10, 11]}
R_NUMBER = {"number_length": [6, 10]}
SCHOOL_NAME = 100
USER_CATEGORY = {"length_limit": 10, "values": ["STUDENT","TEACHER"]}
PASSWORD_LENGTH = {"length_range":[8, 25]} # 25 need to be replaced with the output length of cryptographic technique used.

QUERY_URL_LIMIT = 100
QUERY_DESCRIPTION_LENGTH = 500

PROFILE_PIC_PATH_LENGTH = 200
DEFAULT_PROFILE_PHOTO = 'Templates/default_profile_photo.jpg'


OFFERING_YEAR = datetime.date.today().year

CLS_COURSE_MAPPING_UNIQUE_ID_LENGTH = 7
COURSE_ID_LENGTH = 10 # format, "sc-cl-cs-ofyr" subject_code:class:section:offeringyear
COURSE_NAME_LENGTH = 100
COURSE_ID_ARRAY_MAX_LENGTH = 100

LECTURE_TITLE_LENGTH = 100
LECTURE_UNIQUE_ID = COURSE_ID_LENGTH + 2

TEST_TITLE_LENGTH = 100
TEST_INSTRUCTION_LENGTH = 100
FILES_ALLOWED = 10
FILES_STRING_MAX_LENGTH = FILES_ALLOWED * 25