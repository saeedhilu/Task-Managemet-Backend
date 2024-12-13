import json

from urllib.parse import parse_qs



from channels.middleware import BaseMiddleware

from channels.exceptions import DenyConnection

from channels.db import database_sync_to_async


from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth import get_user_model


from django.conf import settings



USER = get_user_model()



class BaseJWTAuthMiddleWare(BaseMiddleware):
    
    controller_ws_paths = ['auth']
    
    async def __call__(self, scope, receive, send):
        
        """
        ASGI application; can insert things into the scope and run asynchronous
        code.
        """

        print("JWT")      
        
    
        
        # Copy scope to stop changes going upstream
        scope = dict(scope)
        
        
        
        query_params = self.processed_query_params(scope['query_string'])
        
    
        auth_response = await self.authenticate(query_params)
        
        error         = auth_response.get('error')
        
        
        if error is not None:
            
            await self.send_errors(error,send)
            
            return 
        
        
        user = auth_response['user']
        
        scope['user'] = user    
        
            
        return  await self.inner(scope,receive,send)
    
    
    
    
    async def authenticate(self,query_params):
        
        token      = query_params.get('token')
        
        exceptions = {}
        
        
        if token is None:
        
            exceptions['code']   = 4001
            exceptions['reason'] = 'Token Missing in Query String'
            
            return {
                'error':exceptions
            }

        else :
            
            user_id = await self.get_user_id_from_token(token)
            
            if user_id is not None :
                
                
                user = await self.get_user(user_id)
                
                
                if user is None:
                    
                    exceptions['code'] = 4004 
                    exceptions['reason'] = 'User Not Found '
                    
                    
                    return {
                        'error':exceptions,
                        
                    }
                                
                    
                
                
                    
                
                
                return {
                    'user':user
                }    
                    
                
            else:           
                

                exceptions['code'] = 4001
                exceptions['reason'] = 'Token Expired'
                
                
                return {
                    'error':exceptions,
                }
            
            
    
    
    async def send_errors(self,error_data,send):
        
        print(error_data)

        await send({
                    'type': 'websocket.accept'
        })
        
        await send({
            'type': 'websocket.send',
            'text': json.dumps(error_data)
        })
        await send({
            'type': 'websocket.close',
            'code': error_data['code']
        })
    
    
    
    
    
    
    @database_sync_to_async
    def get_user(self,user_id) -> None or USER:     # type: ignore
        try:
            
            user = USER.objects.get(id=user_id)
            
            return user
        except USER.DoesNotExist : 
            
            return None

    
    
    @database_sync_to_async
    def get_user_id_from_token(self, token):
            print("sdfdjfjdf")
            try:
                access_token = AccessToken(token)
                return access_token['user_id']
            except:
                return None
    
    
    
    
    
    @staticmethod
    def processed_query_params(bytstring_param) :
        
        decoded_string = bytstring_param.decode('utf-8')

        #  Parse the query string into a dictionary
        # parse_qs returns a dictionary where the values are lists, use {k: v[0]} to get single values
        parsed_dict = {k: v[0] for k, v in parse_qs(decoded_string).items()}
        
        return parsed_dict






class PathAuthMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        # Make sure to pass the arguments to the BaseMiddleware constructor
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send):
        path = scope['path'].split('/')[1]  # Extract the first path segment
        print(f"Path: {path}")

        if path in BaseJWTAuthMiddleWare.controller_ws_paths:
            print(f"Applying JWT Auth Middleware for {path}")
            auth_controller_app = BaseJWTAuthMiddleWare(self.inner)
            return await auth_controller_app(scope, receive, send)

        # If not the specified path, fallback to regular middleware chain
        else:
            return await super().__call__(scope, receive, send)    
    