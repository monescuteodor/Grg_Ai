# gRPC and Protocol Buffers Complete Reference


---

# CHAPTER 1: gRPC FUNDAMENTALS


## Remarks

gRPC is a high-performance RPC framework by Google. Instead of REST (JSON over HTTP), gRPC uses Protocol Buffers (binary serialization) over HTTP/2. It's 2-10x faster than REST for service-to-service communication. Used by Google, Netflix, Slack, Dropbox, and most microservice architectures at scale.


## Protocol Buffers (Protobuf)

```protobuf
// user.proto — schema definition
syntax = "proto3";

package userservice;

// Message = data structure (like a struct/class)
message User {
    int32 id = 1;          // Field number (not value!)
    string name = 2;
    string email = 3;
    int32 age = 4;
    Role role = 5;
    repeated string tags = 6;  // Array
    Address address = 7;       // Nested message
}

enum Role {
    USER = 0;
    ADMIN = 1;
    MODERATOR = 2;
}

message Address {
    string city = 1;
    string country = 2;
    string zip = 3;
}

// Service definition (API)
service UserService {
    // Unary: one request → one response (like REST)
    rpc GetUser(GetUserRequest) returns (User);
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    
    // Server streaming: one request → stream of responses
    rpc WatchUsers(WatchRequest) returns (stream UserEvent);
    
    // Client streaming: stream of requests → one response
    rpc UploadUsers(stream User) returns (UploadResponse);
    
    // Bidirectional streaming: stream ↔ stream
    rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message GetUserRequest { int32 id = 1; }
message CreateUserRequest { string name = 1; string email = 2; }
message ListUsersRequest { int32 page = 1; int32 per_page = 2; }
message ListUsersResponse { repeated User users = 1; int32 total = 2; }
message UserEvent { string type = 1; User user = 2; }
message WatchRequest {}
message UploadResponse { int32 count = 1; }
message ChatMessage { string user = 1; string text = 2; }
```


## Python gRPC Server

```python
# server.py
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def GetUser(self, request, context):
        user = self.users.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User {request.id} not found')
            return user_pb2.User()
        return user
    
    def CreateUser(self, request, context):
        user = user_pb2.User(
            id=self.next_id,
            name=request.name,
            email=request.email,
        )
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def ListUsers(self, request, context):
        all_users = list(self.users.values())
        start = (request.page - 1) * request.per_page
        end = start + request.per_page
        return user_pb2.ListUsersResponse(
            users=all_users[start:end],
            total=len(all_users),
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```


## Python gRPC Client

```python
# client.py
import grpc
import user_pb2
import user_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

# Create user
user = stub.CreateUser(user_pb2.CreateUserRequest(
    name="Alice",
    email="alice@example.com",
))
print(f"Created: {user.id} {user.name}")

# Get user
user = stub.GetUser(user_pb2.GetUserRequest(id=1))
print(f"Got: {user.name} ({user.email})")

# List users
response = stub.ListUsers(user_pb2.ListUsersRequest(page=1, per_page=10))
for u in response.users:
    print(f"  {u.id}: {u.name}")
```


## gRPC vs REST

```
Feature          REST                  gRPC
─────────────────────────────────────────────────────
Format           JSON (text)           Protobuf (binary)
Protocol         HTTP/1.1 or 2         HTTP/2 only
Speed            1x                    2-10x faster
Schema           OpenAPI (optional)    .proto (required)
Streaming        SSE or WebSocket      Built-in (4 types)
Code generation  Optional (Swagger)    Built-in (protoc)
Browser          Native                Needs grpc-web proxy
Type safety      Runtime               Compile-time

WHEN TO USE gRPC:
  ✅ Service-to-service (microservices)
  ✅ High throughput / low latency
  ✅ Streaming data
  ✅ Polyglot (Python, Go, Java, Rust all generated from same .proto)

WHEN TO USE REST:
  ✅ Public APIs (browser-friendly)
  ✅ Simple CRUD
  ✅ Third-party integrations
  ✅ Debugging (JSON is human-readable)
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Not versioning protobuf fields
  Renaming field number → breaks all clients.
  Fix: never reuse field numbers. Mark old fields as reserved.

PITFALL 2: Large messages
  Sending 100MB protobuf → timeout, memory issues.
  Fix: use streaming for large data. Default max message size is 4MB.

PITFALL 3: No error handling
  gRPC errors are different from HTTP errors.
  Fix: use proper gRPC status codes (NOT_FOUND, INVALID_ARGUMENT, etc.)

PITFALL 4: Blocking calls in async context
  Synchronous gRPC stub in async server → blocks event loop.
  Fix: use grpc.aio for async Python gRPC.

PITFALL 5: No deadlines/timeouts
  Client waits forever for slow server.
  Fix: always set deadline: stub.GetUser(request, timeout=5.0)
```