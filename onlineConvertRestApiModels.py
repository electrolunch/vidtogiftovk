from dataclasses import dataclass
from typing import List, Union, Optional
from json import dumps

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Status:
    code:  Optional[str] 
    info:  Optional[str] 

    # @property
    # def __ Optional[dict] __(self):
    #     return as Optional[dict] (self)

    # @property
    # def json(self):
    #     return dumps(self.__ Optional[dict] __)
        
@dataclass_json
@dataclass
class Conversion:
    id:  Optional[str]  =None
    target:  Optional[str]  =None
    category:  Optional[str]   =None
    options:  Optional[dict]   =None
    metadata:  Optional[dict]   =None
    output_target: Optional[List[ str ] ] =None



@dataclass_json
@dataclass
class Input:
    id:  Optional[str]   =None
    type:  Optional[str]   =None
    status:  Optional[str]   =None
    source:  Optional[str]   =None
    engine:  Optional[str]   =None
    options: Optional[List[ str ] ] =None
    filename:  Optional[str]   =None
    size:  Optional[int]   =None
    hash:  Optional[str]   =None
    checksum:  Optional[str]   =None
    content_type:  Optional[str]   =None
    created_at:  Optional[str]   =None
    modified_at:  Optional[str]   =None
    credentials:  Optional[dict]   =None
    parameters:  Optional[dict]   =None
    metadata:  Optional[dict]   =None



@dataclass_json
@dataclass
class Job:
    id:  Optional[str]  =None
    token:  Optional[str]   =None
    type:  Optional[str]   =None
    status: Optional[Status]  =None
    errors: Optional[List[ str ] ]  =None
    warnings: Optional[List[ str ] ] =None
    process: Optional[bool]  =None
    fail_on_input_error: Optional[bool]  =None
    fail_on_conversion_error: Optional[bool]  =None
    conversion: List[Conversion]  =None
    limits: Optional[List[ str ] ] =None
    input: Optional[List[Input]]  =None
    output: Optional[List[ str ] ] =None
    callback:  Optional[str]   =None
    notify_status: Optional[bool]  =None
    server:  Optional[str]   =None
    spent:  Optional[int]   =None
    created_at:  Optional[str]   =None
    modified_at:  Optional[str]   =None



# @dataclass
# class Job:
#     id:  Optional[str] 
#     input:  Optional[dict] 
#     conversion:  Optional[dict] 
#     output:  Optional[dict] 
#     status:  Optional[str] 
#     created_at:  Optional[str] 
#     finished_at:  Optional[str] 
#     error:  Optional[dict] 

    
# from typing import List
# from typing import Any
# from dataclasses import dataclass
# import json
# @dataclass
# class Conversion:
#     id:  Optional[str] 
#     category:  Optional[str] 
#     target:  Optional[str] 
#     options: List[object]

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Conversion':
#         _id =  Optional[str] (obj.get("id"))
#         _category =  Optional[str] (obj.get("category"))
#         _target =  Optional[str] (obj.get("target"))
#         _options = [.from_ Optional[dict] (y) for y in obj.get("options")]
#         return Conversion(_id, _category, _target, _options)

# @dataclass
# class Input:
#     id:  Optional[str] 
#     type:  Optional[str] 
#     source:  Optional[str] 
#     filename:  Optional[str] 
#     size:  Optional[int] 
#     created_at:  Optional[str] 
#     modified_at:  Optional[str] 

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Input':
#         _id =  Optional[str] (obj.get("id"))
#         _type =  Optional[str] (obj.get("type"))
#         _source =  Optional[str] (obj.get("source"))
#         _filename =  Optional[str] (obj.get("filename"))
#         _size =  Optional[int] (obj.get("size"))
#         _created_at =  Optional[str] (obj.get("created_at"))
#         _modified_at =  Optional[str] (obj.get("modified_at"))
#         return Input(_id, _type, _source, _filename, _size, _created_at, _modified_at)

# @dataclass
# class Output:
#     id:  Optional[str] 
#     source: Source
#     uri:  Optional[str] 
#     size:  Optional[int] 
#     created_at:  Optional[str] 
#     status:  Optional[str] 
#     content_type:  Optional[str] 
#     downloads_counter:  Optional[int] 
#     checksum:  Optional[str] 

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Output':
#         _id =  Optional[str] (obj.get("id"))
#         _source = Source.from_ Optional[dict] (obj.get("source"))
#         _uri =  Optional[str] (obj.get("uri"))
#         _size =  Optional[int] (obj.get("size"))
#         _created_at =  Optional[str] (obj.get("created_at"))
#         _status =  Optional[str] (obj.get("status"))
#         _content_type =  Optional[str] (obj.get("content_type"))
#         _downloads_counter =  Optional[int] (obj.get("downloads_counter"))
#         _checksum =  Optional[str] (obj.get("checksum"))
#         return Output(_id, _source, _uri, _size, _created_at, _status, _content_type, _downloads_counter, _checksum)

# @dataclass
# class Root:
#     id:  Optional[str] 
#     token:  Optional[str] 
#     type:  Optional[str] 
#     status: Status
#     process: bool
#     conversion: List[Conversion]
#     input: List[Input]
#     output: List[Output]
#     callback:  Optional[str] 
#     server:  Optional[str] 
#     created_at:  Optional[str] 
#     modified_at:  Optional[str] 

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Root':
#         _id =  Optional[str] (obj.get("id"))
#         _token =  Optional[str] (obj.get("token"))
#         _type =  Optional[str] (obj.get("type"))
#         _status = Status.from_ Optional[dict] (obj.get("status"))
#         _process = 
#         _conversion = [Conversion.from_ Optional[dict] (y) for y in obj.get("conversion")]
#         _input = [Input.from_ Optional[dict] (y) for y in obj.get("input")]
#         _output = [Output.from_ Optional[dict] (y) for y in obj.get("output")]
#         _callback =  Optional[str] (obj.get("callback"))
#         _server =  Optional[str] (obj.get("server"))
#         _created_at =  Optional[str] (obj.get("created_at"))
#         _modified_at =  Optional[str] (obj.get("modified_at"))
#         return Root(_id, _token, _type, _status, _process, _conversion, _input, _output, _callback, _server, _created_at, _modified_at)

# @dataclass
# class Source:
#     conversion:  Optional[str] 
#     input: List[ Optional[str] ]

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Source':
#         _conversion =  Optional[str] (obj.get("conversion"))
#         _input = [.from_ Optional[dict] (y) for y in obj.get("input")]
#         return Source(_conversion, _input)

# @dataclass
# class Status:
#     code:  Optional[str] 
#     info:  Optional[str] 

#     @staticmethod
#     def from_ Optional[dict] (obj: Any) -> 'Status':
#         _code =  Optional[str] (obj.get("code"))
#         _info =  Optional[str] (obj.get("info"))
#         return Status(_code, _info)

# # Example Usage
# # json Optional[str] ing = json.loads(myjson Optional[str] ing)
# # root = Root.from_ Optional[dict] (json Optional[str] ing)
