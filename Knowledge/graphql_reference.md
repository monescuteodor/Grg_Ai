# GraphQL Complete Reference


---

# CHAPTER 1: QUERIES AND MUTATIONS

```graphql
# Query — fetch data
query {
  user(id: "42") {
    name
    email
    posts {
      title
      comments {
        text
        author { name }
      }
    }
  }
}

# Query with variables
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
  }
}
# Variables: { "id": "42" }

# Mutation — change data
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
  }
}
# Variables: { "input": { "title": "Hello", "body": "World" } }

# Subscription — real-time
subscription {
  newMessage(chatId: "room1") {
    text
    author { name }
    createdAt
  }
}
```


## Schema Definition

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  posts: [Post!]!
  createdAt: String!
}

type Post {
  id: ID!
  title: String!
  body: String
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  text: String!
  author: User!
}

input PostInput {
  title: String!
  body: String
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User!
  createPost(input: PostInput!): Post!
  deletePost(id: ID!): Boolean!
}
```


## Node.js Server (Apollo)

```javascript
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type User { id: ID!, name: String!, email: String! }
  type Query { users: [User!]!, user(id: ID!): User }
  type Mutation { createUser(name: String!, email: String!): User! }
`;

let users = [{ id: '1', name: 'Alice', email: 'alice@mail.com' }];

const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(u => u.id === id),
  },
  Mutation: {
    createUser: (_, { name, email }) => {
      const user = { id: String(users.length + 1), name, email };
      users.push(user);
      return user;
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
server.listen().then(({ url }) => console.log('Server at ' + url));
```


## Frontend Fetch

```javascript
async function graphqlQuery(query, variables = {}) {
    const res = await fetch('/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables }),
    });
    const { data, errors } = await res.json();
    if (errors) throw new Error(errors[0].message);
    return data;
}

// Usage
const { users } = await graphqlQuery('{ users { name email } }');
const { user } = await graphqlQuery(
    'query($id: ID!) { user(id: $id) { name posts { title } } }',
    { id: '42' }
);
```