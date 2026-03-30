import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_id from URL route
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json.get('message', '')
            mandob_id = text_data_json.get('mandob_id')
            admin_id = text_data_json.get('admin_id')

            if text_data_json.get('type') == 'get_history':
                # Send message history
                await self.send_room_history(self.room_id)
                return

            if not message_text:
                await self.send(text_data=json.dumps({
                    'error': 'Message cannot be empty'
                }, ensure_ascii=False))
                return

            # Get or create room and save message
            result = await self.get_or_create_room_and_message(
                self.room_id, mandob_id, admin_id, message_text
            )

            if not result or not result['success']:
                await self.send(text_data=json.dumps({
                    'error': result['error'] if result else 'Failed to create/get room'
                }, ensure_ascii=False))
                return

            room_data = result['room']
            message_data = result['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': message_data
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Server error: {str(e)}'
            }, ensure_ascii=False))

    async def chat_message(self, event):
        # Send message to WebSocket with proper Unicode handling
        await self.send(text_data=json.dumps(event['data'], ensure_ascii=False))

    @database_sync_to_async
    def get_or_create_room_and_message(self, room_id, mandob_id, admin_id, message_text):
        """Get or create room and save message - runs in sync context"""
        try:
            from mandob.models import Mandob ,Room, Message

            room = None

            # Try to get existing room by room_id
            try:
                room_id_int = int(room_id)
                room = Room.objects.get(room_id=room_id_int, is_active=True)
            except (ValueError, Room.DoesNotExist):
                # Room doesn't exist, create new one
                # Only mandob can create a new room
                if not mandob_id:
                    return {
                        'success': False,
                        'error': 'Only mandob can create new room'
                    }

                try:
                    from mandob.models import Mandob
                    mandob = Mandob.objects.get(id=mandob_id)
                    room = Room.objects.create(room=mandob)
                except Mandob.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }

            # Validate sender exists
            sender_obj = None
            if mandob_id:
                try:
                    from mandob.models import Mandob
                    sender_obj = Mandob.objects.get(id=mandob_id)
                except Mandob.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }
            elif admin_id:
                try:
                    from core.models import Admin  # Adjust import path as needed
                    sender_obj = Admin.objects.get(id=admin_id)
                except Exception:
                    return {
                        'success': False,
                        'error': 'Admin not found'
                    }

            # Create message
            message_obj = Message.objects.create(
                room=room,
                message=message_text,
                mandob_id=mandob_id if mandob_id else None,
                admin_id=admin_id if admin_id else None
            )

            # Prepare response data
            message_data = {
                'message': message_text,
                'room_id': str(room.id),
                'timestamp': message_obj.created.isoformat(),
                'message_id': message_obj.id,
            }

            # Add sender info
            if message_obj.mandob:
                message_data['sender'] = {
                    'type': 'mandob',
                    'id': message_obj.mandob.id,
                    'name': getattr(message_obj.mandob, 'name', f'Mandob {message_obj.mandob.id}')
                }
            elif message_obj.admin:
                message_data['sender'] = {
                    'type': 'admin',
                    'id': message_obj.admin.id,
                    'name': getattr(message_obj.admin, 'name', f'Admin {message_obj.admin.id}')
                }

            return {
                'success': True,
                'room': {'id': room.id},
                'message': message_data
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    @database_sync_to_async
    def get_room_messages(self, room_id, limit=50):
        """Get recent messages for the room - runs in sync context"""
        try:
            from mandob.models import Room, Message

            room = Room.objects.get(room_id=room_id, is_active=True)
            messages = Message.objects.filter(
                room=room,
                is_active=True
            ).select_related('mandob', 'admin').order_by('-created')[:limit]

            message_list = []
            for msg in reversed(messages):
                message_data = {
                    'message': msg.message,
                    'room_id': str(room.id),
                    'timestamp': msg.created.isoformat(),
                    'message_id': msg.id,
                }

                if msg.mandob:
                    message_data['sender'] = {
                        'type': 'mandob',
                        'id': msg.mandob.id,
                        'name': getattr(msg.mandob, 'name', f'Mandob {msg.mandob.id}')
                    }
                elif msg.admin:
                    message_data['sender'] = {
                        'type': 'admin',
                        'id': msg.admin.id,
                        'name': getattr(msg.admin, 'name', f'Admin {msg.admin.id}')
                    }

                message_list.append(message_data)

            return message_list
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    async def send_room_history(self, room_id):
        """Send recent messages to newly connected client"""
        messages = await self.get_room_messages(room_id)
        if messages:
            await self.send(text_data=json.dumps({
                'type': 'message_history',
                'messages': messages
            }, ensure_ascii=False))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications_admin'

        # Join notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            # Handle create notification request
            if message_type == 'create_notification':
                title = text_data_json.get('title')
                text = text_data_json.get('text', '')

                if title:
                    # Save to database
                    notification = await self.save_notification(title, text)

                    if notification:
                        # Prepare notification data
                        notification_data = {
                            'id': notification['id'],
                            'title': notification['title'],
                            'text': notification['text'],
                            'created': notification['created']
                        }

                        # Send to all admins in the group
                        await self.channel_layer.group_send(
                            self.group_name,
                            {
                                'type': 'notification_message',
                                'data': notification_data
                            }
                        )

                        # Send success response to sender
                        await self.send(text_data=json.dumps({
                            'type': 'notification_created',
                            'status': 'success',
                            'notification': notification_data
                        }, ensure_ascii=False))
                    else:
                        await self.send(text_data=json.dumps({
                            'type': 'error',
                            'message': 'Failed to create notification'
                        }, ensure_ascii=False))
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Title is required'
                    }, ensure_ascii=False))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Server error: {str(e)}'
            }, ensure_ascii=False))

    # Receive notification from group
    async def notification_message(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        }, ensure_ascii=False))

    @database_sync_to_async
    def save_notification(self, title, text):
        """Save notification to database"""
        try:
            from core.models import Notification  # Adjust import path as needed

            notification = Notification.objects.create(
                user_type='admin',
                title=title,
                text=text
            )

            return {
                'id': notification.id,
                'title': notification.title,
                'text': notification.text,
                'created': notification.created.isoformat() if hasattr(notification, 'created') else None
            }
        except Exception as e:
            print(f"Error saving notification: {e}")
            return None



class CaptainChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_id from URL route
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json.get('message', '')
            captain_id = text_data_json.get('captain_id')
            admin_id = text_data_json.get('admin_id')

            if text_data_json.get('type') == 'get_history':
                # Send message history
                await self.send_room_history(self.room_id)
                return

            if not message_text:
                await self.send(text_data=json.dumps({
                    'error': 'Message cannot be empty'
                }, ensure_ascii=False))
                return

            # Get or create room and save message
            result = await self.get_or_create_room_and_message(
                self.room_id, captain_id, admin_id, message_text
            )

            if not result or not result['success']:
                await self.send(text_data=json.dumps({
                    'error': result['error'] if result else 'Failed to create/get room'
                }, ensure_ascii=False))
                return

            room_data = result['room']
            message_data = result['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': message_data
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Server error: {str(e)}'
            }, ensure_ascii=False))

    async def chat_message(self, event):
        # Send message to WebSocket with proper Unicode handling
        await self.send(text_data=json.dumps(event['data'], ensure_ascii=False))

    @database_sync_to_async
    def get_or_create_room_and_message(self, room_id, captain_id, admin_id, message_text):
        """Get or create room and save message - runs in sync context"""
        try:
            from captain.models import Captain ,CaptainRoom, CaptainMessage

            room = None

            # Try to get existing room by room_id
            try:
                room_id_int = int(room_id)
                room = CaptainRoom.objects.get(room_id=room_id_int, is_active=True)
            except (ValueError, CaptainRoom.DoesNotExist):
                # Room doesn't exist, create new one
                # Only mandob can create a new room
                if not captain_id:
                    return {
                        'success': False,
                        'error': 'Only mandob can create new room'
                    }

                try:
                    from captain.models import Captain
                    captain = Captain.objects.get(id=captain_id)
                    room = CaptainRoom.objects.create(room=captain)
                except Captain.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }

            # Validate sender exists
            sender_obj = None
            if captain_id:
                try:
                    from captain.models import Captain
                    sender_obj = Captain.objects.get(id=captain_id)
                except Captain.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }
            elif admin_id:
                try:
                    from core.models import Admin  # Adjust import path as needed
                    sender_obj = Admin.objects.get(id=admin_id)
                except Exception:
                    return {
                        'success': False,
                        'error': 'Admin not found'
                    }

            # Create message
            message_obj = CaptainMessage.objects.create(
                room=room,
                message=message_text,
                captain_id=captain_id if captain_id else None,
                admin_id=admin_id if admin_id else None
            )

            # Prepare response data
            message_data = {
                'message': message_text,
                'room_id': str(room.id),
                'timestamp': message_obj.created.isoformat(),
                'message_id': message_obj.id,
            }

            # Add sender info
            if message_obj.captain:
                message_data['sender'] = {
                    'type': 'captain',
                    'id': message_obj.captain.id,
                    'name': getattr(message_obj.captain, 'name', f'captain {message_obj.captain.id}')
                }
            elif message_obj.admin:
                message_data['sender'] = {
                    'type': 'admin',
                    'id': message_obj.admin.id,
                    'name': getattr(message_obj.admin, 'name', f'Admin {message_obj.admin.id}')
                }

            return {
                'success': True,
                'room': {'id': room.id},
                'message': message_data
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    @database_sync_to_async
    def get_room_messages(self, room_id, limit=50):
        """Get recent messages for the room - runs in sync context"""
        try:
            from captain.models import CaptainRoom, CaptainMessage

            room = CaptainRoom.objects.get(room_id=room_id, is_active=True)
            messages = CaptainMessage.objects.filter(
                room=room,
                is_active=True
            ).select_related('captain', 'admin').order_by('-created')[:limit]

            message_list = []
            for msg in reversed(messages):
                message_data = {
                    'message': msg.message,
                    'room_id': str(room.id),
                    'timestamp': msg.created.isoformat(),
                    'message_id': msg.id,
                }

                if msg.captain:
                    message_data['sender'] = {
                        'type': 'captain',
                        'id': msg.captain.id,
                        'name': getattr(msg.mandob, 'name', f'captain {msg.captain.id}')
                    }
                elif msg.admin:
                    message_data['sender'] = {
                        'type': 'admin',
                        'id': msg.admin.id,
                        'name': getattr(msg.admin, 'name', f'Admin {msg.admin.id}')
                    }

                message_list.append(message_data)

            return message_list
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    async def send_room_history(self, room_id):
        """Send recent messages to newly connected client"""
        messages = await self.get_room_messages(room_id)
        if messages:
            await self.send(text_data=json.dumps({
                'type': 'message_history',
                'messages': messages
            }, ensure_ascii=False))


class UserChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_id from URL route
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json.get('message', '')
            user_id = text_data_json.get('user_id')
            admin_id = text_data_json.get('admin_id')

            if text_data_json.get('type') == 'get_history':
                # Send message history
                await self.send_room_history(self.room_id)
                return

            if not message_text:
                await self.send(text_data=json.dumps({
                    'error': 'Message cannot be empty'
                }, ensure_ascii=False))
                return

            # Get or create room and save message
            result = await self.get_or_create_room_and_message(
                self.room_id, user_id, admin_id, message_text
            )

            if not result or not result['success']:
                await self.send(text_data=json.dumps({
                    'error': result['error'] if result else 'Failed to create/get room'
                }, ensure_ascii=False))
                return

            room_data = result['room']
            message_data = result['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': message_data
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Server error: {str(e)}'
            }, ensure_ascii=False))

    async def chat_message(self, event):
        # Send message to WebSocket with proper Unicode handling
        await self.send(text_data=json.dumps(event['data'], ensure_ascii=False))

    @database_sync_to_async
    def get_or_create_room_and_message(self, room_id, user_id, admin_id, message_text):
        """Get or create room and save message - runs in sync context"""
        try:
            from user.models import User ,UserRoom, UserMessage

            room = None

            # Try to get existing room by room_id
            try:
                room_id_int = int(room_id)
                room = UserRoom.objects.get(room_id=room_id_int, is_active=True)
            except (ValueError, UserRoom.DoesNotExist):
                # Room doesn't exist, create new one
                # Only mandob can create a new room
                if not user_id:
                    return {
                        'success': False,
                        'error': 'Only mandob can create new room'
                    }

                try:
                    from user.models import User
                    user = User.objects.get(id=user_id)
                    room = UserRoom.objects.create(room=user)
                except User.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }

            # Validate sender exists
            sender_obj = None
            if user_id:
                try:
                    from user.models import User
                    sender_obj = User.objects.get(id=user_id)
                except sender_obj.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'Mandob not found'
                    }
            elif admin_id:
                try:
                    from core.models import Admin  # Adjust import path as needed
                    sender_obj = Admin.objects.get(id=admin_id)
                except Exception:
                    return {
                        'success': False,
                        'error': 'Admin not found'
                    }

            # Create message
            message_obj = UserMessage.objects.create(
                room=room,
                message=message_text,
                user_id=user_id if user_id else None,
                admin_id=admin_id if admin_id else None
            )

            # Prepare response data
            message_data = {
                'message': message_text,
                'room_id': str(room.id),
                'timestamp': message_obj.created.isoformat(),
                'message_id': message_obj.id,
            }

            # Add sender info
            if message_obj.user:
                message_data['sender'] = {
                    'type': 'user',
                    'id': message_obj.user.id,
                    'name': getattr(message_obj.user, 'name', f'user {message_obj.user.id}')
                }
            elif message_obj.admin:
                message_data['sender'] = {
                    'type': 'admin',
                    'id': message_obj.admin.id,
                    'name': getattr(message_obj.admin, 'name', f'Admin {message_obj.admin.id}')
                }

            return {
                'success': True,
                'room': {'id': room.id},
                'message': message_data
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Database error: {str(e)}'
            }

    @database_sync_to_async
    def get_room_messages(self, room_id, limit=50):
        """Get recent messages for the room - runs in sync context"""
        try:
            from user.models import UserRoom, UserMessage

            room = UserRoom.objects.get(room_id=room_id, is_active=True)
            messages = UserRoom.objects.filter(
                room=room,
                is_active=True
            ).select_related('user', 'admin').order_by('-created')[:limit]

            message_list = []
            for msg in reversed(messages):
                message_data = {
                    'message': msg.message,
                    'room_id': str(room.id),
                    'timestamp': msg.created.isoformat(),
                    'message_id': msg.id,
                }

                if msg.user:
                    message_data['sender'] = {
                        'type': 'user',
                        'id': msg.user.id,
                        'name': getattr(msg.mandob, 'name', f'user {msg.user.id}')
                    }
                elif msg.admin:
                    message_data['sender'] = {
                        'type': 'admin',
                        'id': msg.admin.id,
                        'name': getattr(msg.admin, 'name', f'Admin {msg.admin.id}')
                    }

                message_list.append(message_data)

            return message_list
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    async def send_room_history(self, room_id):
        """Send recent messages to newly connected client"""
        messages = await self.get_room_messages(room_id)
        if messages:
            await self.send(text_data=json.dumps({
                'type': 'message_history',
                'messages': messages
            }, ensure_ascii=False))