from fastapi import Depends, HTTPException, status

from src.database.models import User
from src.services.auth import token_service
from src.messages import *


class Role:
    async def is_admin(self, user):
        if user.role in ADMIN_PERMISSIONS:
            return True
        
    async def is_moder(self, user):
        if user.role in MODERATOR_PERMISSIONS:
            return True
        
        
role_service = Role()