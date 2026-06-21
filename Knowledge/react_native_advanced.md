# React Native Advanced Reference


---

# CHAPTER 1: GETTING STARTED WITH REACT NATIVE


## Remarks

React Native is a framework by Meta for building native mobile apps using JavaScript/TypeScript and React. It compiles to native UI components (not WebViews), giving near-native performance. Used by Instagram, Discord, Shopify, Tesla, Coinbase.

Two architectures exist: **Old (Bridge)** — async JSON messages between JS and native. **New (Fabric + TurboModules)** — synchronous, type-safe, JSI-based. New Architecture is default from RN 0.76+.

Tools: Expo (managed workflow, easiest), React Native CLI (full control), Metro (bundler), Flipper/React DevTools (debugging), Reanimated 3 (60fps animations), Hermes (JS engine).


## Project Setup

```bash
# Expo (easiest, recommended for most apps)
npx create-expo-app@latest MyApp --template
cd MyApp
npx expo start

# React Native CLI (more control, native modules access)
npx @react-native-community/cli@latest init MyApp
cd MyApp
npm run ios       # or: npm run android

# TypeScript template (recommended)
npx create-expo-app@latest MyApp -t expo-template-blank-typescript
```


---

# CHAPTER 2: FUNCTIONAL COMPONENTS AND HOOKS


## Component Fundamentals

```tsx
// Basic functional component with TypeScript
import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { View, Text, TextInput, Button, StyleSheet, FlatList } from 'react-native';

interface Props {
  title: string;
  onSubmit?: (value: string) => void;
}

const MyComponent: React.FC<Props> = ({ title, onSubmit }) => {
  // useState — local state
  const [count, setCount] = useState<number>(0);
  const [text, setText] = useState<string>('');
  const [items, setItems] = useState<string[]>([]);

  // useRef — mutable ref that does NOT trigger re-render
  const inputRef = useRef<TextInput>(null);
  const renderCount = useRef<number>(0);

  // useEffect — side effects (mount, update, cleanup)
  useEffect(() => {
    console.log('Mounted or count changed:', count);
    return () => {
      console.log('Cleanup before next effect or unmount');
    };
  }, [count]);  // Runs only when count changes

  // useEffect with empty deps — mount only
  useEffect(() => {
    const timer = setInterval(() => {
      renderCount.current += 1;
    }, 1000);
    return () => clearInterval(timer);  // Cleanup on unmount
  }, []);

  // useCallback — memoize callback (prevents child re-renders)
  const handleAdd = useCallback(() => {
    setItems(prev => [...prev, text]);
    setText('');
    inputRef.current?.focus();
  }, [text]);

  // useMemo — memoize expensive computation
  const sortedItems = useMemo(() => {
    return [...items].sort();
  }, [items]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <Text>Count: {count}</Text>
      <Button title="Increment" onPress={() => setCount(c => c + 1)} />

      <TextInput
        ref={inputRef}
        style={styles.input}
        value={text}
        onChangeText={setText}
        placeholder="Enter item"
      />
      <Button title="Add" onPress={handleAdd} />

      <FlatList
        data={sortedItems}
        keyExtractor={(item, idx) => `${item}-${idx}`}
        renderItem={({ item }) => <Text>{item}</Text>}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold' },
  input: { borderWidth: 1, padding: 8, marginVertical: 8 },
});

export default MyComponent;
```


## Custom Hooks

```tsx
// useDebounce.ts - debounce any value
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debounced;
}

// useFetch.ts - generic data fetching
import { useState, useEffect } from 'react';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useFetch<T>(url: string, deps: unknown[] = []): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState(s => ({ ...s, loading: true, error: null }));

    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        if (!cancelled) setState({ data, loading: false, error: null });
      })
      .catch(error => {
        if (!cancelled) setState({ data: null, loading: false, error });
      });

    return () => { cancelled = true; };
  }, [url, ...deps]);

  return state;
}

// useToggle.ts - boolean toggle
import { useState, useCallback } from 'react';

export function useToggle(initial: boolean = false): [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle];
}

// useKeyboard.ts - track keyboard state
import { useEffect, useState } from 'react';
import { Keyboard, KeyboardEvent } from 'react-native';

export function useKeyboard() {
  const [visible, setVisible] = useState(false);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    const showSub = Keyboard.addListener('keyboardDidShow', (e: KeyboardEvent) => {
      setVisible(true);
      setHeight(e.endCoordinates.height);
    });
    const hideSub = Keyboard.addListener('keyboardDidHide', () => {
      setVisible(false);
      setHeight(0);
    });
    return () => {
      showSub.remove();
      hideSub.remove();
    };
  }, []);

  return { visible, height };
}

// Usage of custom hooks
function SearchScreen() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  const { data, loading, error } = useFetch<Item[]>(
    `https://api.example.com/search?q=${debouncedQuery}`,
    [debouncedQuery]
  );

  // Auto-search when typing stops for 300ms
  return <SearchUI query={query} onChange={setQuery} results={data} />;
}
```


---

# CHAPTER 3: NAVIGATION WITH REACT NAVIGATION


## Stack, Tabs, Drawer

```tsx
// Install:
// npm install @react-navigation/native @react-navigation/native-stack
// npm install @react-navigation/bottom-tabs @react-navigation/drawer
// npm install react-native-screens react-native-safe-area-context
// npm install react-native-gesture-handler react-native-reanimated

// App.tsx
import 'react-native-gesture-handler';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer';

// Type-safe navigation params
type RootStackParamList = {
  Home: undefined;                          // No params
  Profile: { userId: string };              // Required param
  Settings: { tab?: 'general' | 'privacy' }; // Optional param
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();
const Drawer = createDrawerNavigator();

// Tabs at bottom
function HomeTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ color, size }) => {
          // Return Icon based on route.name
          return null;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}
    >
      <Tab.Screen name="Feed" component={FeedScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Notifications" component={NotificationsScreen} />
    </Tab.Navigator>
  );
}

// Root stack
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#007AFF' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeTabs}
          options={{ title: 'Home', headerShown: false }}
        />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={({ route }) => ({
            title: `User ${route.params.userId}`,
            presentation: 'modal',
          })}
        />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Type-safe navigation in components
import { NativeStackScreenProps } from '@react-navigation/native-stack';
type ProfileProps = NativeStackScreenProps<RootStackParamList, 'Profile'>;

function ProfileScreen({ navigation, route }: ProfileProps) {
  const { userId } = route.params;  // Type-checked!

  return (
    <View>
      <Text>User ID: {userId}</Text>
      <Button
        title="Go to Settings"
        onPress={() => navigation.navigate('Settings', { tab: 'privacy' })}
      />
      <Button title="Go Back" onPress={() => navigation.goBack()} />
      <Button
        title="Reset to Home"
        onPress={() => navigation.reset({ index: 0, routes: [{ name: 'Home' }] })}
      />
    </View>
  );
}
```


## Deep Linking

```tsx
// Configure deep links to open specific screens from URLs
// Example: myapp://profile/123 or https://myapp.com/profile/123

import { LinkingOptions } from '@react-navigation/native';

const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: '',
      Profile: 'profile/:userId',
      Settings: 'settings/:tab?',
    },
  },
  // Custom getInitialURL — for cold starts from notification
  async getInitialURL() {
    const url = await Linking.getInitialURL();
    if (url) return url;
    // Check notification
    const message = await messaging().getInitialNotification();
    return message?.data?.url ?? null;
  },
  subscribe(listener) {
    const sub = Linking.addEventListener('url', ({ url }) => listener(url));
    return () => sub.remove();
  },
};

<NavigationContainer linking={linking} fallback={<Loading />}>
  {/* ... */}
</NavigationContainer>
```


---

# CHAPTER 4: STATE MANAGEMENT


## Context API for Simple Global State

```tsx
// AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore session on mount
  useEffect(() => {
    AsyncStorage.getItem('user').then(stored => {
      if (stored) setUser(JSON.parse(stored));
      setIsLoading(false);
    });
  }, []);

  const login = async (email: string, password: string) => {
    const response = await fetch('https://api.example.com/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error('Login failed');
    const userData: User = await response.json();
    await AsyncStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = async () => {
    await AsyncStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use context safely
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

// Usage in App.tsx
function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <RootNavigator />
      </NavigationContainer>
    </AuthProvider>
  );
}

// Usage in screen
function LoginScreen() {
  const { login } = useAuth();
  // ...
}
```


## Zustand — Lightweight Global Store

```tsx
// store.ts - npm install zustand
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  total: number;

  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clear: () => void;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      total: 0,

      addItem: (newItem) => set((state) => {
        const existing = state.items.find(i => i.id === newItem.id);
        const items = existing
          ? state.items.map(i =>
              i.id === newItem.id
                ? { ...i, quantity: i.quantity + 1 }
                : i
            )
          : [...state.items, { ...newItem, quantity: 1 }];
        const total = items.reduce((s, i) => s + i.price * i.quantity, 0);
        return { items, total };
      }),

      removeItem: (id) => set((state) => {
        const items = state.items.filter(i => i.id !== id);
        const total = items.reduce((s, i) => s + i.price * i.quantity, 0);
        return { items, total };
      }),

      updateQuantity: (id, quantity) => set((state) => {
        if (quantity <= 0) {
          return { items: state.items.filter(i => i.id !== id) };
        }
        const items = state.items.map(i =>
          i.id === id ? { ...i, quantity } : i
        );
        const total = items.reduce((s, i) => s + i.price * i.quantity, 0);
        return { items, total };
      }),

      clear: () => set({ items: [], total: 0 }),
    }),
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Usage in components — select only what you need (prevents re-renders)
function CartScreen() {
  // Subscribe to specific slices
  const items = useCartStore(s => s.items);
  const total = useCartStore(s => s.total);
  const removeItem = useCartStore(s => s.removeItem);

  return (
    <FlatList
      data={items}
      keyExtractor={item => item.id}
      renderItem={({ item }) => (
        <CartRow item={item} onRemove={() => removeItem(item.id)} />
      )}
      ListFooterComponent={<Text>Total: ${total.toFixed(2)}</Text>}
    />
  );
}
```


## Redux Toolkit (RTK) — Heavy Apps

```tsx
// store/index.ts - npm install @reduxjs/toolkit react-redux
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import cartReducer from './cartSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
  },
  middleware: (getDefault) => getDefault({
    serializableCheck: { ignoredActions: ['persist/PERSIST'] },
  }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// store/authSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  user: User | null;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: AuthState = { user: null, status: 'idle', error: null };

// Async thunk for API call
export const loginUser = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }) => {
    const response = await fetch('https://api.example.com/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error('Login failed');
    return (await response.json()) as User;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.status = 'idle';
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(loginUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.status = 'succeeded';
        state.user = action.payload;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message ?? 'Login failed';
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;

// Usage with type-safe hooks
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

function LoginScreen() {
  const dispatch = useAppDispatch();
  const { status, error } = useAppSelector(s => s.auth);

  const handleLogin = async () => {
    const result = await dispatch(loginUser({ email, password }));
    if (loginUser.fulfilled.match(result)) {
      navigation.navigate('Home');
    }
  };
}
```


---

# CHAPTER 5: NETWORKING AND ASYNC


## Fetch, Axios, TanStack Query

```tsx
// Plain fetch with proper error handling
async function getUser(id: string): Promise<User> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);  // 10s timeout

  try {
    const response = await fetch(`https://api.example.com/users/${id}`, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request timeout');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Axios - more features, interceptors, auto-JSON
// npm install axios
import axios, { AxiosInstance, AxiosError } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor - add token to every request
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - auto-refresh expired tokens
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config;
    if (error.response?.status === 401 && !original?.headers['X-Retry']) {
      // Token expired - refresh and retry
      try {
        const newToken = await refreshToken();
        await AsyncStorage.setItem('token', newToken);
        original!.headers['X-Retry'] = 'true';
        original!.headers.Authorization = `Bearer ${newToken}`;
        return api(original!);
      } catch {
        // Refresh failed - logout
        await AsyncStorage.removeItem('token');
        // Navigate to login
      }
    }
    return Promise.reject(error);
  }
);

// Usage
const { data } = await api.get<User>(`/users/${id}`);
await api.post('/posts', { title, body });
```


## TanStack Query (formerly React Query)

```tsx
// npm install @tanstack/react-query
// Best for caching, refetching, mutations, optimistic updates

import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5 min
      retry: 2,
      refetchOnWindowFocus: false,      // Not relevant in RN
    },
  },
});

// Wrap app
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>

// Query - fetch data
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.get<User>(`/users/${userId}`).then(r => r.data),
    enabled: !!userId,  // Skip if no ID
  });

  if (isLoading) return <ActivityIndicator />;
  if (error) return <Text>Error: {error.message}</Text>;
  return <UserCard user={data!} onRefresh={refetch} />;
}

// Mutation - modify data
function CreatePostForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newPost: NewPost) =>
      api.post<Post>('/posts', newPost).then(r => r.data),

    // Optimistic update - update UI before API responds
    onMutate: async (newPost) => {
      await queryClient.cancelQueries({ queryKey: ['posts'] });
      const previous = queryClient.getQueryData<Post[]>(['posts']);
      queryClient.setQueryData<Post[]>(['posts'], (old = []) => [
        { ...newPost, id: 'temp-' + Date.now(), createdAt: new Date() },
        ...old,
      ]);
      return { previous };
    },
    onError: (err, newPost, context) => {
      // Rollback on error
      if (context?.previous) {
        queryClient.setQueryData(['posts'], context.previous);
      }
    },
    onSettled: () => {
      // Always refetch after settling
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  return (
    <Button
      title={mutation.isPending ? 'Posting...' : 'Post'}
      disabled={mutation.isPending}
      onPress={() => mutation.mutate({ title, body })}
    />
  );
}

// Infinite scroll
function InfiniteFeed() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ['feed'],
    queryFn: ({ pageParam = 1 }) =>
      api.get(`/posts?page=${pageParam}`).then(r => r.data),
    getNextPageParam: (lastPage, allPages) =>
      lastPage.hasMore ? allPages.length + 1 : undefined,
    initialPageParam: 1,
  });

  const items = data?.pages.flatMap(p => p.items) ?? [];

  return (
    <FlatList
      data={items}
      onEndReached={() => hasNextPage && !isFetchingNextPage && fetchNextPage()}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
      renderItem={({ item }) => <PostCard post={item} />}
    />
  );
}
```


---

# CHAPTER 6: PERFORMANCE OPTIMIZATION


## FlatList Optimization

```tsx
// SLOW FlatList - common mistakes
<FlatList
  data={hugeData}
  renderItem={({ item }) => <ExpensiveRow data={item} />}  // Not memoized
  keyExtractor={(item, index) => index.toString()}          // Bad - index!
/>

// FAST FlatList - all optimizations
import React, { memo, useCallback } from 'react';

// 1. Memoize the row component
const Row = memo(({ data }: { data: Item }) => (
  <View style={styles.row}>
    <Text>{data.title}</Text>
  </View>
), (prev, next) => prev.data.id === next.data.id && prev.data.updatedAt === next.data.updatedAt);

function OptimizedList({ items }: { items: Item[] }) {
  // 2. Stable renderItem reference
  const renderItem = useCallback(({ item }: { item: Item }) => (
    <Row data={item} />
  ), []);

  // 3. Stable keyExtractor - use unique ID
  const keyExtractor = useCallback((item: Item) => item.id, []);

  // 4. getItemLayout - if rows have fixed height, skip measurement
  const getItemLayout = useCallback((_: unknown, index: number) => ({
    length: ROW_HEIGHT,
    offset: ROW_HEIGHT * index,
    index,
  }), []);

  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout}

      // 5. Window size - how many viewports to render around current
      windowSize={5}                     // Default 21, try 5-10
      maxToRenderPerBatch={10}            // Default 10
      updateCellsBatchingPeriod={50}      // Default 50ms
      initialNumToRender={10}             // Default 10
      removeClippedSubviews={true}        // Detach offscreen views

      // 6. For very long lists - turn off scroll throttling
      scrollEventThrottle={16}            // 60fps
    />
  );
}

const ROW_HEIGHT = 80;
```


## React.memo, useMemo, useCallback

```tsx
// React.memo - skip re-render if props haven't changed
const UserCard = memo<UserCardProps>(({ user, onPress }) => {
  console.log('UserCard render:', user.id);
  return (
    <Pressable onPress={() => onPress(user.id)}>
      <Text>{user.name}</Text>
    </Pressable>
  );
});

// Custom comparison function for deep equality
const ExpensiveChart = memo<{ data: number[] }>(
  ({ data }) => <Chart data={data} />,
  (prev, next) => {
    if (prev.data.length !== next.data.length) return false;
    return prev.data.every((v, i) => v === next.data[i]);
  }
);

// useMemo - cache expensive computations
function Statistics({ items }: { items: Item[] }) {
  // BAD - recalculated on every render
  const total = items.reduce((s, i) => s + i.value, 0);

  // GOOD - cached until items change
  const stats = useMemo(() => {
    const total = items.reduce((s, i) => s + i.value, 0);
    const avg = total / items.length;
    const max = Math.max(...items.map(i => i.value));
    const min = Math.min(...items.map(i => i.value));
    return { total, avg, max, min };
  }, [items]);

  return <StatsView {...stats} />;
}

// useCallback - cache function references for child memo'd components
function Parent() {
  const [count, setCount] = useState(0);

  // BAD - new function every render, breaks memo
  const handleClick = () => setCount(c => c + 1);

  // GOOD - stable reference
  const handleClick = useCallback(() => setCount(c => c + 1), []);

  return <MemoizedChild onClick={handleClick} />;
}
```


## Hermes Engine and Bundle Size

```tsx
// Enable Hermes for 30%+ smaller memory + faster startup
// android/gradle.properties
hermesEnabled=true

// ios/Podfile
:hermes_enabled => true

// Check if Hermes is active at runtime
if (global.HermesInternal != null) {
  console.log('Running on Hermes');
}

// Reduce bundle size:
// 1. Avoid moment.js - use date-fns (tree-shakeable) or Day.js
// 2. Avoid full lodash - import specific: import debounce from 'lodash/debounce'
// 3. Use react-native-svg instead of importing PNG @1x/@2x/@3x
// 4. Enable Proguard for Android (android/app/proguard-rules.pro)
// 5. Use Hermes - smaller runtime than JSC
// 6. Code splitting with React.lazy() + dynamic imports

// Analyze bundle
// npx react-native-bundle-visualizer
```


---

# CHAPTER 7: ANIMATIONS WITH REANIMATED 3


## UI Thread Animations at 60fps

```tsx
// npm install react-native-reanimated
// Animations run on UI thread - never blocked by JS work

import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  withRepeat,
  withSequence,
  runOnJS,
  interpolate,
  Easing,
} from 'react-native-reanimated';

// Basic spring animation
function BouncyBox() {
  const offset = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: offset.value }],
  }));

  const handlePress = () => {
    offset.value = withSpring(Math.random() * 200, {
      damping: 12,
      stiffness: 100,
    });
  };

  return (
    <>
      <Animated.View style={[styles.box, animatedStyle]} />
      <Button title="Move" onPress={handlePress} />
    </>
  );
}

// Sequenced + Repeated
function HeartbeatIcon() {
  const scale = useSharedValue(1);

  useEffect(() => {
    scale.value = withRepeat(
      withSequence(
        withTiming(1.3, { duration: 300, easing: Easing.out(Easing.cubic) }),
        withTiming(1.0, { duration: 300 })
      ),
      -1,  // -1 = infinite repeat
      false
    );
  }, []);

  const style = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return <Animated.Image source={heartImage} style={[styles.heart, style]} />;
}

// Interpolation for complex effects
function FadeScrollHeader({ scrollY }: { scrollY: Animated.SharedValue<number> }) {
  const headerStyle = useAnimatedStyle(() => {
    const opacity = interpolate(
      scrollY.value,
      [0, 50, 100],     // input range
      [1, 0.5, 0],       // output range
      'clamp'            // don't extrapolate
    );
    const translateY = interpolate(
      scrollY.value,
      [0, 100],
      [0, -50],
      'clamp'
    );
    return {
      opacity,
      transform: [{ translateY }],
    };
  });

  return <Animated.View style={[styles.header, headerStyle]} />;
}

// Gesture-driven animation with Reanimated + Gesture Handler
import { GestureDetector, Gesture } from 'react-native-gesture-handler';

function DraggableCard() {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);

  const gesture = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
      translateY.value = e.translationY;
    })
    .onEnd(() => {
      // Snap back to origin with spring
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={[styles.card, animatedStyle]} />
    </GestureDetector>
  );
}

// runOnJS - call JS functions from worklets
function SwipeToDelete({ item, onDelete }: { item: Item; onDelete: () => void }) {
  const translateX = useSharedValue(0);

  const gesture = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
    })
    .onEnd(() => {
      if (translateX.value < -100) {
        translateX.value = withTiming(-500);
        runOnJS(onDelete)();   // Call JS callback from worklet
      } else {
        translateX.value = withSpring(0);
      }
    });

  // ...
}
```


---

# CHAPTER 8: NATIVE MODULES AND DEVICE APIS


## Accessing Native Features

```tsx
// Most common APIs via Expo / community packages

// CAMERA - expo-camera
import { CameraView, useCameraPermissions } from 'expo-camera';

function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  if (!permission?.granted) {
    return <Button title="Grant camera" onPress={requestPermission} />;
  }

  const takePicture = async () => {
    const photo = await cameraRef.current?.takePictureAsync({
      quality: 0.8,
      base64: false,
    });
    console.log('Photo:', photo?.uri);
  };

  return (
    <CameraView ref={cameraRef} style={{ flex: 1 }} facing="back">
      <Button title="Capture" onPress={takePicture} />
    </CameraView>
  );
}

// LOCATION - expo-location
import * as Location from 'expo-location';

async function getLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') throw new Error('Permission denied');

  const location = await Location.getCurrentPositionAsync({
    accuracy: Location.Accuracy.High,
  });
  return { lat: location.coords.latitude, lng: location.coords.longitude };
}

// Watch position - continuous updates
useEffect(() => {
  let subscription: Location.LocationSubscription;
  (async () => {
    subscription = await Location.watchPositionAsync(
      { accuracy: Location.Accuracy.High, distanceInterval: 10 },
      (loc) => setPosition(loc.coords)
    );
  })();
  return () => subscription?.remove();
}, []);

// PUSH NOTIFICATIONS - expo-notifications
import * as Notifications from 'expo-notifications';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

async function registerForPushNotifications(): Promise<string | null> {
  const { status: existing } = await Notifications.getPermissionsAsync();
  let finalStatus = existing;
  if (existing !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }
  if (finalStatus !== 'granted') return null;

  const token = (await Notifications.getExpoPushTokenAsync()).data;
  return token;  // Send to your backend
}

// Handle incoming notifications
useEffect(() => {
  const sub = Notifications.addNotificationReceivedListener(notification => {
    console.log('Received:', notification);
  });
  const tapSub = Notifications.addNotificationResponseReceivedListener(response => {
    const url = response.notification.request.content.data.url;
    if (url) Linking.openURL(url as string);
  });
  return () => {
    sub.remove();
    tapSub.remove();
  };
}, []);

// STORAGE - SecureStore for tokens, AsyncStorage for data
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

// SecureStore - encrypted, max 2KB per value (use for tokens)
await SecureStore.setItemAsync('auth_token', token);
const token = await SecureStore.getItemAsync('auth_token');
await SecureStore.deleteItemAsync('auth_token');

// AsyncStorage - unencrypted, larger storage (use for cache/prefs)
await AsyncStorage.setItem('theme', 'dark');
const theme = await AsyncStorage.getItem('theme');

// BIOMETRICS - expo-local-authentication
import * as LocalAuthentication from 'expo-local-authentication';

async function authenticateUser() {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  if (!hasHardware || !isEnrolled) return false;

  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Unlock app',
    fallbackLabel: 'Use passcode',
  });
  return result.success;
}
```


---

# CHAPTER 9: TESTING


## Unit, Integration, E2E

```tsx
// Unit tests with Jest + React Native Testing Library
// npm install --save-dev @testing-library/react-native jest

// Counter.tsx
import { Button, Text, View } from 'react-native';
import { useState } from 'react';

export function Counter({ initial = 0 }: { initial?: number }) {
  const [count, setCount] = useState(initial);
  return (
    <View>
      <Text testID="count">{count}</Text>
      <Button title="Increment" onPress={() => setCount(c => c + 1)} />
    </View>
  );
}

// Counter.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { Counter } from './Counter';

describe('Counter', () => {
  it('renders initial value', () => {
    const { getByTestId } = render(<Counter initial={5} />);
    expect(getByTestId('count').props.children).toBe(5);
  });

  it('increments on button press', () => {
    const { getByTestId, getByText } = render(<Counter />);
    expect(getByTestId('count').props.children).toBe(0);

    fireEvent.press(getByText('Increment'));
    expect(getByTestId('count').props.children).toBe(1);

    fireEvent.press(getByText('Increment'));
    fireEvent.press(getByText('Increment'));
    expect(getByTestId('count').props.children).toBe(3);
  });
});

// Mocking
jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
}));

// Async testing
it('loads user from storage', async () => {
  (AsyncStorage.getItem as jest.Mock).mockResolvedValue(
    JSON.stringify({ id: '1', name: 'Alice' })
  );

  const { findByText } = render(<UserProfile />);
  expect(await findByText('Alice')).toBeTruthy();
});

// E2E with Detox
// detox.config.js + detox test
describe('Login flow', () => {
  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should log in successfully', async () => {
    await element(by.id('email')).typeText('user@example.com');
    await element(by.id('password')).typeText('pass123');
    await element(by.id('submit')).tap();

    await expect(element(by.text('Welcome'))).toBeVisible();
  });
});
```


---

# CHAPTER 10: PRODUCTION TIPS


## Crash Reporting and Analytics

```tsx
// Sentry for crashes
// npx @sentry/wizard@latest -i reactNative
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://...@sentry.io/...',
  enableAutoSessionTracking: true,
  tracesSampleRate: 0.2,
  beforeSend(event, hint) {
    // Filter sensitive data
    if (event.user) delete event.user.email;
    return event;
  },
});

// Catch errors
try {
  await riskyOperation();
} catch (e) {
  Sentry.captureException(e);
  throw e;  // Re-throw for boundary
}

// Performance monitoring
const transaction = Sentry.startTransaction({ name: 'CheckoutFlow' });
await processPayment();
transaction.finish();

// Error boundary - catch render errors
class ErrorBoundary extends React.Component<{ children: ReactNode }, { hasError: boolean }> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    Sentry.captureException(error, { extra: info });
  }

  render() {
    if (this.state.hasError) {
      return (
        <View>
          <Text>Something went wrong</Text>
          <Button title="Retry" onPress={() => this.setState({ hasError: false })} />
        </View>
      );
    }
    return this.props.children;
  }
}
```


## Build Configurations and Code Push

```tsx
// Environment configs - npm install react-native-config
// .env.development
API_URL=https://dev-api.example.com
ENABLE_LOGS=true

// .env.production
API_URL=https://api.example.com
ENABLE_LOGS=false

// Usage
import Config from 'react-native-config';
const url = Config.API_URL;

// OTA updates - Expo EAS Update (no app store review needed for JS-only)
// eas update --branch production --message "Bug fixes"
import * as Updates from 'expo-updates';

useEffect(() => {
  (async () => {
    if (__DEV__) return;
    try {
      const update = await Updates.checkForUpdateAsync();
      if (update.isAvailable) {
        await Updates.fetchUpdateAsync();
        await Updates.reloadAsync();   // Restart with new bundle
      }
    } catch {}
  })();
}, []);

// Feature flags
const FEATURES = {
  newCheckout: __DEV__ || Config.ENABLE_NEW_CHECKOUT === 'true',
  darkMode: true,
};

if (FEATURES.newCheckout) {
  return <NewCheckoutFlow />;
}
return <LegacyCheckout />;
```


## Common Pitfalls

```tsx
// PITFALL 1: Stale closures in useEffect
function BadCounter() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setCount(count + 1);  // Always 0+1 - stale closure!
    }, 1000);
    return () => clearInterval(id);
  }, []);  // Missing 'count' dependency
}

function GoodCounter() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1);  // Use functional update - always current
    }, 1000);
    return () => clearInterval(id);
  }, []);  // No dependency needed
}

// PITFALL 2: Memory leaks - not cleaning up
function BadComponent() {
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData);
    // No cleanup - setData may be called after unmount = warning
  }, []);
}

function GoodComponent() {
  useEffect(() => {
    let cancelled = false;
    fetch('/api/data').then(r => r.json()).then(data => {
      if (!cancelled) setData(data);
    });
    return () => { cancelled = true; };
  }, []);
}

// PITFALL 3: Object/array recreated every render = breaks memo
function BadParent() {
  return <ChildMemo config={{ timeout: 5000 }} />;  // New object every render!
}

function GoodParent() {
  const config = useMemo(() => ({ timeout: 5000 }), []);
  return <ChildMemo config={config} />;
}

// PITFALL 4: Index as key in lists
items.map((item, i) => <Row key={i} {...item} />)  // BAD if items reorder

items.map(item => <Row key={item.id} {...item} />)  // GOOD - stable

// PITFALL 5: Inline styles defeating StyleSheet optimization
<View style={{ padding: 16, backgroundColor: 'red' }}>  // New object every render

const styles = StyleSheet.create({ box: { padding: 16, backgroundColor: 'red' } });
<View style={styles.box}>  // Stable reference, cached
```
