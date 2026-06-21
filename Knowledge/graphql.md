# GraphQL Complete Reference


---

# CHAPTER 1: GRAPHQL FUNDAMENTALS


## Remarks

GraphQL is a query language for APIs developed by Facebook in 2012 (open-sourced 2015). Instead of multiple REST endpoints returning fixed shapes, GraphQL has ONE endpoint where the client specifies exactly what data it needs. This solves REST's over-fetching (getting fields you don't need) and under-fetching (needing multiple requests for related data).

Key concepts: **Schema** (type system defining all available data), **Queries** (read data), **Mutations** (write data), **Subscriptions** (real-time updates), **Resolvers** (functions that fetch data), **Type system** (strongly typed), **Introspection** (API is self-documenting).

Used by: GitHub, Shopify, Twitter, Airbnb, PayPal, Yelp, The New York Times. React apps with Apollo Client or urql are the most common consumer pattern.

Tools: **Apollo Server/Client** (most popular), **urql** (lighter client), **Relay** (Facebook's client), **GraphQL Yoga** (server), **Pothos/TypeGraphQL** (code-first schema), **GraphiQL/Apollo Studio** (playground/explorer).


## GraphQL vs REST

```
REST:
  GET  /users/123              → { id, name, email, age, address, ... }
  GET  /users/123/posts        → [{ id, title, body, ... }, ...]
  GET  /users/123/posts/1/comments → [{ ... }]
  
  Problems:
    Over-fetching:  GET /users/123 returns 20 fields, you need 2
    Under-fetching: Need user + posts + comments = 3 requests
    Versioning:     /v1/users vs /v2/users for different shapes

GraphQL:
  POST /graphql
  
  query {
    user(id: 123) {
      name
      email
      posts(limit: 5) {
        title
        comments {
          text
          author { name }
        }
      }
    }
  }
  
  Benefits:
    Exact data:     Client asks for exactly what it needs
    One request:    User + posts + comments in single query
    No versioning:  Add fields without breaking clients
    Self-documenting: Schema IS the documentation
    Strongly typed: Validation built-in

WHEN TO USE GRAPHQL:
  ✅ Multiple clients (web, mobile, TV) needing different data shapes
  ✅ Complex nested data (social graphs, e-commerce catalogs)
  ✅ Rapidly evolving frontend
  ✅ Mobile apps (bandwidth matters — fetch only what you need)

WHEN TO USE REST:
  ✅ Simple CRUD APIs
  ✅ File uploads/downloads
  ✅ Public APIs (REST more widely understood)
  ✅ Caching-heavy APIs (HTTP caching works better with REST)
  ✅ Server-to-server communication (simpler)
```


## Schema Definition Language (SDL)

```graphql
# Scalar types (built-in)
# String, Int, Float, Boolean, ID

# Custom scalar
scalar DateTime
scalar JSON

# Enum
enum Role {
  ADMIN
  MODERATOR
  USER
  GUEST
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

# Object type
type User {
  id: ID!                    # ! = non-null (required)
  name: String!
  email: String!
  age: Int
  role: Role!
  avatar: String
  createdAt: DateTime!
  posts: [Post!]!            # Non-null list of non-null posts
  followers: [User!]!
  followerCount: Int!
}

type Post {
  id: ID!
  title: String!
  body: String!
  status: PostStatus!
  author: User!
  comments: [Comment!]!
  tags: [String!]!
  publishedAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Comment {
  id: ID!
  text: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

# Input type (for mutations — separate from output types)
input CreatePostInput {
  title: String!
  body: String!
  tags: [String!]
  status: PostStatus = DRAFT    # Default value
}

input UpdatePostInput {
  title: String
  body: String
  tags: [String!]
  status: PostStatus
}

# Pagination types
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

# Interface (shared fields)
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post implements Node & Timestamped {
  id: ID!
  title: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Union (one of several types)
union SearchResult = User | Post | Comment

type SearchResponse {
  results: [SearchResult!]!
  totalCount: Int!
}

# Root types
type Query {
  # Users
  user(id: ID!): User
  users(limit: Int = 20, after: String): UserConnection!
  me: User

  # Posts
  post(id: ID!): Post
  posts(
    limit: Int = 20
    after: String
    status: PostStatus
    authorId: ID
  ): PostConnection!

  # Search
  search(query: String!, limit: Int = 10): SearchResponse!
}

type Mutation {
  # Auth
  login(email: String!, password: String!): AuthPayload!
  register(input: RegisterInput!): AuthPayload!

  # Posts
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
  publishPost(id: ID!): Post!

  # Comments
  addComment(postId: ID!, text: String!): Comment!
  deleteComment(id: ID!): Boolean!

  # Social
  followUser(userId: ID!): User!
  unfollowUser(userId: ID!): User!
}

type Subscription {
  postPublished: Post!
  commentAdded(postId: ID!): Comment!
  userStatusChanged(userId: ID!): User!
}

type AuthPayload {
  token: String!
  user: User!
}

input RegisterInput {
  name: String!
  email: String!
  password: String!
}
```


---

# CHAPTER 2: QUERIES AND MUTATIONS


## Query Examples

```graphql
# Simple query
query GetUser {
  user(id: "123") {
    name
    email
    role
  }
}

# Response:
{
  "data": {
    "user": {
      "name": "Alice",
      "email": "alice@example.com",
      "role": "ADMIN"
    }
  }
}


# Nested query (one request, multiple levels)
query GetUserWithPosts {
  user(id: "123") {
    name
    posts(limit: 5) {
      title
      status
      comments {
        text
        author {
          name
        }
      }
    }
  }
}


# Query with variables (parameterized, reusable)
query GetUser($userId: ID!) {
  user(id: $userId) {
    name
    email
    posts(limit: 10) {
      title
    }
  }
}
# Variables (sent separately):
{
  "userId": "123"
}


# Multiple queries in one request
query Dashboard {
  me {
    name
    role
  }
  recentPosts: posts(limit: 5, status: PUBLISHED) {
    edges {
      node {
        title
        publishedAt
      }
    }
  }
  userCount: users {
    totalCount
  }
}


# Fragments (reusable field selections)
fragment UserBasic on User {
  id
  name
  email
  avatar
}

fragment PostPreview on Post {
  id
  title
  status
  publishedAt
  author {
    ...UserBasic
  }
}

query Feed {
  posts(limit: 20, status: PUBLISHED) {
    edges {
      node {
        ...PostPreview
        comments {
          text
          author {
            ...UserBasic
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}


# Aliases (same field, different arguments)
query CompareUsers {
  alice: user(id: "1") {
    name
    followerCount
  }
  bob: user(id: "2") {
    name
    followerCount
  }
}


# Directives (@include, @skip)
query GetUser($userId: ID!, $withPosts: Boolean!) {
  user(id: $userId) {
    name
    email
    posts @include(if: $withPosts) {
      title
    }
  }
}
# Variables: { "userId": "123", "withPosts": true }


# Inline fragments (for union/interface types)
query Search($query: String!) {
  search(query: $query) {
    results {
      ... on User {
        name
        email
      }
      ... on Post {
        title
        body
      }
      ... on Comment {
        text
      }
    }
  }
}
```


## Mutation Examples

```graphql
# Create
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    status
    createdAt
  }
}
# Variables:
{
  "input": {
    "title": "GraphQL is awesome",
    "body": "Here's why...",
    "tags": ["graphql", "api"]
  }
}


# Update
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    status
    updatedAt
  }
}
# Variables:
{
  "id": "456",
  "input": {
    "title": "Updated title",
    "status": "PUBLISHED"
  }
}


# Delete
mutation DeletePost($id: ID!) {
  deletePost(id: $id)
}


# Authentication
mutation Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    token
    user {
      id
      name
      role
    }
  }
}


# Multiple mutations (executed sequentially)
mutation SetupProfile {
  updateProfile: updateUser(input: { bio: "Developer" }) {
    id
    bio
  }
  followAlice: followUser(userId: "alice-123") {
    id
    name
  }
  createFirstPost: createPost(input: { title: "Hello World", body: "My first post" }) {
    id
    title
  }
}
```


---

# CHAPTER 3: SERVER IMPLEMENTATION


## Apollo Server (Node.js)

```typescript
// npm install @apollo/server graphql

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

// Type definitions (schema)
const typeDefs = `#graphql
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    body: String!
    author: User!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
    post(id: ID!): Post
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, body: String!, authorId: ID!): Post!
  }
`;

// Resolvers (how to fetch data)
const resolvers = {
    Query: {
        users: async (_, __, { dataSources }) => {
            return dataSources.userAPI.getAll();
        },

        user: async (_, { id }, { dataSources }) => {
            return dataSources.userAPI.getById(id);
        },

        posts: async (_, __, { dataSources }) => {
            return dataSources.postAPI.getAll();
        },

        post: async (_, { id }, { dataSources }) => {
            return dataSources.postAPI.getById(id);
        },
    },

    Mutation: {
        createUser: async (_, { name, email }, { dataSources }) => {
            return dataSources.userAPI.create({ name, email });
        },

        createPost: async (_, { title, body, authorId }, { dataSources }) => {
            return dataSources.postAPI.create({ title, body, authorId });
        },
    },

    // Field resolvers (resolve relationships)
    User: {
        posts: async (parent, _, { dataSources }) => {
            // parent = the User object
            return dataSources.postAPI.getByAuthor(parent.id);
        },
    },

    Post: {
        author: async (parent, _, { dataSources }) => {
            return dataSources.userAPI.getById(parent.authorId);
        },
    },
};


// Data sources
class UserAPI {
    constructor(private db: Database) {}

    async getAll() {
        return this.db.query('SELECT * FROM users');
    }

    async getById(id: string) {
        return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    }

    async create(data: { name: string; email: string }) {
        return this.db.query(
            'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
            [data.name, data.email]
        );
    }
}


// Start server
const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
    context: async ({ req }) => {
        // Auth context
        const token = req.headers.authorization?.replace('Bearer ', '');
        const user = token ? await verifyToken(token) : null;

        return {
            user,
            dataSources: {
                userAPI: new UserAPI(db),
                postAPI: new PostAPI(db),
            },
        };
    },
});

console.log(`Server ready at ${url}`);
```


## Authentication and Authorization

```typescript
// Context — extract user from token
const server = new ApolloServer({
    typeDefs,
    resolvers,
    plugins: [
        {
            async requestDidStart() {
                return {
                    async didResolveOperation(requestContext) {
                        // Log queries (optional)
                        console.log(requestContext.request.query);
                    },
                };
            },
        },
    ],
});

// Auth directive / middleware
function requireAuth(resolver) {
    return (parent, args, context, info) => {
        if (!context.user) {
            throw new GraphQLError('Not authenticated', {
                extensions: { code: 'UNAUTHENTICATED' },
            });
        }
        return resolver(parent, args, context, info);
    };
}

function requireRole(role: string) {
    return (resolver) => {
        return (parent, args, context, info) => {
            if (!context.user) {
                throw new GraphQLError('Not authenticated', {
                    extensions: { code: 'UNAUTHENTICATED' },
                });
            }
            if (context.user.role !== role) {
                throw new GraphQLError('Not authorized', {
                    extensions: { code: 'FORBIDDEN' },
                });
            }
            return resolver(parent, args, context, info);
        };
    };
}

// Usage in resolvers
const resolvers = {
    Query: {
        me: requireAuth((_, __, { user, dataSources }) => {
            return dataSources.userAPI.getById(user.id);
        }),

        users: requireRole('ADMIN')((_, __, { dataSources }) => {
            return dataSources.userAPI.getAll();
        }),
    },

    Mutation: {
        deletePost: requireAuth(async (_, { id }, { user, dataSources }) => {
            const post = await dataSources.postAPI.getById(id);
            if (post.authorId !== user.id && user.role !== 'ADMIN') {
                throw new GraphQLError('Not authorized to delete this post');
            }
            return dataSources.postAPI.delete(id);
        }),
    },
};
```


## Error Handling

```typescript
import { GraphQLError } from 'graphql';

// Throwing errors in resolvers
const resolvers = {
    Query: {
        user: async (_, { id }, { dataSources }) => {
            const user = await dataSources.userAPI.getById(id);

            if (!user) {
                throw new GraphQLError(`User with id ${id} not found`, {
                    extensions: {
                        code: 'USER_NOT_FOUND',
                        argumentName: 'id',
                    },
                });
            }

            return user;
        },
    },

    Mutation: {
        createUser: async (_, { input }, { dataSources }) => {
            // Validation
            if (!input.email.includes('@')) {
                throw new GraphQLError('Invalid email address', {
                    extensions: {
                        code: 'VALIDATION_ERROR',
                        field: 'email',
                    },
                });
            }

            try {
                return await dataSources.userAPI.create(input);
            } catch (err) {
                if (err.code === '23505') {   // Unique constraint
                    throw new GraphQLError('Email already registered', {
                        extensions: { code: 'DUPLICATE_EMAIL' },
                    });
                }
                throw err;
            }
        },
    },
};

// Error response format:
// {
//   "data": null,
//   "errors": [
//     {
//       "message": "User with id 999 not found",
//       "locations": [{ "line": 2, "column": 3 }],
//       "path": ["user"],
//       "extensions": {
//         "code": "USER_NOT_FOUND",
//         "argumentName": "id"
//       }
//     }
//   ]
// }

// Format errors (hide internal details in production)
const server = new ApolloServer({
    typeDefs,
    resolvers,
    formatError: (formattedError, error) => {
        // Don't expose internal errors
        if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
            return {
                message: 'An unexpected error occurred',
                extensions: { code: 'INTERNAL_SERVER_ERROR' },
            };
        }
        return formattedError;
    },
});
```


---

# CHAPTER 4: CLIENT IMPLEMENTATION


## Apollo Client (React)

```typescript
// npm install @apollo/client graphql

import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery, useMutation } from '@apollo/client';

// Setup client
const client = new ApolloClient({
    uri: 'https://api.example.com/graphql',
    cache: new InMemoryCache(),
    headers: {
        authorization: `Bearer ${getToken()}`,
    },
});

// Wrap app
function App() {
    return (
        <ApolloProvider client={client}>
            <Router />
        </ApolloProvider>
    );
}


// Define queries
const GET_USERS = gql`
    query GetUsers($limit: Int) {
        users(limit: $limit) {
            edges {
                node {
                    id
                    name
                    email
                    avatar
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
`;

const GET_USER = gql`
    query GetUser($id: ID!) {
        user(id: $id) {
            id
            name
            email
            role
            posts {
                id
                title
                status
            }
        }
    }
`;

const CREATE_POST = gql`
    mutation CreatePost($input: CreatePostInput!) {
        createPost(input: $input) {
            id
            title
            status
        }
    }
`;


// useQuery hook
function UserList() {
    const { loading, error, data, fetchMore } = useQuery(GET_USERS, {
        variables: { limit: 20 },
    });

    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;

    const { edges, pageInfo } = data.users;

    return (
        <div>
            {edges.map(({ node: user }) => (
                <UserCard key={user.id} user={user} />
            ))}

            {pageInfo.hasNextPage && (
                <button
                    onClick={() =>
                        fetchMore({
                            variables: { after: pageInfo.endCursor },
                        })
                    }
                >
                    Load More
                </button>
            )}
        </div>
    );
}


// useMutation hook
function CreatePostForm() {
    const [createPost, { loading, error }] = useMutation(CREATE_POST, {
        // Update cache after mutation
        update(cache, { data: { createPost: newPost } }) {
            cache.modify({
                fields: {
                    posts(existingPosts = { edges: [] }) {
                        const newEdge = {
                            __typename: 'PostEdge',
                            node: newPost,
                            cursor: newPost.id,
                        };
                        return {
                            ...existingPosts,
                            edges: [newEdge, ...existingPosts.edges],
                        };
                    },
                },
            });
        },
        // Optimistic response (instant UI update)
        optimisticResponse: {
            createPost: {
                __typename: 'Post',
                id: 'temp-id',
                title: formData.title,
                status: 'DRAFT',
            },
        },
    });

    const handleSubmit = async (formData) => {
        try {
            await createPost({
                variables: { input: formData },
            });
        } catch (err) {
            console.error('Failed to create post:', err);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {error && <ErrorBanner error={error} />}
            <input name="title" required />
            <textarea name="body" required />
            <button type="submit" disabled={loading}>
                {loading ? 'Creating...' : 'Create Post'}
            </button>
        </form>
    );
}


// Polling and refetching
function LiveFeed() {
    const { data, refetch } = useQuery(GET_POSTS, {
        pollInterval: 30000,    // Refetch every 30 seconds
    });

    return (
        <div>
            <button onClick={() => refetch()}>Refresh</button>
            {/* render posts */}
        </div>
    );
}
```


## Subscriptions (Real-time)

```typescript
// Server: subscription resolver
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
    Mutation: {
        createComment: async (_, { postId, text }, { user, dataSources }) => {
            const comment = await dataSources.commentAPI.create({
                postId,
                text,
                authorId: user.id,
            });

            // Publish event
            pubsub.publish(`COMMENT_ADDED_${postId}`, {
                commentAdded: comment,
            });

            return comment;
        },
    },

    Subscription: {
        commentAdded: {
            subscribe: (_, { postId }) => {
                return pubsub.asyncIterator(`COMMENT_ADDED_${postId}`);
            },
        },
    },
};


// Client: useSubscription
import { useSubscription, gql } from '@apollo/client';

const COMMENT_SUBSCRIPTION = gql`
    subscription OnCommentAdded($postId: ID!) {
        commentAdded(postId: $postId) {
            id
            text
            author {
                name
            }
            createdAt
        }
    }
`;

function PostComments({ postId }) {
    const { data: queryData } = useQuery(GET_COMMENTS, {
        variables: { postId },
    });

    // Real-time new comments
    useSubscription(COMMENT_SUBSCRIPTION, {
        variables: { postId },
        onData: ({ data }) => {
            // New comment received — Apollo cache auto-updates
            console.log('New comment:', data.data.commentAdded);
        },
    });

    return (
        <div>
            {queryData?.comments.map(comment => (
                <Comment key={comment.id} comment={comment} />
            ))}
        </div>
    );
}
```


---

# CHAPTER 5: PERFORMANCE AND SECURITY


## N+1 Problem and DataLoader

```
THE N+1 PROBLEM:

  query {
    posts(limit: 20) {      ← 1 query: SELECT * FROM posts LIMIT 20
      title
      author {               ← 20 queries: SELECT * FROM users WHERE id = ?
        name                    (one per post!)
      }
    }
  }

  Total: 1 + 20 = 21 queries! Very slow.

SOLUTION: DataLoader (batching + caching)
```

```typescript
// npm install dataloader
import DataLoader from 'dataloader';

// Create loader (batches individual loads into one query)
function createUserLoader(db: Database) {
    return new DataLoader<string, User>(async (userIds) => {
        // ONE query for ALL requested users
        const users = await db.query(
            'SELECT * FROM users WHERE id = ANY($1)',
            [userIds]
        );

        // Return in same order as requested IDs
        const userMap = new Map(users.map(u => [u.id, u]));
        return userIds.map(id => userMap.get(id) || null);
    });
}

// Create per-request (important! each request gets fresh loader)
const server = new ApolloServer({ typeDefs, resolvers });

// In context
context: async ({ req }) => ({
    loaders: {
        user: createUserLoader(db),
        post: createPostLoader(db),
    },
}),

// In resolver
const resolvers = {
    Post: {
        author: (parent, _, { loaders }) => {
            return loaders.user.load(parent.authorId);
            // DataLoader batches: if 20 posts resolve author,
            // only ONE SQL query runs with all 20 IDs
        },
    },
};

// Result: 1 + 1 = 2 queries instead of 1 + 20!
```


## Query Complexity and Depth Limiting

```typescript
// Prevent malicious queries
// npm install graphql-depth-limit graphql-query-complexity

import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
    typeDefs,
    resolvers,
    validationRules: [
        depthLimit(10),   // Max 10 levels deep
        createComplexityLimitRule(1000, {
            // Each field costs 1, lists cost more
            scalarCost: 1,
            objectCost: 2,
            listFactor: 10,
        }),
    ],
});

// BAD query (attacker could send):
// query {
//   user(id: 1) {
//     posts {
//       author {
//         posts {
//           author {
//             posts {        ← Depth 7, recursion attack!
//               author { ... }
//             }
//           }
//         }
//       }
//     }
//   }
// }
// → Blocked by depth limit

// Rate limiting per query complexity
// Simple query (cost 5):   user { name email }
// Complex query (cost 500): users { posts { comments { author { posts { ... } } } } }
// Rate limit based on total cost, not just request count
```


## Caching Strategies

```typescript
// Apollo Client cache is automatic and powerful

// Cache policies
const client = new ApolloClient({
    cache: new InMemoryCache({
        typePolicies: {
            Query: {
                fields: {
                    // Merge paginated results
                    posts: {
                        keyArgs: ['status'],   // Different cache per status
                        merge(existing = { edges: [] }, incoming) {
                            return {
                                ...incoming,
                                edges: [...existing.edges, ...incoming.edges],
                            };
                        },
                    },
                },
            },
            User: {
                // Cache by 'id' field (default)
                keyFields: ['id'],
            },
            Post: {
                keyFields: ['id'],
                fields: {
                    // Computed field
                    isPublished: {
                        read(_, { readField }) {
                            return readField('status') === 'PUBLISHED';
                        },
                    },
                },
            },
        },
    }),
});

// Fetch policies
useQuery(GET_USER, {
    fetchPolicy: 'cache-first',        // Default: use cache, fetch if missing
    // 'cache-and-network':            // Show cache, refetch in background
    // 'network-only':                 // Always fetch, update cache
    // 'cache-only':                   // Only cache, never fetch
    // 'no-cache':                     // Fetch, don't cache
});

// Server-side caching (CDN, Redis)
// Add cache hints in resolvers
const resolvers = {
    Query: {
        posts: (_, __, ___, info) => {
            info.cacheControl.setCacheHint({ maxAge: 300 });   // 5 min
            return dataSources.postAPI.getAll();
        },
    },
    Post: {
        author: (parent, _, __, info) => {
            info.cacheControl.setCacheHint({ maxAge: 3600 });  // 1 hour
        },
    },
};
```


---

# CHAPTER 6: BEST PRACTICES AND PITFALLS


## Schema Design Best Practices

```graphql
# 1. Use Input types for mutations (not inline args)
# BAD:
type Mutation {
  createUser(name: String!, email: String!, age: Int, role: Role): User!
}

# GOOD:
input CreateUserInput {
  name: String!
  email: String!
  age: Int
  role: Role
}
type Mutation {
  createUser(input: CreateUserInput!): User!
}


# 2. Return the created/updated object (not just ID or boolean)
# BAD:
type Mutation {
  updateUser(id: ID!, input: UpdateUserInput!): Boolean!
}

# GOOD:
type Mutation {
  updateUser(id: ID!, input: UpdateUserInput!): User!
}


# 3. Use Relay-style pagination for lists
# BAD:
type Query {
  posts: [Post!]!
}

# GOOD:
type Query {
  posts(first: Int, after: String): PostConnection!
}


# 4. Mutation responses with user errors
type CreatePostPayload {
  post: Post              # null if errors
  errors: [UserError!]!   # empty if success
}

type UserError {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}


# 5. Use enums for fixed sets
# BAD:
type Post {
  status: String!   # Could be anything
}

# GOOD:
enum PostStatus { DRAFT, PUBLISHED, ARCHIVED }
type Post {
  status: PostStatus!
}


# 6. Nullable vs Non-null
# Use ! (non-null) by default
# Make nullable only when field might genuinely be absent
type User {
  id: ID!           # Always exists
  name: String!     # Always exists
  email: String!    # Always exists
  bio: String       # Nullable: user might not have set bio
  avatar: String    # Nullable: might not have uploaded
}
```


## Common Pitfalls

```
PITFALL 1: N+1 queries
  Every nested field triggers separate DB query.
  Fix: DataLoader for batching and caching.

PITFALL 2: No depth/complexity limits
  Attacker sends deeply nested query → server OOM.
  Fix: graphql-depth-limit + query complexity analysis.

PITFALL 3: Exposing internal errors
  Stack traces visible to client.
  Fix: formatError in server config, log internally.

PITFALL 4: No authentication/authorization
  All data accessible to everyone.
  Fix: Auth in context, permission checks in resolvers.

PITFALL 5: Over-fetching in resolvers
  Resolver fetches ALL fields from DB even if client asks for 2.
  Fix: Use info parameter to check requested fields, or use DataLoader.

PITFALL 6: Giant schema in one file
  Unmaintainable 5000-line schema.
  Fix: Split by domain (user.graphql, post.graphql), merge at startup.

PITFALL 7: Using GraphQL for file uploads
  GraphQL is for structured data, not binary.
  Fix: Use REST endpoint for uploads, return URL via GraphQL.

PITFALL 8: No rate limiting
  Complex query costs 100x more than simple one, both count as "1 request".
  Fix: Rate limit by query complexity, not just request count.

PITFALL 9: Returning arrays instead of connections
  Can't paginate, can't add metadata.
  Fix: Use Relay-style connections (edges, pageInfo, totalCount).

PITFALL 10: Schema-first vs code-first confusion
  Schema-first: write .graphql files, generate code.
  Code-first: write TypeScript, generate schema.
  Pick one, be consistent. Both work.

PITFALL 11: Not using fragments
  Duplicating field selections across queries.
  Fix: Define fragments for common patterns, reuse.

PITFALL 12: Ignoring caching
  Every query hits DB even for rarely-changing data.
  Fix: Apollo cache policies, CDN caching, Redis.

PITFALL 13: Mutations without optimistic UI
  User waits for server response → slow perceived performance.
  Fix: optimisticResponse in Apollo Client mutations.

PITFALL 14: Not versioning deprecations
  Remove field → break clients.
  Fix: @deprecated directive, then remove after grace period.
  type User {
    name: String!
    fullName: String! @deprecated(reason: "Use 'name' instead")
  }

PITFALL 15: Testing only happy paths
  Fix: Test error cases, auth failures, validation, edge cases.
  Use Apollo's MockedProvider for component tests.
```