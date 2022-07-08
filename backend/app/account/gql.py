from .resolvers import login, logout, register, change_password, check_token
import strawberry


@strawberry.type
class AccountQuery:
    check_token = check_token


@strawberry.type
class AccountMutation:
    login = login
    logout = logout
    register = register
    change_password = change_password
