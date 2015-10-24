
from   __future__   import unicode_literals
import re
import json
import httplib
import urllib
from datetime import datetime

import yaml
import pprint; pp = pprint.PrettyPrinter( indent = 4 )




ParseClass = {}

class ParseObject( object ):

    '''
    Class registry: Make it possible to reference any subclass of ParseObject by name
    '''

    @classmethod
    def register( cls, parseName = None ):
        cls.parseName = parseName or cls.__name__
        ParseClass[ cls.parseName ] = cls

    '''
    Parse.com <=> JSON
    '''

    envs = [] # a stack of environments to support push_environment() and pop_environment()

    @staticmethod
    def __set_keys( app_id, api_key ):
        ParseObject.headers = {
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key"  : api_key,
        }
        ParseObject.headers_with_type = {
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key"  : api_key,
            "Content_type"          : 'application/json; charset=UTF-8',        
        }

    @staticmethod
    def set_environment( env ):
        if env == 'development':
            ParseObject.__set_keys( app_id = '2k5RlMXLM9VtUyM9PKsNgGR40RGeNn2dllDxAPxD', api_key = 'wjjHcNP322Zljnr4EOcERmxxhUBSb7YCwqvtKDeS' )
            return
        if True:
            ParseObject.__set_keys( app_id = None,                                       api_key = None )
            return

    @staticmethod
    def set_installation_environment( app_id, master_key ):
        ParseObject.headers["X-Parse-Application-Id"]           = app_id
        ParseObject.headers["X-Parse-Master-Key"]               = master_key
        ParseObject.headers_with_type["X-Parse-Application-Id"] = app_id
        ParseObject.headers_with_type["X-Parse-Master-Key"]     = master_key
        

    @staticmethod
    def push_environment( env ):
        ParseObject.envs.append( env )
        ParseObject.set_environment( env )

    @staticmethod
    def pop_environment():
        assert len( ParseObject.envs ) > 0, 'Attempted to pop from an empty ParseObject environment stack'
        ParseObject.envs.pop()
        ParseObject.set_environment( ParseObject.envs[-1] if len( ParseObject.envs ) > 0 else None )

    @staticmethod
    def http_connection():
        connection = httplib.HTTPSConnection( 'api.parse.com', 443 )
        connection.connect()
        return connection

    @staticmethod
    def http_delete( url ):
        c = ParseObject.http_connection()
        c.request( 'DELETE', url, '', ParseObject.headers )
        return json.loads( c.getresponse().read() )

    @staticmethod
    def http_get( url, params = {} ):
        c = ParseObject.http_connection()
        c.request( 'GET', '{}?{}' .format( url, urllib.urlencode(params) ), '', ParseObject.headers )
        return json.loads( c.getresponse().read() )

    @staticmethod
    def http_post( url, body ):
        c = ParseObject.http_connection()
        c.request( 'POST', url, body, ParseObject.headers_with_type )
        return json.loads( c.getresponse().read() )

    @staticmethod
    def http_put( url, body ):
        c = ParseObject.http_connection()
        c.request( 'PUT', url, body, ParseObject.headers_with_type )
        return json.loads( c.getresponse().read() )

    '''
    JSON <=> attributes
    '''

    def clear_attributes( self ):
        keys = [ key for key in dir(self) if key != 'keys' and key not in dir(type(self)) ]
        for key in keys: delattr( self, key )

    @staticmethod
    def from_attributes( v ):

        # Case 0: Not a structure
        if type( v ) is not dict or '__type' not in v: return v
        if v['__type'] == 'Date'    : return str(v)

        # Case 1: Just a bare pointer
        if v['__type'] == 'Pointer' : return ParsePointer( className = v['className'], objectId = v['objectId'] )

        # Case 2: A relation
        if v['__type'] == 'Relation': return None # TODO

        # Case 3: A full object
        if v['__type'] == 'Object'  :
            o = ParseClass[ v['className'] ] ( objectId = v['objectId'] )
            del v['__type']
            del v['className']
            del v['objectId']
            o.set_attributes( v )
            return o

        # Un-handled type
        assert False, 'Did not know how to deal with __type = {}' .format( v['__type'] )

    def set_attributes( self, j ):
        for k, v in j.items():
            if type( v ) is list:
                setattr( self, k, [ ParseObject.from_attributes(w) for w in v ] )
            else:
                setattr( self, k, ParseObject.from_attributes(v) )

    def get_attributes( self ):
        keys = [ key for key in dir(self) if key != 'keys' and key not in dir(type(self)) ]
        return json.dumps({ key: getattr(self,key) for key in keys })

    def delete_attribute( self, field ):
        return json.dumps({ field: { '__op': 'Delete' } })

    @staticmethod
    def struct_attributes( val ):
        if type(val) in set([ type(None), str, unicode ]): return val
        if type(val) is list: return [    ParseObject.struct_attributes(v) for   v in val         ]
        if type(val) is dict: return { k: ParseObject.struct_attributes(v) for k,v in val.items() }
        return {
            key: ParseObject.struct_attributes( getattr(val,key) )
            for key in dir( val )
            if key != 'keys' and key not in dir(type(val))
        }

    def __str__( self ):
        return yaml.safe_dump(
            { 'ParseObject of type {}'.format(type(self).__name__): ParseObject.struct_attributes( self ) },
            default_flow_style = False
        )

    '''
    CRUD
    '''

    def create( self ):
        assert not hasattr( self, 'objectId' )
        j = self.get_attributes()
        r = ParseObject.http_post( '/1/classes/{}'.format( type(self).__name__ ), j )
        self.set_attributes( r )
        # assert re.search( '^2', r['Status'] ), 'Failed to create object of type {}' .format( type(self).__name__ )

    def read( self, include = None ):
        assert hasattr( self, 'objectId' )
        params = {} if include is None else { 'include': include }
        j = ParseObject.http_get( '/1/classes/{}/{}'.format( type(self).__name__, self.objectId ), params )
        assert 'error' not in j, 'Failed to read {} with ID {}: {}' .format( type(self).__name__, self.objectId, j )
        self.clear_attributes()
        self.set_attributes( j )

    def update( self ):
        assert hasattr( self, 'objectId' )
        j = self.get_attributes()
        r = ParseObject.http_put( '/1/classes/{}/{}'.format( type(self).__name__, self.objectId ), j )
        # assert re.search( '^2', r['Status'] ), 'Failed to update object of type {}' .format( type(self).__name__ )

    def delete( self ):
        assert hasattr( self, 'objectId' )
        j = ParseObject.http_delete( '/1/classes/{}/{}'.format( type(self).__name__, self.objectId ) )

    def delete_field( self, field ):
        assert hasattr( self, 'objectId' )
        delattr( self, field )
        j = self.delete_attribute( field )
        j = ParseObject.http_put( '/1/classes/{}/{}'.format( type(self).__name__, self.objectId ), j )

    '''
    Push notifications
    '''

    @staticmethod
    def push_to_selected_installations( text, installationIds ):
        for installationId in installationIds:
            j = json.dumps({ "where": { "objectId": installationId }, "data": { "alert": text, "sound": "cheering.caf" } })
            ParseObject.http_post( '/1/push', j )

    @staticmethod
    def push_to_selected_users( text, userIds, payload, badges = {} ):
        for userId in userIds:
            data = { "alert": text, "sound": "cheering.caf" } 
            if badges.get( userId, -1 ) > 0: data['badge'] = badges.get( userId, -1 )
            data.update( payload )
            j = json.dumps({ "where": { "userId": userId }, "data": data })
            ParseObject.http_post( '/1/push', j )

    @staticmethod
    def push_to_channels( text, channels ):
        j = json.dumps({ "channels": channels, "data": { "alert": text, "sound": "cheering.caf" } })
        ParseObject.http_post( '/1/push', j )

    # def delete( self ):
    #     assert hasattr( self, 'objectId' )
    #     j = self.get_attributes()
    #     r = ParseObject.http_put( '/1/classes/{}/{}'.format( type(self).__name__, self.objectId ), j )

    '''
    Public methods
    '''

    # Construct object that's empty (if objectId is None) else read from Parse
    def __init__( self, objectId = None, include = None ):
        if objectId is not None:
            self.objectId = objectId
            self.read( include )
        else:
            assert include is None

    # Commit to Parse
    def commit( self ):
        if hasattr(self,'objectId'): self.update()
        else:                        self.create()

    @classmethod
    def query_get( cls, params ):

        return ParseObject.http_get( '/1/classes/{}'.format( cls.__name__ ), params )

    @classmethod
    def query_chunk( cls, include, limit, skip, **where ):

        # Change conditions on ParseObject descendants into conditions on Parse pointers
        where = {
            k: { '__type': "Pointer", 'className': v.__class__.parseName, 'objectId': v.objectId } if isinstance(v,ParseObject) else v
            for k,v in where.items()
        }

        # Get response from server
        params = { 'where': json.dumps(where), 'limit': limit, 'skip': skip, 'order': 'createdAt' }
        if include is not None: params['include'] = include
        j = cls.query_get( params )
        assert 'error' not in j, 'Failed to read array of {} with query {}' .format( cls.__name__, json.dumps(where) )

        # Return results as generator
        for result in j['results']:
            o = object.__new__( cls )
            o.set_attributes( result )
            yield o

    @classmethod
    def query_all( cls, include, limit, skip, **where ):

        while True:
            count = 0
            for count, o in enumerate( cls.query_chunk( include, limit = limit, skip = skip, **where ) ): yield o
            if count == 0: return
            skip += limit

    @classmethod
    def query( cls, include = None, **where ):

        try:
            for o in cls.query_all( include, limit = 100, skip = 0, **where ): yield o
        except:
            print 'Query failed at', datetime.now().isoformat() # TODO: Handle the exception better

    '''
    Tests
    '''

    @staticmethod
    def test_fruit():

        class Fruit( ParseObject ): pass

        # Create
        f0 = Fruit()
        f0.color = 'red'
        f0.commit()

        # Read
        f1 = Fruit( objectId = f0.objectId )
        print f1.color

        # Update
        f1.color = 'yellow'
        f1.commit()

        # Delete color
        f1.delete_field( 'color' )
        f1.commit()

        # Read back
        f2 = Fruit( objectId = f1.objectId )
        assert not hasattr( f2, 'color' )

    @staticmethod
    def test_dump_fruit():

        class Fruit( ParseObject ): pass

        print '-'*80
        for fruit in Fruit.query():
            print fruit.objectId

    @staticmethod
    def test_push():
        
        # Sends push notifications directly to installations
        # ParseObject.push_to_selected_installations( 'TESTING: Push to Installations', ['4lFvOCc3Ij'] )
        
        # Sends push notification to installations given userId
        # ParseObject.push_to_selected_users( 'TESTING: Push to Users', userIds = ['Qb6eS0N0YC'], payload = {} ) # 02MQBNSYIr

        ParseObject.push_to_channels( 'channel test', ['traffic'] )

    @staticmethod
    def test_array():

        class Message( ParseObject ): pass
        Message.register()

        class Task( ParseObject ): pass
        Task.register()

        m0 = Message( objectId = 'FVIAk53cS7', include = 'botmessages,task' )
        print '='*80
        print m0

        for m in Message.query( user = 'MMZo7hZWQ2', include = 'botmessages,task', limit = 2 ).values():
            print '-'*80
            print m

        print '='*80

class ParsePointer( ParseObject ):

    def __init__( self, className, objectId ):
        self.className = className
        self.objectId  = objectId

    def dereference( self, include = None ):
        return ParseClass[ self.className ] ( objectId = self.objectId, include = include )

"""
TEST
"""

if __name__ == '__main__':

    ParseObject.push_environment( 'development' )
    ParseObject.test_fruit()
    ParseObject.test_dump_fruit()