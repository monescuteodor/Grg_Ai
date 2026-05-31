# Objective-C Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH OBJECTIVE-C


## Remarks

Objective-C is a general-purpose, object-oriented language that adds Smalltalk-style messaging to C. It was the primary language for Apple platforms (macOS, iOS) before Swift. Objective-C and Swift can interoperate in the same project.

Tools: Xcode, clang compiler, AppKit (macOS), UIKit (iOS), Foundation framework.


## Hello World

```objc
// hello.m
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"Hello, World!");
        NSLog(@"Hello, %@!", @"Objective-C");
    }
    return 0;
}
```

```bash
clang -framework Foundation hello.m -o hello
./hello

# Xcode: New Project > macOS > Command Line Tool
```


---

# CHAPTER 2: BASIC SYNTAX AND TYPES


## Types and Variables

```objc
#import <Foundation/Foundation.h>

int main() {
    @autoreleasepool {
        // C types
        int n = 42;
        float f = 3.14f;
        double d = 3.14159265;
        BOOL flag = YES;        // YES/NO instead of true/false
        char c = 'A';

        // NSInteger / NSUInteger (platform-sized)
        NSInteger size = 100;
        NSUInteger count = 200;
        CGFloat width = 100.0;

        // Objective-C objects (always pointers)
        NSString *str = @"Hello";
        NSNumber *num = @42;           // boxed number
        NSNumber *flt = @3.14;
        NSNumber *yes = @YES;
        NSArray  *arr = @[@1, @2, @3];
        NSDictionary *dict = @{@"key": @"value"};

        // NSLog — formatted print
        NSLog(@"String: %@", str);
        NSLog(@"Int: %ld", (long)size);
        NSLog(@"Float: %f", d);

        // nil (null for objects)
        NSString *empty = nil;
        if (empty == nil) NSLog(@"nil!");

        // id — generic object type
        id obj = @"anything";
        obj = @42;
    }
    return 0;
}
```

## Strings

```objc
NSString *s = @"Hello, World!";
NSUInteger len = s.length;                     // 13
NSString *upper = [s uppercaseString];
NSString *lower = [s lowercaseString];
BOOL contains = [s containsString:@"World"];   // YES
BOOL starts   = [s hasPrefix:@"Hello"];
BOOL ends     = [s hasSuffix:@"!"];
NSRange range = [s rangeOfString:@"World"];    // {7, 5}
NSString *sub = [s substringWithRange:NSMakeRange(0, 5)]; // "Hello"
NSString *rep = [s stringByReplacingOccurrencesOfString:@"World"
                                             withString:@"ObjC"];

// String formatting
NSString *msg = [NSString stringWithFormat:@"Name: %@, Age: %ld", @"Alice", 30L];

// Mutable string
NSMutableString *ms = [NSMutableString stringWithString:@"Hello"];
[ms appendString:@", World!"];
[ms insertString:@"!!" atIndex:5];
[ms replaceCharactersInRange:NSMakeRange(0,5) withString:@"Hi"];
```


---

# CHAPTER 3: COLLECTIONS


## NSArray, NSDictionary, NSSet

```objc
// NSArray (immutable)
NSArray *arr = @[@"Alice", @"Bob", @"Carol", @42, @YES];
NSUInteger count = arr.count;                    // 5
id first = arr[0];                               // @"Alice"
id last  = arr.lastObject;                       // @YES

BOOL has = [arr containsObject:@"Bob"];           // YES
NSUInteger idx = [arr indexOfObject:@"Bob"];      // 1

// Enumerate
for (id item in arr) {
    NSLog(@"%@", item);
}

[arr enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop) {
    NSLog(@"[%lu] %@", idx, obj);
}];

// NSMutableArray
NSMutableArray *ma = [NSMutableArray arrayWithArray:arr];
[ma addObject:@"Dave"];
[ma insertObject:@"Zero" atIndex:0];
[ma removeObject:@"Bob"];
[ma removeObjectAtIndex:0];
[ma sortUsingComparator:^NSComparisonResult(id a, id b) {
    return [a compare:b];
}];

// NSDictionary (immutable)
NSDictionary *d = @{
    @"name": @"Alice",
    @"age":  @30,
    @"city": @"NYC",
};
id name = d[@"name"];                           // @"Alice"
NSArray *keys = d.allKeys;
NSArray *vals = d.allValues;

for (NSString *key in d) {
    NSLog(@"%@: %@", key, d[key]);
}

// NSMutableDictionary
NSMutableDictionary *md = [NSMutableDictionary dictionary];
md[@"x"] = @1;
md[@"y"] = @2;
[md removeObjectForKey:@"x"];

// NSSet / NSMutableSet
NSSet *set = [NSSet setWithArray:@[@1, @2, @3, @2, @1]];
NSMutableSet *ms2 = [NSMutableSet setWithSet:set];
[ms2 addObject:@4];
[ms2 removeObject:@1];
BOOL has2 = [set containsObject:@2];
NSSet *union_set = [set setByAddingObjectsFromSet:ms2];
```


---

# CHAPTER 4: CLASSES AND METHODS


## Object-Oriented Programming

```objc
// Animal.h — interface
#import <Foundation/Foundation.h>

@interface Animal : NSObject

@property (nonatomic, strong) NSString *name;
@property (nonatomic, copy)   NSString *sound;
@property (nonatomic, assign) NSInteger age;
@property (nonatomic, readonly) BOOL isAdult;

+ (instancetype)animalWithName:(NSString *)name sound:(NSString *)sound;
- (instancetype)initWithName:(NSString *)name sound:(NSString *)sound;
- (NSString *)speak;

@end

// Animal.m — implementation
#import "Animal.h"

@implementation Animal

+ (instancetype)animalWithName:(NSString *)name sound:(NSString *)sound {
    return [[self alloc] initWithName:name sound:sound];
}

- (instancetype)initWithName:(NSString *)name sound:(NSString *)sound {
    self = [super init];
    if (self) {
        _name  = [name copy];
        _sound = [sound copy];
        _age   = 0;
    }
    return self;
}

- (BOOL)isAdult { return _age >= 1; }

- (NSString *)speak {
    return [NSString stringWithFormat:@"%@ says %@", self.name, self.sound];
}

- (NSString *)description {
    return [NSString stringWithFormat:@"Animal(%@)", self.name];
}

@end

// Dog.h
@interface Dog : Animal
@property (nonatomic, copy) NSString *breed;
+ (instancetype)dogWithName:(NSString *)name breed:(NSString *)breed;
- (NSString *)fetch;
@end

// Dog.m
@implementation Dog
+ (instancetype)dogWithName:(NSString *)name breed:(NSString *)breed {
    Dog *dog = [[self alloc] initWithName:name sound:@"Woof"];
    dog.breed = breed;
    return dog;
}
- (NSString *)speak { return [[super speak] stringByAppendingString:@"!"]; }
- (NSString *)fetch { return [NSString stringWithFormat:@"%@ fetches!", self.name]; }
@end
```


---

# CHAPTER 5: PROTOCOLS AND CATEGORIES


## Protocols and Extensions

```objc
// Protocol (interface)
@protocol Printable <NSObject>
@required
- (void)printDescription;
@optional
- (NSString *)prettyDescription;
@end

// Conforming to protocol
@interface Person : NSObject <Printable, NSCopying>
@property (nonatomic, copy) NSString *name;
@property (nonatomic) NSInteger age;
- (instancetype)initWithName:(NSString *)name age:(NSInteger)age;
@end

@implementation Person
- (instancetype)initWithName:(NSString *)n age:(NSInteger)a {
    self = [super init];
    if (self) { _name = n; _age = a; }
    return self;
}
- (void)printDescription {
    NSLog(@"Person: %@, age %ld", _name, _age);
}
- (id)copyWithZone:(NSZone *)zone {
    return [[Person allocWithZone:zone] initWithName:_name age:_age];
}
@end

// Category (extend existing class, even NSString)
@interface NSString (Utilities)
- (BOOL)isPalindrome;
- (NSString *)reversed;
- (NSInteger)wordCount;
@end

@implementation NSString (Utilities)
- (BOOL)isPalindrome {
    NSString *lower = [self lowercaseString];
    return [lower isEqualToString:[self reversed]];
}
- (NSString *)reversed {
    return [NSString stringWithString:
        [[self componentsSeparatedByString:@""] reverseObjectEnumerator].allObjects
        componentsJoinedByString:@""]];
}
- (NSInteger)wordCount {
    return [[self componentsSeparatedByCharactersInSet:
        [NSCharacterSet whitespaceAndNewlineCharacterSet]] count];
}
@end

// Usage
NSLog(@"%@", [@"racecar" isPalindrome] ? @"palindrome" : @"not");
```


---

# CHAPTER 6: MEMORY MANAGEMENT


## ARC and Memory

```objc
// ARC (Automatic Reference Counting) — modern Objective-C
// Strong references keep objects alive
@property (nonatomic, strong) NSObject *obj;    // strong (default for objects)
@property (nonatomic, weak)   id<Delegate> delegate;  // weak (no ownership)
@property (nonatomic, copy)   NSString *name;   // copy (defensive for mutable)
@property (nonatomic, assign) NSInteger count;  // assign (primitives)

// Blocks and memory
typedef void (^CompletionBlock)(NSString *result);

- (void)doWorkWithCompletion:(CompletionBlock)completion {
    // Capture self weakly to avoid retain cycle
    __weak typeof(self) weakSelf = self;
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;
        NSString *result = [strongSelf computeResult];
        dispatch_async(dispatch_get_main_queue(), ^{
            completion(result);
        });
    });
}

// Autorelease pool (for loops creating many objects)
for (int i = 0; i < 10000; i++) {
    @autoreleasepool {
        NSString *s = [NSString stringWithFormat:@"item %d", i];
        // s autoreleased at end of pool
    }
}
```


---

# CHAPTER 7: GCD AND CONCURRENCY


## Grand Central Dispatch

```objc
#import <Foundation/Foundation.h>

// Queues
dispatch_queue_t main_q    = dispatch_get_main_queue();
dispatch_queue_t global_q  = dispatch_get_global_queue(QOS_CLASS_DEFAULT, 0);
dispatch_queue_t serial_q  = dispatch_queue_create("com.app.serial", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t concurrent = dispatch_queue_create("com.app.concurrent", DISPATCH_QUEUE_CONCURRENT);

// Async dispatch
dispatch_async(global_q, ^{
    // Heavy work on background thread
    NSData *data = [NSData dataWithContentsOfURL:url];
    dispatch_async(main_q, ^{
        // Update UI on main thread
        self.imageView.image = [UIImage imageWithData:data];
    });
});

// Sync dispatch
dispatch_sync(serial_q, ^{
    // Runs synchronously
    [self.cache setObject:obj forKey:key];
});

// After delay
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 2 * NSEC_PER_SEC), main_q, ^{
    NSLog(@"After 2 seconds");
});

// dispatch_once (singleton)
static dispatch_once_t onceToken;
static MyClass *instance;
dispatch_once(&onceToken, ^{
    instance = [[MyClass alloc] init];
});

// NSOperationQueue
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
queue.maxConcurrentOperationCount = 4;

[queue addOperationWithBlock:^{
    // Background work
    NSLog(@"Background task");
    [[NSOperationQueue mainQueue] addOperationWithBlock:^{
        NSLog(@"Back on main thread");
    }];
}];
```


---

# CHAPTER 8: FOUNDATION FRAMEWORK


## Key Foundation Classes

```objc
// NSDate and NSDateFormatter
NSDate *now = [NSDate date];
NSDateFormatter *fmt = [[NSDateFormatter alloc] init];
fmt.dateFormat = @"yyyy-MM-dd HH:mm:ss";
NSString *dateStr = [fmt stringFromDate:now];
NSDate *parsed = [fmt dateFromString:@"2024-01-15 12:00:00"];

NSDateComponents *comps = [[NSCalendar currentCalendar]
    components:NSCalendarUnitYear|NSCalendarUnitMonth|NSCalendarUnitDay
    fromDate:now];
NSLog(@"Year: %ld", comps.year);

// NSFileManager
NSFileManager *fm = [NSFileManager defaultManager];
NSURL *docs = [[fm URLsForDirectory:NSDocumentDirectory inDomains:NSUserDomainMask] firstObject];

[fm createDirectoryAtURL:[docs URLByAppendingPathComponent:@"subdir"]
    withIntermediateDirectories:YES attributes:nil error:nil];

NSString *filePath = [[docs URLByAppendingPathComponent:@"data.txt"] path];
[@"Hello" writeToFile:filePath atomically:YES encoding:NSUTF8StringEncoding error:nil];
NSString *content = [NSString stringWithContentsOfFile:filePath
    encoding:NSUTF8StringEncoding error:nil];

// NSUserDefaults
NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
[defaults setObject:@"Alice" forKey:@"username"];
[defaults setInteger:42 forKey:@"score"];
[defaults synchronize];

NSString *username = [defaults stringForKey:@"username"];
NSInteger score = [defaults integerForKey:@"score"];

// NSNotificationCenter
[[NSNotificationCenter defaultCenter] addObserver:self
    selector:@selector(handleEvent:)
    name:@"MyEvent" object:nil];

[[NSNotificationCenter defaultCenter] postNotificationName:@"MyEvent"
    object:self userInfo:@{@"key": @"value"}];

[[NSNotificationCenter defaultCenter] removeObserver:self];

// KVC / KVO
[person setValue:@"Alice" forKey:@"name"];
NSString *name = [person valueForKey:@"name"];
NSArray *names = [people valueForKeyPath:@"@distinctUnionOfObjects.name"];

[person addObserver:self forKeyPath:@"name"
    options:NSKeyValueObservingOptionNew context:nil];
```
