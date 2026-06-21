# Flutter Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH FLUTTER


## Remarks

Flutter is Google's UI toolkit for building natively compiled apps for mobile (iOS, Android), web, and desktop from a single Dart codebase. Unlike React Native, Flutter draws its own pixels using Skia/Impeller engine — no native UI widgets, so apps look identical on every platform.

Key concepts: **Widgets** (everything is a widget — UI, layout, styling, animations), **Dart language** (typed, async/await, sound null safety), **Hot Reload** (instant code changes during development), **Material Design** & **Cupertino** widget libraries (Android/iOS look).

Used by: Google Pay, BMW, Toyota, Alibaba, eBay Motors, Nubank, ByteDance apps.

Tools: Flutter SDK, Dart SDK, VS Code/Android Studio with Flutter plugin, DevTools (profiling), `flutter doctor` (env check).


## Project Setup

```bash
# Install Flutter SDK from flutter.dev
# Verify installation
flutter doctor

# Create new app
flutter create my_app
cd my_app

# Run on connected device/emulator
flutter run                    # Debug mode
flutter run --release          # Release build

# List devices/emulators
flutter devices
flutter emulators
flutter emulators --launch <id>

# Build for production
flutter build apk                  # Android APK
flutter build appbundle            # Android AAB (Play Store)
flutter build ios                  # iOS (needs Xcode)
flutter build web                  # Web

# Manage dependencies (pubspec.yaml)
flutter pub add http
flutter pub get
flutter pub upgrade
```


## Hello World

```dart
// lib/main.dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hello World',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hello, Flutter!')),
      body: const Center(
        child: Text('Welcome', style: TextStyle(fontSize: 24)),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
```


---

# CHAPTER 2: WIDGETS FUNDAMENTALS


## StatelessWidget vs StatefulWidget

```dart
// StatelessWidget - immutable, no internal state
class Greeting extends StatelessWidget {
  final String name;
  final int age;

  const Greeting({super.key, required this.name, this.age = 0});

  @override
  Widget build(BuildContext context) {
    return Text('Hello $name, age $age');
  }
}

// Usage:
// Greeting(name: 'Alice', age: 25)


// StatefulWidget - has mutable State object
class Counter extends StatefulWidget {
  final int initial;

  const Counter({super.key, this.initial = 0});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  late int _count;

  @override
  void initState() {
    super.initState();
    _count = widget.initial;   // Access widget properties
    // One-time setup: subscriptions, controllers, etc.
  }

  @override
  void didUpdateWidget(Counter oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Called when parent rebuilds with new widget config
    if (widget.initial != oldWidget.initial) {
      _count = widget.initial;   // React to prop changes
    }
  }

  @override
  void dispose() {
    // Cleanup: cancel subscriptions, dispose controllers
    super.dispose();
  }

  void _increment() {
    setState(() {   // setState triggers rebuild
      _count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(onPressed: _increment, child: const Text('+')),
      ],
    );
  }
}
```


## Layout Widgets

```dart
// Container - box with padding, margin, decoration
Container(
  width: 200,
  height: 100,
  padding: const EdgeInsets.all(16),
  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: Colors.blue.shade100,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(color: Colors.blue, width: 2),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.2),
        blurRadius: 8,
        offset: const Offset(0, 4),
      ),
    ],
  ),
  child: const Text('Card-like'),
)

// Row - horizontal layout
Row(
  mainAxisAlignment: MainAxisAlignment.spaceBetween,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Icon(Icons.home),
    Text('Home'),
    Icon(Icons.settings),
  ],
)

// Column - vertical layout
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Text('Title'),
    SizedBox(height: 8),    // Spacer
    Text('Subtitle'),
  ],
)

// Expanded - fill available space (in Row/Column/Flex)
Row(children: [
  Container(width: 100, color: Colors.red),
  Expanded(child: Container(color: Colors.green)),   // Takes remaining
  Expanded(flex: 2, child: Container(color: Colors.blue)),   // 2x size
])

// Stack - layered widgets (z-axis)
Stack(
  alignment: Alignment.center,
  children: [
    Image.asset('background.jpg'),
    Positioned(
      top: 16,
      right: 16,
      child: Icon(Icons.favorite, color: Colors.red),
    ),
    const Text('Centered'),
  ],
)

// Wrap - flow to next line when out of space
Wrap(
  spacing: 8,        // Horizontal gap
  runSpacing: 4,     // Vertical gap between rows
  children: tags.map((tag) => Chip(label: Text(tag))).toList(),
)

// SafeArea - avoid notches, status bar, navigation bar
SafeArea(
  child: Scaffold(/* ... */),
)

// SingleChildScrollView - scrollable single child
SingleChildScrollView(
  scrollDirection: Axis.vertical,
  padding: const EdgeInsets.all(16),
  child: Column(children: [/* lots of content */]),
)
```


## Common UI Widgets

```dart
// Text with styling
Text(
  'Hello',
  style: TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
    color: Colors.black87,
    letterSpacing: 0.5,
    decoration: TextDecoration.underline,
  ),
  textAlign: TextAlign.center,
  maxLines: 2,
  overflow: TextOverflow.ellipsis,
)

// RichText - mixed styles in one string
RichText(
  text: const TextSpan(
    style: TextStyle(color: Colors.black, fontSize: 16),
    children: [
      TextSpan(text: 'Hello '),
      TextSpan(text: 'World', style: TextStyle(fontWeight: FontWeight.bold)),
      TextSpan(text: '!'),
    ],
  ),
)

// Buttons
ElevatedButton(
  onPressed: () => print('Pressed'),
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
  ),
  child: const Text('Click Me'),
)

TextButton(onPressed: () {}, child: const Text('Text'))
OutlinedButton(onPressed: () {}, child: const Text('Outlined'))
IconButton(icon: const Icon(Icons.menu), onPressed: () {})
FloatingActionButton(child: const Icon(Icons.add), onPressed: () {})

// Disabled button (onPressed: null)
ElevatedButton(onPressed: null, child: const Text('Disabled'))

// TextField
TextField(
  controller: _textController,
  decoration: const InputDecoration(
    labelText: 'Email',
    hintText: 'you@example.com',
    prefixIcon: Icon(Icons.email),
    border: OutlineInputBorder(),
  ),
  keyboardType: TextInputType.emailAddress,
  textInputAction: TextInputAction.done,
  onChanged: (value) => print(value),
  onSubmitted: (value) => print('Submitted: $value'),
)

// Image
Image.asset('assets/logo.png')
Image.network('https://example.com/img.jpg', loadingBuilder: (ctx, child, p) {
  if (p == null) return child;
  return const CircularProgressIndicator();
})

// Icons
Icon(Icons.favorite, size: 24, color: Colors.red)

// Card
Card(
  elevation: 4,
  margin: const EdgeInsets.all(8),
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(/* content */),
  ),
)

// ListTile - common list item pattern
ListTile(
  leading: const Icon(Icons.person),
  title: const Text('Alice'),
  subtitle: const Text('Software engineer'),
  trailing: const Icon(Icons.chevron_right),
  onTap: () => print('Tapped'),
)

// CircularProgressIndicator / LinearProgressIndicator
const CircularProgressIndicator()
LinearProgressIndicator(value: 0.7)
```


---

# CHAPTER 3: NAVIGATION AND ROUTING


## Imperative Navigation (Navigator 1.0)

```dart
// Push new screen
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailPage(id: 123)),
);

// Pop current screen
Navigator.pop(context);

// Pop with result
Navigator.pop(context, 'result data');

// Receive result from popped screen
final result = await Navigator.push<String>(
  context,
  MaterialPageRoute(builder: (_) => PickerPage()),
);
print('Got: $result');

// Replace (no back)
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (_) => const HomePage()),
);

// Pop everything until route
Navigator.popUntil(context, (route) => route.isFirst);

// Push and clear stack
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (_) => const LoginPage()),
  (route) => false,   // Remove all
);

// Named routes (define in MaterialApp)
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => const HomePage(),
    '/profile': (context) => const ProfilePage(),
    '/settings': (context) => const SettingsPage(),
  },
)

// Navigate by name
Navigator.pushNamed(context, '/profile');
Navigator.pushNamed(context, '/profile', arguments: {'id': 42});

// Receive arguments
class ProfilePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    final id = args['id'];
    return Text('Profile $id');
  }
}
```


## go_router — Declarative Navigation (Recommended)

```dart
// pubspec.yaml: go_router: ^14.0.0
import 'package:go_router/go_router.dart';

final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/users/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return UserPage(userId: id);
      },
      routes: [
        // Nested route: /users/:id/edit
        GoRoute(
          path: 'edit',
          builder: (context, state) => UserEditPage(
            userId: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginPage(),
    ),
  ],

  // Redirect logic for auth
  redirect: (context, state) {
    final loggedIn = authService.isLoggedIn;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!loggedIn && !isLoggingIn) return '/login';
    if (loggedIn && isLoggingIn) return '/';
    return null;   // No redirect
  },

  errorBuilder: (context, state) => NotFoundPage(),
);

// MaterialApp.router setup
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
    );
  }
}

// Navigate
context.go('/users/42');                    // Replace stack
context.push('/users/42');                  // Push new route
context.pop();                              // Back
context.go('/users/42', extra: userObject); // Pass complex objects

// Bottom navigation with go_router (ShellRoute)
final router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/feed', builder: (_, __) => FeedPage()),
        GoRoute(path: '/search', builder: (_, __) => SearchPage()),
        GoRoute(path: '/profile', builder: (_, __) => ProfilePage()),
      ],
    ),
  ],
);
```


---

# CHAPTER 4: STATE MANAGEMENT


## setState — Local Widget State

```dart
// Good for: small/local state (form inputs, toggles, counters)
class ToggleSwitch extends StatefulWidget {
  const ToggleSwitch({super.key});

  @override
  State<ToggleSwitch> createState() => _ToggleSwitchState();
}

class _ToggleSwitchState extends State<ToggleSwitch> {
  bool _isOn = false;

  @override
  Widget build(BuildContext context) {
    return Switch(
      value: _isOn,
      onChanged: (value) => setState(() => _isOn = value),
    );
  }
}
```


## Provider — Simple State Management

```dart
// pubspec.yaml: provider: ^6.0.0
import 'package:provider/provider.dart';

// 1. Model with ChangeNotifier
class CartModel extends ChangeNotifier {
  final List<Item> _items = [];

  List<Item> get items => List.unmodifiable(_items);
  int get count => _items.length;
  double get total => _items.fold(0.0, (sum, item) => sum + item.price);

  void add(Item item) {
    _items.add(item);
    notifyListeners();   // Trigger UI rebuild
  }

  void remove(Item item) {
    _items.remove(item);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}

// 2. Provide at app level
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartModel()),
        ChangeNotifierProvider(create: (_) => AuthModel()),
      ],
      child: const MyApp(),
    ),
  );
}

// 3. Consume in widgets
class CartBadge extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Listens to changes - rebuilds when notifyListeners called
    final cart = context.watch<CartModel>();
    return Badge(
      label: Text('${cart.count}'),
      child: const Icon(Icons.shopping_cart),
    );
  }
}

class AddButton extends StatelessWidget {
  final Item item;
  const AddButton({required this.item});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        // read - get current value, doesn't subscribe
        context.read<CartModel>().add(item);
      },
      child: const Text('Add'),
    );
  }
}

// Selector - rebuild only when specific value changes
class TotalDisplay extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Selector<CartModel, double>(
      selector: (_, cart) => cart.total,
      builder: (context, total, child) => Text('Total: \$${total.toStringAsFixed(2)}'),
    );
  }
}
```


## Riverpod — Modern State Management

```dart
// pubspec.yaml: flutter_riverpod: ^2.0.0
// Riverpod is provider-but-better: compile-time safe, testable, no BuildContext needed

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

// Wrap app
void main() {
  runApp(
    const ProviderScope(child: MyApp()),
  );
}

// 1. Simple value provider
final greetingProvider = Provider<String>((ref) => 'Hello, World');

// 2. StateProvider - mutable simple value
final counterProvider = StateProvider<int>((ref) => 0);

// 3. NotifierProvider - complex mutable state
class CartNotifier extends Notifier<List<Item>> {
  @override
  List<Item> build() => [];   // Initial state

  void add(Item item) {
    state = [...state, item];   // Create new list (immutable update)
  }

  void remove(int index) {
    state = [
      for (var i = 0; i < state.length; i++)
        if (i != index) state[i],
    ];
  }

  void clear() => state = [];
}

final cartProvider = NotifierProvider<CartNotifier, List<Item>>(CartNotifier.new);

// 4. AsyncNotifier - async state (loading/error/data)
class PostsNotifier extends AsyncNotifier<List<Post>> {
  @override
  Future<List<Post>> build() async {
    // Initial fetch
    final response = await http.get(Uri.parse('https://api.example.com/posts'));
    return parsePosts(response.body);
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final response = await http.get(Uri.parse('https://api.example.com/posts'));
      return parsePosts(response.body);
    });
  }

  Future<void> addPost(Post post) async {
    final current = state.value ?? [];
    state = AsyncValue.data([post, ...current]);
    // Sync with server
    await http.post(Uri.parse('https://api.example.com/posts'), body: post.toJson());
  }
}

final postsProvider = AsyncNotifierProvider<PostsNotifier, List<Post>>(PostsNotifier.new);

// 5. FutureProvider - one-time async value
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final response = await http.get(Uri.parse('/api/users/$userId'));
  return User.fromJson(jsonDecode(response.body));
});

// Consume providers - use ConsumerWidget instead of StatelessWidget
class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch - subscribes to changes
    final cart = ref.watch(cartProvider);

    return Scaffold(
      appBar: AppBar(title: Text('Cart (${cart.length})')),
      body: ListView.builder(
        itemCount: cart.length,
        itemBuilder: (context, index) {
          final item = cart[index];
          return ListTile(
            title: Text(item.name),
            trailing: IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () {
                // Read - get notifier to call methods
                ref.read(cartProvider.notifier).remove(index);
              },
            ),
          );
        },
      ),
    );
  }
}

// AsyncValue handling
class PostsScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final postsAsync = ref.watch(postsProvider);

    return postsAsync.when(
      data: (posts) => ListView.builder(
        itemCount: posts.length,
        itemBuilder: (context, i) => ListTile(title: Text(posts[i].title)),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(child: Text('Error: $error')),
    );
  }
}

// Listen to changes (side effects)
class HomeScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen<List<Item>>(cartProvider, (previous, next) {
      if (next.length > (previous?.length ?? 0)) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Item added!')),
        );
      }
    });
    return Scaffold(/* ... */);
  }
}
```


## BLoC Pattern — Enterprise State Management

```dart
// pubspec.yaml: flutter_bloc: ^8.0.0
// Best for: complex business logic, predictable state, testing

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

// 1. Events (inputs to bloc)
abstract class CounterEvent extends Equatable {
  const CounterEvent();
  @override
  List<Object> get props => [];
}

class CounterIncremented extends CounterEvent {}
class CounterDecremented extends CounterEvent {}
class CounterReset extends CounterEvent {}
class CounterSetTo extends CounterEvent {
  final int value;
  const CounterSetTo(this.value);
  @override
  List<Object> get props => [value];
}

// 2. State
class CounterState extends Equatable {
  final int count;
  final bool isLoading;
  const CounterState({this.count = 0, this.isLoading = false});

  CounterState copyWith({int? count, bool? isLoading}) {
    return CounterState(
      count: count ?? this.count,
      isLoading: isLoading ?? this.isLoading,
    );
  }

  @override
  List<Object> get props => [count, isLoading];
}

// 3. Bloc
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState()) {
    on<CounterIncremented>((event, emit) {
      emit(state.copyWith(count: state.count + 1));
    });

    on<CounterDecremented>((event, emit) {
      emit(state.copyWith(count: state.count - 1));
    });

    on<CounterReset>((event, emit) {
      emit(const CounterState());
    });

    on<CounterSetTo>((event, emit) async {
      emit(state.copyWith(isLoading: true));
      await Future.delayed(const Duration(seconds: 1));   // Simulate async
      emit(state.copyWith(count: event.value, isLoading: false));
    });
  }
}

// 4. Provide bloc
void main() {
  runApp(
    BlocProvider(
      create: (_) => CounterBloc(),
      child: const MyApp(),
    ),
  );
}

// 5. Use in widgets
class CounterDisplay extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocBuilder<CounterBloc, CounterState>(
        builder: (context, state) {
          if (state.isLoading) return const CircularProgressIndicator();
          return Text('Count: ${state.count}');
        },
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton(
            heroTag: 'inc',
            onPressed: () => context.read<CounterBloc>().add(CounterIncremented()),
            child: const Icon(Icons.add),
          ),
          const SizedBox(height: 8),
          FloatingActionButton(
            heroTag: 'dec',
            onPressed: () => context.read<CounterBloc>().add(CounterDecremented()),
            child: const Icon(Icons.remove),
          ),
        ],
      ),
    );
  }
}

// BlocListener - side effects (no rebuild)
BlocListener<CounterBloc, CounterState>(
  listener: (context, state) {
    if (state.count == 10) {
      showDialog(context: context, builder: (_) => const AlertDialog(
        title: Text('Milestone!'),
      ));
    }
  },
  child: const CounterDisplay(),
)
```


---

# CHAPTER 5: NETWORKING


## HTTP Requests with dio

```dart
// pubspec.yaml: dio: ^5.0.0
import 'package:dio/dio.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {'Content-Type': 'application/json'},
    ));

    // Logging interceptor (debug only)
    _dio.interceptors.add(LogInterceptor(responseBody: true));

    // Auth interceptor
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await SecureStorage.getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Refresh token
          final refreshed = await _refreshToken();
          if (refreshed) {
            // Retry original request
            final newOptions = error.requestOptions;
            final response = await _dio.fetch(newOptions);
            return handler.resolve(response);
          }
        }
        return handler.next(error);
      },
    ));
  }

  Future<User> getUser(String id) async {
    try {
      final response = await _dio.get('/users/$id');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<Post>> getPosts({int page = 1, int limit = 20}) async {
    final response = await _dio.get(
      '/posts',
      queryParameters: {'page': page, 'limit': limit},
    );
    return (response.data as List).map((j) => Post.fromJson(j)).toList();
  }

  Future<Post> createPost(Post post) async {
    final response = await _dio.post('/posts', data: post.toJson());
    return Post.fromJson(response.data);
  }

  Future<void> deletePost(String id) async {
    await _dio.delete('/posts/$id');
  }

  // File upload
  Future<String> uploadAvatar(String filePath) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(filePath, filename: 'avatar.jpg'),
    });
    final response = await _dio.post('/upload', data: formData);
    return response.data['url'];
  }

  // Cancel request
  CancelToken cancelToken = CancelToken();

  Future<List<Result>> search(String query) async {
    cancelToken.cancel();   // Cancel previous
    cancelToken = CancelToken();
    final response = await _dio.get('/search',
        queryParameters: {'q': query}, cancelToken: cancelToken);
    return (response.data as List).map((j) => Result.fromJson(j)).toList();
  }

  Exception _handleError(DioException e) {
    if (e.type == DioExceptionType.connectionTimeout) {
      return TimeoutException('Connection timeout');
    }
    if (e.response?.statusCode == 404) {
      return NotFoundException('Not found');
    }
    return ApiException(e.message ?? 'Unknown error');
  }
}
```


## JSON Serialization

```dart
// Manual approach for small models
class User {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;

  User({required this.id, required this.name, required this.email, required this.createdAt});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'email': email,
    'created_at': createdAt.toIso8601String(),
  };
}

// Auto-generated with freezed + json_serializable
// pubspec.yaml:
//   freezed_annotation: ^2.0.0
//   json_annotation: ^4.0.0
// dev: freezed: ^2.0.0, json_serializable: ^6.0.0, build_runner: ^2.0.0

import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    @Default(false) bool isActive,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Generate code: flutter pub run build_runner build
// Now you get: copyWith, ==, hashCode, toString, JSON serialization - free
final user = User(id: '1', name: 'Alice', email: 'a@b.com', createdAt: DateTime.now());
final updated = user.copyWith(name: 'Bob');
```


---

# CHAPTER 6: ANIMATIONS


## Implicit Animations (Easy)

```dart
// AnimatedContainer - tweens any property change
class AnimatedBox extends StatefulWidget {
  @override
  State<AnimatedBox> createState() => _AnimatedBoxState();
}

class _AnimatedBoxState extends State<AnimatedBox> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _expanded = !_expanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
        width: _expanded ? 200 : 100,
        height: _expanded ? 200 : 100,
        decoration: BoxDecoration(
          color: _expanded ? Colors.blue : Colors.red,
          borderRadius: BorderRadius.circular(_expanded ? 100 : 8),
        ),
      ),
    );
  }
}

// AnimatedOpacity, AnimatedAlign, AnimatedPositioned, AnimatedDefaultTextStyle...
AnimatedOpacity(
  duration: const Duration(milliseconds: 300),
  opacity: _visible ? 1.0 : 0.0,
  child: const Text('Fades'),
)

// AnimatedSwitcher - smooth widget transitions
AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  child: _showFirst
      ? const Text('First', key: ValueKey('first'))
      : const Text('Second', key: ValueKey('second')),
)

// Hero - shared element transitions between routes
// On screen A:
Hero(tag: 'avatar-$userId', child: CircleAvatar(/*...*/))
// On screen B (navigation target):
Hero(tag: 'avatar-$userId', child: CircleAvatar(/* bigger */))
```


## Explicit Animations (Full Control)

```dart
class FadeInWidget extends StatefulWidget {
  final Widget child;
  const FadeInWidget({required this.child});

  @override
  State<FadeInWidget> createState() => _FadeInWidgetState();
}

class _FadeInWidgetState extends State<FadeInWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeIn);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(opacity: _animation, child: widget.child);
  }
}

// Multiple animations - Tween
class SlideUpWidget extends StatefulWidget {
  @override
  State<SlideUpWidget> createState() => _SlideUpWidgetState();
}

class _SlideUpWidgetState extends State<SlideUpWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _offset;
  late Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );

    _offset = Tween<Offset>(
      begin: const Offset(0, 1),    // Start below screen
      end: Offset.zero,              // End in place
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));

    _opacity = Tween<double>(begin: 0.0, end: 1.0).animate(_controller);

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: _offset,
      child: FadeTransition(
        opacity: _opacity,
        child: const Text('Slides up + fades in'),
      ),
    );
  }
}

// Repeating with reverse
_controller.repeat(reverse: true);

// Listening to animation status
_controller.addStatusListener((status) {
  if (status == AnimationStatus.completed) {
    _controller.reverse();
  }
});
```


---

# CHAPTER 7: LISTS AND SCROLLING


## ListView and ListView.builder

```dart
// Simple - all items built upfront (small lists only)
ListView(
  children: [
    const Text('Item 1'),
    const Text('Item 2'),
    const Text('Item 3'),
  ],
)

// Builder - lazy build (large lists)
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    final item = items[index];
    return ListTile(
      title: Text(item.name),
      subtitle: Text(item.description),
      onTap: () => print('Tapped $index'),
    );
  },
)

// Separated - with dividers between items
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => const Divider(height: 1),
  itemBuilder: (context, index) => ListTile(title: Text(items[index].name)),
)

// Horizontal scroll
ListView.builder(
  scrollDirection: Axis.horizontal,
  itemCount: 10,
  itemBuilder: (context, index) => Container(
    width: 100,
    margin: const EdgeInsets.all(4),
    color: Colors.blue,
  ),
)

// Pull-to-refresh
RefreshIndicator(
  onRefresh: () async {
    await loadData();
  },
  child: ListView.builder(/* ... */),
)

// Infinite scroll
class InfiniteList extends StatefulWidget {
  @override
  State<InfiniteList> createState() => _InfiniteListState();
}

class _InfiniteListState extends State<InfiniteList> {
  final ScrollController _scrollController = ScrollController();
  final List<Item> _items = [];
  bool _isLoading = false;
  int _page = 1;

  @override
  void initState() {
    super.initState();
    _loadMore();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      _loadMore();
    }
  }

  Future<void> _loadMore() async {
    if (_isLoading) return;
    setState(() => _isLoading = true);

    final newItems = await api.getItems(page: _page);
    setState(() {
      _items.addAll(newItems);
      _page++;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _scrollController,
      itemCount: _items.length + (_isLoading ? 1 : 0),
      itemBuilder: (context, index) {
        if (index == _items.length) {
          return const Center(child: Padding(
            padding: EdgeInsets.all(16),
            child: CircularProgressIndicator(),
          ));
        }
        return ListTile(title: Text(_items[index].name));
      },
    );
  }
}
```


## CustomScrollView with Slivers

```dart
// Complex scrolling layouts - collapsing app bars, mixed content
CustomScrollView(
  slivers: [
    // Collapsing app bar with image
    SliverAppBar(
      expandedHeight: 200,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Profile'),
        background: Image.network('https://example.com/banner.jpg', fit: BoxFit.cover),
      ),
    ),

    // Static header
    const SliverToBoxAdapter(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Text('Posts', style: TextStyle(fontSize: 24)),
      ),
    ),

    // Lazy-built list
    SliverList.builder(
      itemCount: posts.length,
      itemBuilder: (context, index) => PostCard(post: posts[index]),
    ),

    // Grid section
    SliverGrid(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3),
      delegate: SliverChildBuilderDelegate(
        (context, index) => Image.network(photos[index]),
        childCount: photos.length,
      ),
    ),
  ],
)
```


---

# CHAPTER 8: PERSISTENCE


## SharedPreferences (Simple Key-Value)

```dart
// pubspec.yaml: shared_preferences: ^2.0.0
import 'package:shared_preferences/shared_preferences.dart';

class PrefsService {
  static late SharedPreferences _prefs;

  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  static Future<void> setDarkMode(bool enabled) =>
      _prefs.setBool('dark_mode', enabled);

  static bool getDarkMode() => _prefs.getBool('dark_mode') ?? false;

  static Future<void> setUsername(String name) => _prefs.setString('username', name);
  static String? getUsername() => _prefs.getString('username');

  static Future<void> clear() => _prefs.clear();
}

// Use in main()
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await PrefsService.init();
  runApp(const MyApp());
}
```


## SQLite with drift

```dart
// pubspec.yaml:
//   drift: ^2.0.0
//   sqlite3_flutter_libs: ^0.5.0
//   path_provider: ^2.0.0
// dev: drift_dev, build_runner

import 'package:drift/drift.dart';

class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 50)();
  TextColumn get email => text().unique()();
  IntColumn get age => integer()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // Queries
  Future<List<User>> getAllUsers() => select(users).get();

  Stream<List<User>> watchAllUsers() => select(users).watch();   // Reactive!

  Future<User?> getUser(int id) =>
      (select(users)..where((u) => u.id.equals(id))).getSingleOrNull();

  Future<int> insertUser(UsersCompanion user) => into(users).insert(user);

  Future<int> updateUser(User user) => update(users).replace(user);

  Future<int> deleteUser(int id) =>
      (delete(users)..where((u) => u.id.equals(id))).go();

  Future<List<User>> searchUsers(String query) =>
      (select(users)..where((u) => u.name.like('%$query%'))).get();
}

// Use database
final db = AppDatabase();
await db.insertUser(UsersCompanion.insert(
  name: 'Alice',
  email: 'a@b.com',
  age: 25,
));

// Reactive UI - StreamBuilder updates automatically
StreamBuilder<List<User>>(
  stream: db.watchAllUsers(),
  builder: (context, snapshot) {
    if (!snapshot.hasData) return const CircularProgressIndicator();
    final users = snapshot.data!;
    return ListView.builder(
      itemCount: users.length,
      itemBuilder: (_, i) => ListTile(title: Text(users[i].name)),
    );
  },
)
```


---

# CHAPTER 9: TESTING


## Unit, Widget, Integration Tests

```dart
// pubspec.yaml: flutter_test (built-in)
// Unit test - test business logic
// test/counter_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/counter.dart';

void main() {
  group('Counter', () {
    test('starts at zero', () {
      expect(Counter().value, 0);
    });

    test('increments correctly', () {
      final counter = Counter();
      counter.increment();
      expect(counter.value, 1);
    });

    test('throws on negative', () {
      expect(() => Counter().setValue(-1), throwsArgumentError);
    });
  });
}

// Widget test - test UI in isolation
// test/login_widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';

void main() {
  testWidgets('LoginPage shows error on empty submit', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: LoginPage()));

    // Find widgets
    expect(find.text('Login'), findsOneWidget);
    expect(find.byType(TextField), findsNWidgets(2));

    // Interact
    await tester.tap(find.text('Submit'));
    await tester.pumpAndSettle();   // Wait for animations

    // Verify error appears
    expect(find.text('Email is required'), findsOneWidget);
  });

  testWidgets('Counter increments', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CounterPage()));
    expect(find.text('0'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}

// Integration test - test full app on real device
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('login flow end-to-end', (tester) async {
    await tester.pumpWidget(const MyApp());

    await tester.enterText(find.byKey(const Key('email')), 'user@example.com');
    await tester.enterText(find.byKey(const Key('password')), 'pass123');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    expect(find.text('Welcome'), findsOneWidget);
  });
}
// Run: flutter test integration_test/
```


## Common Pitfalls

```dart
// PITFALL 1: setState after dispose
class _BadWidgetState extends State<BadWidget> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 5), () {
      setState(() {});   // CRASH if widget already disposed!
    });
  }
}

class _GoodWidgetState extends State<GoodWidget> {
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer(const Duration(seconds: 5), () {
      if (mounted) setState(() {});   // Check mounted!
    });
  }

  @override
  void dispose() {
    _timer?.cancel();   // Cancel pending operations
    super.dispose();
  }
}

// PITFALL 2: const widgets - HUGE performance win
// BAD - creates new widget tree on every rebuild
Widget build(BuildContext context) {
  return Container(
    padding: EdgeInsets.all(16),
    child: Text('Static text'),
  );
}

// GOOD - widgets are constant, reused
Widget build(BuildContext context) {
  return const Container(
    padding: EdgeInsets.all(16),
    child: Text('Static text'),
  );
}

// PITFALL 3: Building heavy widgets in loops
// BAD - filters items every rebuild
Widget build(BuildContext context) {
  final filtered = items.where((i) => i.isActive).toList();   // Every rebuild!
  return ListView(children: filtered.map((i) => ItemCard(item: i)).toList());
}

// GOOD - cache filtered list
class _MyWidgetState extends State<MyWidget> {
  late List<Item> _filtered;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _filtered = widget.items.where((i) => i.isActive).toList();
  }

  @override
  Widget build(BuildContext context) {
    return ListView(children: _filtered.map((i) => ItemCard(item: i)).toList());
  }
}

// PITFALL 4: Using ListView with hundreds of items
// BAD - builds all at once
ListView(children: items.map((i) => ItemCard(item: i)).toList())

// GOOD - lazy build
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, i) => ItemCard(item: items[i]),
)

// PITFALL 5: Forgetting to dispose controllers
class _BadState extends State<Bad> {
  final TextEditingController _controller = TextEditingController();
  // Never disposed - memory leak!
}

class _GoodState extends State<Good> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

// PITFALL 6: Async gaps without mounted check
Future<void> _loadData() async {
  final data = await api.fetch();
  // After await, widget might be disposed!
  if (!mounted) return;
  setState(() => _data = data);
}

// PITFALL 7: Rebuilding entire screen on small state change
// BAD - Setting state at top level rebuilds everything
class _BadScreen extends State<BadScreen> {
  int _count = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(children: [
        ExpensiveWidget(),   // Rebuilds when _count changes!
        Text('$_count'),
        ElevatedButton(onPressed: () => setState(() => _count++), child: Text('+')),
      ]),
    );
  }
}

// GOOD - Isolate state in smallest possible widget
class GoodScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(children: [
        const ExpensiveWidget(),   // No rebuild
        const CounterWidget(),     // Only this rebuilds
      ]),
    );
  }
}
```
