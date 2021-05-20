from fastapi import HTTPException

from services.external import get_external_request
from core.config import AUTH_IP


class Permissions:
    READ = []
    WRITE = ['Writer']
    SUPER = ['Super']


def role_has_permissions(role_id: int, permissions: list):
    data, status = get_external_request(AUTH_IP + f'/api/permissions/roles/{role_id}/')
    if status != 200:
        raise HTTPException(status_code=status, detail=data if 'detail' not in data else data['detail'])
    role_groups = [group['name'] for group in data['groups']]
    missing_groups = set(permissions) - set(role_groups)
    return missing_groups == []


def user_has_permissions(user: dict, permissions: list):
    if not user or not role_has_permissions(user['role_id'], permissions):
        raise HTTPException(status_code=403, detail='You have no permissions to perform the operation')
    return True
