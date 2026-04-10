BASE_URL = "https://stellarburgers.education-services.ru/api"

REGISTER = "/auth/register"
LOGIN = "/auth/login"
ORDERS = "/orders"
INGREDIENTS = "/ingredients"
USER_DELETE = "/auth/user"

HTTP_OK = 200 # фактически API возвращает 200 при успешном создании, хотя логичнее было бы 201. Оставляем 200 для соответствия реальному поведению API, чтобы была возможность использовать его для проверки успешного создания.
HTTP_CREATED = 201 
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_INTERNAL_ERROR = 500

ERR_USER_EXISTS = "User already exists"
ERR_REQUIRED_FIELDS = "Email, password and name are required fields"
ERR_LOGIN_FAILED = "email or password are incorrect"
ERR_NO_INGREDIENTS = "Ingredient ids must be provided"
