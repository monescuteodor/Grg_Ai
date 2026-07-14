# NoSQL Databases Complete Reference


---

# CHAPTER 1: SQL vs NoSQL


## Remarks

NoSQL databases sacrifice some SQL features (joins, transactions, schema enforcement) for scalability, flexibility, and performance in specific use cases. There is no "best" database — the choice depends on your data model, query patterns, and scale requirements.


## When to Use What

```
SQL (Relational):
  ✅ Complex queries with JOINs
  ✅ Transactions (ACID — bank transfers, inventory)
  ✅ Structured data with relationships
  ✅ Data integrity (foreign keys, constraints)
  ✅ Ad-hoc queries (analytics, reporting)
  Examples: PostgreSQL, MySQL, SQLite
  Use for: e-commerce, banking, ERP, any app with complex relationships

NoSQL (Document):
  ✅ Flexible schema (different fields per document)
  ✅ Hierarchical/nested data (JSON-like)
  ✅ Rapid prototyping (schema changes easy)
  ✅ Horizontal scaling (sharding built-in)
  Examples: MongoDB, CouchDB, Firestore
  Use for: CMS, user profiles, catalogs, content management

NoSQL (Key-Value):
  ✅ Ultra-fast simple lookups
  ✅ Caching
  ✅ Session storage
  ✅ Simple data model
  Examples: Redis, DynamoDB, Memcached
  Use for: caching, sessions, rate limiting, real-time counters

NoSQL (Column-Family):
  ✅ Write-heavy workloads
  ✅ Time-series data
  ✅ Massive scale (petabytes)
  Examples: Cassandra, HBase, ScyllaDB
  Use for: IoT data, event logs, analytics at scale

NoSQL (Graph):
  ✅ Relationship-heavy queries
  ✅ Social networks, recommendations
  ✅ Path finding, network analysis
  Examples: Neo4j, Amazon Neptune
  Use for: social graphs, fraud detection, knowledge graphs
```


---

# CHAPTER 2: MONGODB


## Document Model

```javascript
// MongoDB stores DOCUMENTS (JSON-like objects called BSON)
// No fixed schema — each document can have different fields

// Insert
db.users.insertOne({
    name: "Alice",
    age: 30,
    email: "alice@example.com",
    address: {
        city: "Brașov",
        country: "Romania"
    },
    tags: ["developer", "python", "ai"],
    createdAt: new Date()
});

// Flexible schema: this document has different fields!
db.users.insertOne({
    name: "Bob",
    age: 25,
    company: "TechCorp",    // Alice doesn't have this field
    skills: {               // Different structure than Alice
        primary: "JavaScript",
        years: 5
    }
});

// Find (query)
db.users.find({ age: { $gt: 25 } });                    // Age > 25
db.users.find({ "address.city": "Brașov" });             // Nested field
db.users.find({ tags: "python" });                       // Array contains
db.users.find({ age: { $gte: 25, $lte: 35 } });         // Range
db.users.find({ name: /^ali/i });                        // Regex
db.users.find({}, { name: 1, email: 1, _id: 0 });       // Projection (select fields)

// Update
db.users.updateOne(
    { name: "Alice" },
    { 
        $set: { age: 31 },           // Set field
        $push: { tags: "fastapi" },  // Add to array
        $inc: { loginCount: 1 }      // Increment
    }
);

// Aggregation pipeline (like SQL GROUP BY)
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: {
        _id: "$userId",
        totalSpent: { $sum: "$total" },
        orderCount: { $count: {} },
        avgOrder: { $avg: "$total" }
    }},
    { $sort: { totalSpent: -1 } },
    { $limit: 10 }
]);

// Indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ "address.city": 1, age: -1 });
db.users.createIndex({ name: "text" });  // Full-text search
```

```python
# PyMongo (Python driver)
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.myapp
users = db.users

# Insert
user_id = users.insert_one({
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
}).inserted_id

# Find
user = users.find_one({"email": "alice@example.com"})
adults = list(users.find({"age": {"$gte": 18}}).sort("name", 1).limit(10))

# Update
users.update_one(
    {"_id": user_id},
    {"$set": {"age": 31}, "$push": {"tags": "python"}}
)

# Delete
users.delete_one({"_id": user_id})
```


---

# CHAPTER 3: DYNAMODB (AWS)


## Key-Value + Document

```python
# DynamoDB: fully managed, auto-scaling, pay-per-request
# DESIGN: think about ACCESS PATTERNS first, then design tables

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put item
table.put_item(Item={
    'PK': 'USER#alice',           # Partition key
    'SK': 'PROFILE',              # Sort key
    'name': 'Alice',
    'age': 30,
    'email': 'alice@example.com',
})

# Store user's orders in SAME table (single table design)
table.put_item(Item={
    'PK': 'USER#alice',
    'SK': 'ORDER#2026-06-10#001',
    'total': 99.99,
    'status': 'completed',
})

# Get user profile
response = table.get_item(Key={'PK': 'USER#alice', 'SK': 'PROFILE'})
user = response['Item']

# Get all orders for user (query by partition key + sort key prefix)
response = table.query(
    KeyConditionExpression='PK = :pk AND begins_with(SK, :prefix)',
    ExpressionAttributeValues={':pk': 'USER#alice', ':prefix': 'ORDER#'}
)
orders = response['Items']

# SINGLE TABLE DESIGN:
# All entities in ONE table. Access patterns determine key design.
# PK=USER#alice, SK=PROFILE     → User profile
# PK=USER#alice, SK=ORDER#001   → User's order
# PK=USER#alice, SK=SESSION#abc → User's session
# One query gets everything about a user!
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Using NoSQL because "SQL doesn't scale"
  PostgreSQL handles millions of rows fine. Most apps never outgrow it.
  Fix: start with PostgreSQL. Move to NoSQL only when you hit real limits.

PITFALL 2: MongoDB without schema validation
  Typo in field name → silently stores wrong data.
  Fix: use MongoDB schema validation or Mongoose (Node.js ORM with schemas).

PITFALL 3: Embedding too much data in MongoDB
  16MB document limit. Embedding 10,000 comments in a post → bloat.
  Fix: embed small/bounded data, reference large/unbounded data.

PITFALL 4: No indexes on frequently queried fields
  find({ email: "..." }) without index → full collection scan.
  Fix: create indexes on fields used in queries. Use explain() to verify.

PITFALL 5: Using MongoDB for transactions
  Multi-document transactions added in 4.0 but slower than SQL.
  Fix: if you need strong transactions (banking, inventory) → use PostgreSQL.

PITFALL 6: DynamoDB without understanding access patterns
  Designed table → realized you need a query DynamoDB can't do.
  Fix: list ALL access patterns BEFORE designing table keys.

PITFALL 7: Treating NoSQL like SQL
  Trying to JOIN collections in MongoDB → slow, multiple queries.
  Fix: denormalize. Store redundant data. Trade storage for speed.

PITFALL 8: Not considering consistency
  MongoDB: reads from secondary replicas may return stale data.
  Fix: use readPreference "primary" for critical reads, or use readConcern "majority".
```