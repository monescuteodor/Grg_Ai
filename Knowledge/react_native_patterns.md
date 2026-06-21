# React Native Production Patterns Complete Reference


---

# CHAPTER 1: APP ARCHITECTURE


## Remarks

This reference focuses on **production patterns** for React Native apps — beyond the basics covered in `react_native_advanced.md`. Topics include scalable folder structure, architecture patterns, state management at scale, performance optimization for 60fps, offline-first apps, and patterns from production apps (Discord, Coinbase, Shopify, Facebook).

Key concepts: **Feature-based architecture**, **Atomic Design**, **Container/Presentational components**, **Custom hooks for logic**, **Offline-first** (TanStack Query, MMKV), **Optimistic updates**, **Performance** (FlashList, Reanimated 3, Hermes), **Type safety** (TypeScript strict), **Error boundaries**, **Code splitting**, **A/B testing**.

Used by: Discord, Coinbase, Shopify Shop, Facebook, Instagram, Walmart, Uber Eats, Pinterest — many of the largest mobile apps.

Tools: **TypeScript** (essentially required at scale), **React Query / TanStack Query** (server state), **Zustand / Jotai** (client state), **react-hook-form + Zod** (forms), **Reanimated 3** (animations), **FlashList** (Shopify, replaces FlatList), **MMKV** (fast storage), **Sentry** (error tracking), **Detox** (E2E tests).


## Scalable Folder Structure

```
src/
├── app/                          # Navigation, root setup
│   ├── _layout.tsx               # Root layout (Expo Router) or App.tsx
│   ├── navigation/
│   └── providers/                # Compose all providers
│       └── AppProviders.tsx
│
├── features/                     # Feature-based organization (BEST)
│   ├── auth/
│   │   ├── api/                  # API calls for this feature
│   │   ├── components/           # UI components specific to auth
│   │   ├── hooks/                # useLogin, useRegister, etc.
│   │   ├── screens/              # LoginScreen, RegisterScreen
│   │   ├── stores/               # authStore (Zustand)
│   │   ├── types.ts              # Feature-specific types
│   │   └── index.ts              # Public exports
│   │
│   ├── profile/
│   ├── feed/
│   ├── chat/
│   └── settings/
│
├── shared/                       # Cross-feature code
│   ├── api/                      # Base API client (axios/fetch)
│   ├── components/               # Reusable UI (Button, Input, Card)
│   ├── hooks/                    # useDebounce, usePrevious
│   ├── lib/                      # Utils, helpers
│   ├── stores/                   # Global stores (theme, locale)
│   ├── theme/                    # Colors, spacing, typography
│   └── types/                    # Global types
│
├── assets/                       # Images, fonts, animations
│
└── config/                       # Env vars, constants
    └── env.ts

# Why feature-based vs technical-layered?
# 
# BAD (technical layers):              GOOD (features):
#   components/                          features/
#     LoginForm.tsx                        auth/
#     ProfileCard.tsx                      profile/
#   screens/                               feed/
#     LoginScreen.tsx                    
#     ProfileScreen.tsx
#   hooks/
#     useLogin.ts
#     useProfile.ts
#
# Why features wins:
#   - When you change auth, all auth code in one folder
#   - Easy to delete a feature (delete folder)
#   - Easy onboarding (devs work on one feature at a time)
#   - Clear ownership boundaries
#   - Scales to 100+ devs
```


## Provider Composition Pattern

```typescript
// shared/providers/AppProviders.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ThemeProvider } from '@/shared/theme';
import { AuthProvider } from '@/features/auth';
import { ErrorBoundary } from '@/shared/components/ErrorBoundary';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,     // 5 min
      retry: 2,
      refetchOnWindowFocus: false,   // RN doesn't need this
    },
  },
});

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary>
      <SafeAreaProvider>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </ThemeProvider>
        </QueryClientProvider>
      </SafeAreaProvider>
    </ErrorBoundary>
  );
}

// In root component:
export default function App() {
  return (
    <AppProviders>
      <Navigation />
    </AppProviders>
  );
}

// Why this matters:
// - Single place to add/remove providers
// - Order matters! ErrorBoundary outside, hooks inside
// - Testing: mock specific providers easily
```


## Atomic Design for Components

```
ATOMS:        Smallest reusable parts
              Button, Input, Text, Icon, Avatar
              
MOLECULES:    Combinations of atoms with simple purpose
              SearchBar (Input + Icon), FormField (Label + Input + Error)
              
ORGANISMS:    Complex UI sections
              Header, ProductCard, ChatMessage
              
TEMPLATES:    Page layouts (no content)
              ScreenLayout, ModalLayout
              
SCREENS:      Full pages with data
              LoginScreen, ProfileScreen

EXAMPLE FOLDER:
  shared/components/
    atoms/
      Button/
        Button.tsx
        Button.test.tsx
        Button.types.ts
        index.ts
      Input/
      Text/
    molecules/
      SearchBar/
      FormField/
    organisms/
      Header/
      ProductCard/
```


---

# CHAPTER 2: STATE MANAGEMENT AT SCALE


## Server State vs Client State

```
TWO TYPES OF STATE:

SERVER STATE:
  Data that lives on the server.
  Examples: user profile, posts list, products
  Challenges: caching, refetching, sync with server, optimistic updates
  Tool: TanStack Query (formerly React Query) — DON'T put this in Redux!

CLIENT STATE:
  UI state that lives only in the app.
  Examples: modal open/closed, form values, selected tab, theme
  Tool: Zustand, Jotai, useState, or Context

ANTI-PATTERN: Putting server state in Redux/Zustand
  → Reinvents caching, refetching, error handling
  → Tons of boilerplate
  → Hard to invalidate

BEST PRACTICE: Use TanStack Query for server state, Zustand for client state.
```


## TanStack Query (Server State)

```typescript
// features/posts/api/postsApi.ts
import { apiClient } from '@/shared/api';

export interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  createdAt: string;
}

export const postsApi = {
  list: () => apiClient.get<Post[]>('/posts').then(r => r.data),
  get: (id: string) => apiClient.get<Post>(`/posts/${id}`).then(r => r.data),
  create: (data: Omit<Post, 'id' | 'createdAt'>) => 
    apiClient.post<Post>('/posts', data).then(r => r.data),
  update: (id: string, data: Partial<Post>) => 
    apiClient.patch<Post>(`/posts/${id}`, data).then(r => r.data),
  delete: (id: string) => apiClient.delete(`/posts/${id}`),
};


// features/posts/hooks/usePostsQuery.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postsApi, Post } from '../api/postsApi';

// Query keys factory (organized, type-safe)
export const postsKeys = {
  all: ['posts'] as const,
  lists: () => [...postsKeys.all, 'list'] as const,
  list: (filters?: object) => [...postsKeys.lists(), filters] as const,
  details: () => [...postsKeys.all, 'detail'] as const,
  detail: (id: string) => [...postsKeys.details(), id] as const,
};

// List posts
export function usePosts(filters?: { author?: string }) {
  return useQuery({
    queryKey: postsKeys.list(filters),
    queryFn: () => postsApi.list(),
    staleTime: 1000 * 60,    // Fresh for 1 min
  });
}

// Single post (with prefetch)
export function usePost(id: string) {
  return useQuery({
    queryKey: postsKeys.detail(id),
    queryFn: () => postsApi.get(id),
    enabled: !!id,
  });
}

// Create with optimistic update
export function useCreatePost() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: postsApi.create,
    
    // Optimistic update: add to list immediately
    onMutate: async (newPost) => {
      // Cancel in-flight queries
      await queryClient.cancelQueries({ queryKey: postsKeys.lists() });
      
      // Snapshot previous
      const previous = queryClient.getQueryData<Post[]>(postsKeys.list());
      
      // Optimistically add
      const tempPost: Post = {
        ...newPost,
        id: `temp-${Date.now()}`,
        createdAt: new Date().toISOString(),
      };
      
      queryClient.setQueryData<Post[]>(postsKeys.list(), (old = []) => 
        [tempPost, ...old]
      );
      
      return { previous };
    },
    
    // On error: rollback
    onError: (_err, _newPost, context) => {
      if (context?.previous) {
        queryClient.setQueryData(postsKeys.list(), context.previous);
      }
    },
    
    // After success/error: refetch to get real data
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: postsKeys.lists() });
    },
  });
}


// In screen
function FeedScreen() {
  const { data: posts, isLoading, error } = usePosts();
  const createMutation = useCreatePost();
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorView error={error} />;
  
  return (
    <FlashList
      data={posts}
      renderItem={({ item }) => <PostCard post={item} />}
      onEndReached={() => {/* pagination */}}
    />
  );
}
```


## Zustand (Client State)

```typescript
// features/auth/stores/authStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  // Actions (methods)
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: (user, token) => set({
        user,
        token,
        isAuthenticated: true,
      }),
      
      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false,
      }),
      
      updateUser: (updates) => set((state) => ({
        user: state.user ? { ...state.user, ...updates } : null,
      })),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Use in components (subscribe to specific slices)
function Header() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  
  return (
    <View>
      <Text>{user?.name}</Text>
      <Button onPress={logout} title="Logout" />
    </View>
  );
}

// Outside React (utils, API interceptors)
import { useAuthStore } from '@/features/auth/stores/authStore';

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Why Zustand wins for client state:
// - No boilerplate (vs Redux)
// - No Provider needed at root
// - Use outside React easily (.getState())
// - Tiny (~1KB)
// - Built-in persistence
// - Selective subscribing (avoid re-renders)
```


## Why NOT Redux for New Projects

```
Redux had its time. Modern alternatives are better:

PROBLEMS WITH REDUX:
  ❌ Lots of boilerplate (actions, reducers, thunks)
  ❌ Easy to put server state in (anti-pattern)
  ❌ Hard to scale without conventions (RTK helps but still verbose)
  ❌ Steep learning curve

EXCEPTIONS WHERE REDUX MAKES SENSE:
  - Existing large Redux codebase
  - Time-travel debugging needed
  - Complex undo/redo
  - Team already knows Redux deeply

FOR NEW PROJECTS:
  Server state:  TanStack Query
  Client state:  Zustand or Jotai
  Form state:    react-hook-form
  URL state:     React Navigation or Expo Router
```


---

# CHAPTER 3: PERFORMANCE OPTIMIZATION


## The 60fps Promise

```
60fps = 16.67ms per frame.
If a frame takes longer → drop frames → janky UI.

CAUSES OF SLOWNESS:
  1. Heavy JS computation on main thread
  2. Bridge calls (RN0.x architecture)
  3. Large lists rendered with FlatList
  4. Re-renders cascading
  5. Heavy synchronous work in render

NEW ARCHITECTURE (RN 0.76+):
  - Fabric (new renderer) — synchronous layout
  - TurboModules — lazy native modules
  - JSI (JavaScript Interface) — direct C++ ↔ JS, no bridge
  - Bridgeless mode

ENABLE NEW ARCHITECTURE (Expo SDK 51+ default):
  // app.json
  "experiments": {
    "newArchEnabled": true
  }
```


## Lists: FlashList over FlatList

```typescript
// FlashList by Shopify — 5-10x better performance than FlatList
import { FlashList } from "@shopify/flash-list";

function ProductList({ products }: { products: Product[] }) {
  return (
    <FlashList
      data={products}
      renderItem={({ item }) => <ProductCard product={item} />}
      estimatedItemSize={120}              // CRITICAL for performance
      keyExtractor={(item) => item.id}
      
      // For different item types
      getItemType={(item) => item.type}    // 'product' | 'ad' | 'banner'
      
      // Pagination
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
      
      // Pull to refresh
      refreshing={isRefreshing}
      onRefresh={refresh}
      
      // Empty state
      ListEmptyComponent={<EmptyView />}
    />
  );
}

// Why FlashList beats FlatList:
//  - Recycles views aggressively (like RecyclerView on Android)
//  - Pre-allocates views
//  - No off-screen rendering
//  - Lower memory footprint
//  - Smoother scrolling on long lists

// IMPORTANT: estimatedItemSize must be ACCURATE
// If too small/large → blank areas during scroll
// Measure actual item height: View Profiler or hand-test
```


## Memoization Strategies

```typescript
// React.memo — prevent re-renders if props unchanged
const ProductCard = React.memo(({ product, onPress }: Props) => {
  return (
    <Pressable onPress={() => onPress(product.id)}>
      <Text>{product.name}</Text>
    </Pressable>
  );
});

// PROBLEM: function prop changes every render → memo useless
// SOLUTION: useCallback in parent

function ProductList({ products }: Props) {
  const handlePress = useCallback((id: string) => {
    navigate('Product', { id });
  }, []);   // Stable reference
  
  return (
    <FlashList
      data={products}
      renderItem={({ item }) => (
        <ProductCard product={item} onPress={handlePress} />
      )}
    />
  );
}

// useMemo — cache computed values
function FilteredList({ items, filter }: Props) {
  const filtered = useMemo(() => {
    return items.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);
  
  return <FlashList data={filtered} renderItem={...} />;
}

// RULE: Don't memoize everything!
// memo costs CPU to compare props. If component is cheap, just re-render.
// Profile first, then memoize bottlenecks.
```


## Reducing Re-renders

```typescript
// SYMPTOM: typing in one input re-renders entire screen

// BAD: parent component holds form state, all children re-render
function BadForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  
  return (
    <View>
      <TextInput value={name} onChangeText={setName} />
      <TextInput value={email} onChangeText={setEmail} />
      <TextInput value={phone} onChangeText={setPhone} />
      <ExpensiveComponent />   {/* Re-renders on every keystroke! */}
    </View>
  );
}

// GOOD: react-hook-form (uncontrolled inputs, only what needs renders)
import { useForm, Controller } from 'react-hook-form';

function GoodForm() {
  const { control, handleSubmit } = useForm();
  
  return (
    <View>
      <Controller
        control={control}
        name="name"
        render={({ field: { onChange, value } }) => (
          <TextInput value={value} onChangeText={onChange} />
        )}
      />
      {/* ... */}
      <ExpensiveComponent />   {/* Only renders once! */}
    </View>
  );
}

// Why react-hook-form is fast:
//  - Uses refs internally (uncontrolled)
//  - No re-render of parent on input changes
//  - Validation also doesn't re-render unless needed
//  - Tiny bundle (8KB)
```


## Image Optimization

```typescript
// Don't use Image — use expo-image (or fastimage)
import { Image } from 'expo-image';

<Image
  source={{ uri: 'https://example.com/photo.jpg' }}
  style={{ width: 200, height: 200 }}
  
  // Caching strategy
  cachePolicy="memory-disk"     // memory + disk cache
  
  // Progressive loading
  placeholder={blurhash}        // Show blurhash while loading
  transition={300}              // Fade in
  
  // Sizing
  contentFit="cover"
  
  // Pre-load (when you know they'll need it soon)
  // Image.prefetch(urls)
/>

// Generate blurhash (server-side) for placeholders
// https://blurha.sh/
// Tiny string represents image preview — instant blurry placeholder
```


## Avoiding Bridge Overhead (Animations)

```typescript
// Reanimated 3 — animations on UI thread (not bridge!)
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';

function AnimatedBox() {
  const scale = useSharedValue(1);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  return (
    <Animated.View style={[styles.box, animatedStyle]}>
      <Pressable
        onPressIn={() => { scale.value = withSpring(0.9); }}
        onPressOut={() => { scale.value = withSpring(1); }}
      >
        <Text>Press me</Text>
      </Pressable>
    </Animated.View>
  );
}

// Runs at 60fps even when JS is busy.
// vs Animated API (older) which goes through bridge.

// Gesture Handler (also UI thread)
import { GestureDetector, Gesture } from 'react-native-gesture-handler';

function Swipeable() {
  const translateX = useSharedValue(0);
  
  const pan = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
    })
    .onEnd(() => {
      translateX.value = withSpring(0);
    });
  
  const style = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));
  
  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={[styles.box, style]} />
    </GestureDetector>
  );
}
```


---

# CHAPTER 4: OFFLINE-FIRST


## Why Offline-First Matters

```
USERS EXPECT:
  - App opens instantly (don't wait for network)
  - Can read cached content offline
  - Actions queued and synced when online
  - No "spinner of doom"

BENEFITS:
  - Better UX (perceived performance)
  - Works in poor networks (3G, subway)
  - Reduces server load
  - Lower battery usage

CHALLENGES:
  - Cache invalidation
  - Conflict resolution (if server changed too)
  - Sync queue management
  - Storage limits
```


## MMKV — Fast Persistent Storage

```typescript
// MMKV by Tencent — 30x faster than AsyncStorage
// Synchronous (!), encrypted, type-safe
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV({
  id: 'user-storage',
  encryptionKey: 'optional-encryption-key',
});

// Synchronous API
storage.set('user.name', 'Alice');
storage.set('user.age', 30);
storage.set('user.isPremium', true);
storage.set('user.data', JSON.stringify({ /* ... */ }));

const name = storage.getString('user.name');
const age = storage.getNumber('user.age');
const isPremium = storage.getBoolean('user.isPremium');
const data = JSON.parse(storage.getString('user.data') ?? '{}');

// Delete
storage.delete('user.name');
storage.clearAll();

// Listen to changes
const listener = storage.addOnValueChangedListener((changedKey) => {
  console.log(`${changedKey} changed`);
});
// listener.remove(); when done

// Multiple instances for separation
const cacheStorage = new MMKV({ id: 'cache' });
const settingsStorage = new MMKV({ id: 'settings' });
```


## TanStack Query Persistence

```typescript
// Persist React Query cache to MMKV
import { QueryClient } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

const persister = createSyncStoragePersister({
  storage: {
    getItem: (key) => storage.getString(key) ?? null,
    setItem: (key, value) => storage.set(key, value),
    removeItem: (key) => storage.delete(key),
  },
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24,   // 24h before garbage collection
      staleTime: 1000 * 60 * 5,       // 5 min fresh
    },
  },
});

export function AppProviders({ children }) {
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{ persister, maxAge: 1000 * 60 * 60 * 24 * 7 }}  // 7 days
    >
      {children}
    </PersistQueryClientProvider>
  );
}

// Result: queries restored from disk on app launch
// User sees data instantly, then background refetch
```


## NetInfo — Detect Connectivity

```typescript
import NetInfo from '@react-native-community/netinfo';

// One-shot check
const state = await NetInfo.fetch();
console.log('Connected:', state.isConnected);
console.log('Type:', state.type);   // 'wifi', 'cellular', 'none'

// Subscribe to changes
const unsubscribe = NetInfo.addEventListener(state => {
  console.log('Connection changed:', state.isConnected);
});

// Hook for components
function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  
  useEffect(() => {
    return NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? false);
    });
  }, []);
  
  return isOnline;
}

// Show banner when offline
function OfflineBanner() {
  const isOnline = useNetworkStatus();
  if (isOnline) return null;
  
  return (
    <View style={styles.offlineBanner}>
      <Text style={styles.offlineText}>You're offline</Text>
    </View>
  );
}
```


## Action Queue for Offline Writes

```typescript
// features/sync/actionQueue.ts
import { MMKV } from 'react-native-mmkv';

interface QueuedAction {
  id: string;
  type: string;
  payload: any;
  timestamp: number;
  retries: number;
}

const queueStorage = new MMKV({ id: 'action-queue' });

export const actionQueue = {
  add(action: Omit<QueuedAction, 'id' | 'timestamp' | 'retries'>) {
    const queued: QueuedAction = {
      ...action,
      id: `${Date.now()}-${Math.random()}`,
      timestamp: Date.now(),
      retries: 0,
    };
    const queue = this.getAll();
    queue.push(queued);
    queueStorage.set('queue', JSON.stringify(queue));
  },
  
  getAll(): QueuedAction[] {
    const raw = queueStorage.getString('queue');
    return raw ? JSON.parse(raw) : [];
  },
  
  remove(id: string) {
    const queue = this.getAll().filter(a => a.id !== id);
    queueStorage.set('queue', JSON.stringify(queue));
  },
  
  async processAll() {
    const queue = this.getAll();
    for (const action of queue) {
      try {
        await this.processAction(action);
        this.remove(action.id);
      } catch (err) {
        // Increment retry count, give up after N attempts
        action.retries++;
        if (action.retries >= 5) {
          this.remove(action.id);
          // Log permanent failure
        } else {
          this.update(action);
        }
      }
    }
  },
  
  update(action: QueuedAction) {
    const queue = this.getAll().map(a => a.id === action.id ? action : a);
    queueStorage.set('queue', JSON.stringify(queue));
  },
  
  async processAction(action: QueuedAction) {
    switch (action.type) {
      case 'CREATE_POST':
        await postsApi.create(action.payload);
        break;
      case 'UPDATE_PROFILE':
        await usersApi.update(action.payload.id, action.payload.data);
        break;
      // ...
    }
  },
};

// Hook to auto-process queue when online
export function useActionQueueSync() {
  const isOnline = useNetworkStatus();
  
  useEffect(() => {
    if (isOnline) {
      actionQueue.processAll();
    }
  }, [isOnline]);
}

// Usage: queue action when offline, process when back online
async function createPost(postData) {
  if (!isOnline) {
    actionQueue.add({ type: 'CREATE_POST', payload: postData });
    showToast('Will sync when online');
    return;
  }
  
  try {
    await postsApi.create(postData);
  } catch (err) {
    if (err.code === 'NETWORK_ERROR') {
      actionQueue.add({ type: 'CREATE_POST', payload: postData });
    }
    throw err;
  }
}
```


---

# CHAPTER 5: FORMS AT SCALE


## react-hook-form + Zod

```typescript
// Schema-first validation
import { z } from 'zod';

const RegisterSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z
    .string()
    .min(8, 'At least 8 characters')
    .regex(/[A-Z]/, 'At least one uppercase letter')
    .regex(/[0-9]/, 'At least one number'),
  confirmPassword: z.string(),
  name: z.string().min(1, 'Name required'),
  age: z.number().int().min(18, 'Must be 18 or older'),
  terms: z.literal(true, { errorMap: () => ({ message: 'Must accept terms' }) }),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof RegisterSchema>;

// Form component
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function RegisterForm() {
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<RegisterFormData>({
    resolver: zodResolver(RegisterSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      name: '',
      age: 18,
      terms: false,
    },
  });
  
  const onSubmit = async (data: RegisterFormData) => {
    try {
      await authApi.register(data);
      navigate('Home');
    } catch (err) {
      showError(err.message);
    }
  };
  
  return (
    <View>
      <Controller
        control={control}
        name="email"
        render={({ field }) => (
          <FormField
            label="Email"
            value={field.value}
            onChangeText={field.onChange}
            onBlur={field.onBlur}
            error={errors.email?.message}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        )}
      />
      
      <Controller
        control={control}
        name="password"
        render={({ field }) => (
          <FormField
            label="Password"
            value={field.value}
            onChangeText={field.onChange}
            secureTextEntry
            error={errors.password?.message}
          />
        )}
      />
      
      {/* ... other fields ... */}
      
      <Button
        title="Register"
        onPress={handleSubmit(onSubmit)}
        disabled={isSubmitting}
        loading={isSubmitting}
      />
    </View>
  );
}

// Reusable FormField molecule
interface FormFieldProps {
  label: string;
  error?: string;
  value: string;
  onChangeText: (text: string) => void;
  // ... TextInput props
}

function FormField({ label, error, ...props }: FormFieldProps) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[styles.input, error && styles.inputError]}
        {...props}
      />
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
}
```


---

# CHAPTER 6: NAVIGATION PATTERNS


## Expo Router (File-based, Modern)

```
File-based routing (like Next.js for RN):

app/
├── _layout.tsx               # Root layout (every screen wrapped)
├── index.tsx                 # /
├── login.tsx                 # /login
├── (tabs)/                   # Tab group (parens = not in URL)
│   ├── _layout.tsx           # Tab bar
│   ├── home.tsx              # /home (tab)
│   ├── search.tsx            # /search (tab)
│   └── profile.tsx           # /profile (tab)
├── posts/
│   ├── _layout.tsx
│   ├── index.tsx             # /posts
│   └── [id].tsx              # /posts/123 (dynamic)
└── (modal)/                  # Modal group
    └── settings.tsx          # /settings as modal
```

```typescript
// app/_layout.tsx — root layout
import { Stack } from 'expo-router';
import { AppProviders } from '@/shared/providers';

export default function RootLayout() {
  return (
    <AppProviders>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="login" options={{ presentation: 'modal' }} />
      </Stack>
    </AppProviders>
  );
}

// app/posts/[id].tsx
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function PostScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { data: post } = usePost(id);
  
  return (
    <View>
      <Text>{post?.title}</Text>
      <Button title="Back" onPress={() => router.back()} />
    </View>
  );
}

// Navigate
router.push('/posts/123');
router.replace('/login');
router.back();
```


## Deep Linking

```typescript
// app.json
{
  "expo": {
    "scheme": "myapp",      // myapp://...
    "linking": {
      "config": {
        "screens": {
          "(tabs)": {
            "home": "home",
          },
          "posts": {
            "screens": {
              "[id]": "posts/:id",
            },
          },
        },
      },
    },
  },
}

// URL: myapp://posts/123 → opens PostScreen with id=123
// HTTPS: https://myapp.com/posts/123 → opens app if installed

// Universal links (iOS) / App Links (Android) needed for HTTPS
// Configure in:
//   iOS:     associated-domains entitlement
//   Android: assetlinks.json on server
```


---

# CHAPTER 7: ERROR HANDLING


## Error Boundaries

```typescript
// shared/components/ErrorBoundary.tsx
import React, { Component, ReactNode } from 'react';
import * as Sentry from '@sentry/react-native';

interface Props {
  fallback?: ReactNode;
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    Sentry.captureException(error, {
      contexts: { react: { componentStack: errorInfo.componentStack } },
    });
  }
  
  reset = () => this.setState({ hasError: false, error: undefined });
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <View style={styles.container}>
          <Text style={styles.title}>Something went wrong</Text>
          <Text style={styles.message}>{this.state.error?.message}</Text>
          <Button title="Try Again" onPress={this.reset} />
        </View>
      );
    }
    return this.props.children;
  }
}

// Usage at multiple levels
function App() {
  return (
    <ErrorBoundary>      {/* App-wide catch-all */}
      <Navigation>
        {screens.map(screen => (
          <ErrorBoundary key={screen.name}>   {/* Per-screen isolation */}
            <screen.component />
          </ErrorBoundary>
        ))}
      </Navigation>
    </ErrorBoundary>
  );
}
```


## Sentry Integration

```typescript
// app/_layout.tsx
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
  enableAutoSessionTracking: true,
  sessionTrackingIntervalMillis: 30000,
  enableNative: true,
  tracesSampleRate: 0.1,    // 10% performance samples
  beforeSend(event) {
    // Don't send in dev
    if (__DEV__) return null;
    // Sanitize PII
    if (event.user) delete event.user.email;
    return event;
  },
});

// Capture manually
try {
  await dangerous();
} catch (err) {
  Sentry.captureException(err, {
    tags: { feature: 'checkout' },
    extra: { userId, orderId },
  });
}

// Set user context
Sentry.setUser({ id: user.id, username: user.name });   // Never send email/PII
Sentry.setContext('subscription', { plan: 'pro' });
```


## Toast Notifications

```typescript
// Use a global toast (e.g., react-native-toast-message)
import Toast from 'react-native-toast-message';

// In _layout.tsx
<>
  <Stack />
  <Toast />
</>

// Show from anywhere
Toast.show({
  type: 'success',
  text1: 'Saved!',
  text2: 'Your changes are saved',
  position: 'bottom',
  visibilityTime: 3000,
});

Toast.show({
  type: 'error',
  text1: 'Network error',
  text2: 'Please check your connection',
});
```


---

# CHAPTER 8: TESTING STRATEGY


## Testing Pyramid for Mobile

```
       ┌─────────┐
       │   E2E   │     Few (slow, fragile)
       │ (Detox) │     Critical user flows
       ├─────────┤
       │Integration│   Some
       │  Tests    │   Multiple components together
       ├─────────┤
       │  Unit   │     MANY (fast, cheap)
       │  Tests  │     Pure functions, hooks, components
       └─────────┘

ROUGH RATIO: 70% unit / 20% integration / 10% E2E

CRITICAL FLOWS to E2E test:
  - Onboarding/signup
  - Login
  - Core transaction (purchase, post, message)
  - Payment
  
DON'T E2E test every screen — diminishing returns.
```


## Component Tests with React Native Testing Library

```typescript
// __tests__/LoginScreen.test.tsx
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { LoginScreen } from '../LoginScreen';

describe('LoginScreen', () => {
  it('shows error for invalid email', async () => {
    const { getByPlaceholderText, getByText, findByText } = render(<LoginScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Email'), 'not-an-email');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password123');
    fireEvent.press(getByText('Login'));
    
    expect(await findByText('Invalid email')).toBeTruthy();
  });
  
  it('calls onLogin with valid credentials', async () => {
    const onLogin = jest.fn();
    const { getByPlaceholderText, getByText } = render(
      <LoginScreen onLogin={onLogin} />
    );
    
    fireEvent.changeText(getByPlaceholderText('Email'), 'user@example.com');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password123');
    fireEvent.press(getByText('Login'));
    
    await waitFor(() => {
      expect(onLogin).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123',
      });
    });
  });
});

// Mock API
jest.mock('@/features/auth/api/authApi', () => ({
  login: jest.fn().mockResolvedValue({ token: 'abc', user: { id: '1' } }),
}));
```


## Detox for E2E

```typescript
// e2e/login.e2e.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
  });
  
  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('test@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    
    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(5000);
    
    await expect(element(by.text('Welcome'))).toBeVisible();
  });
  
  it('should show error for invalid credentials', async () => {
    await element(by.id('email-input')).typeText('wrong@example.com');
    await element(by.id('password-input')).typeText('wrong');
    await element(by.id('login-button')).tap();
    
    await expect(element(by.text('Invalid credentials'))).toBeVisible();
  });
});
```


---

# CHAPTER 9: PRODUCTION CHECKLIST


## Pre-Launch Checklist

```
PERFORMANCE:
  ☐ Use FlashList for all long lists
  ☐ Reanimated 3 for all animations
  ☐ Images optimized (size + format) and lazy-loaded
  ☐ Hermes enabled
  ☐ New Architecture enabled (RN 0.76+)
  ☐ Bundle size reasonable (analyze with metro-visualizer)

OFFLINE:
  ☐ Critical screens work offline (cached)
  ☐ Network errors handled gracefully
  ☐ Optimistic updates for actions
  ☐ Offline indicator shown

ERROR HANDLING:
  ☐ Error boundaries at app + screen level
  ☐ Sentry (or similar) integrated
  ☐ Crash reporting tested
  ☐ Network errors → user-friendly messages
  ☐ API timeouts set

SECURITY:
  ☐ Sensitive data in secure storage (Keychain/Keystore)
  ☐ Certificate pinning for critical APIs
  ☐ No secrets in code
  ☐ Obfuscation enabled (ProGuard / R8)
  ☐ Disable debugging in release builds

UX:
  ☐ Loading states everywhere
  ☐ Empty states
  ☐ Error states
  ☐ Pull-to-refresh on lists
  ☐ Skeleton screens (not spinners) for slow loads
  ☐ Haptic feedback for important actions
  ☐ Dark mode supported
  ☐ Accessibility (VoiceOver/TalkBack labels)

ANALYTICS:
  ☐ Key events tracked (signup, purchase, etc.)
  ☐ User properties set
  ☐ Funnels defined
  ☐ Privacy: opt-in, sanitize PII

TESTING:
  ☐ Unit tests for utilities and hooks
  ☐ Component tests for critical UI
  ☐ E2E for: signup, login, core flow
  ☐ Manual test on real devices (iOS + Android)
  ☐ Test on slow networks (Network Link Conditioner)

STORE METADATA:
  ☐ App icon (all sizes)
  ☐ Screenshots (each device size)
  ☐ Description optimized for ASO
  ☐ Privacy policy URL
  ☐ Age rating accurate
  ☐ Permissions explained in description

UPDATES:
  ☐ OTA updates (Expo Updates / CodePush)
  ☐ Version checking ("must update")
  ☐ Migration logic for breaking changes
```


## Common Pitfalls

```
PITFALL 1: Server state in Redux/Zustand
  → Use TanStack Query for server data, Zustand for UI state.

PITFALL 2: FlatList for long lists
  → FlashList is 5-10x faster, simple migration.

PITFALL 3: Inline functions in render
  → Wrap with useCallback if passed to memo'd children.

PITFALL 4: Heavy work in render
  → Move to useMemo or background.

PITFALL 5: Not testing offline behavior
  → Toggle airplane mode in dev. Test every feature offline.

PITFALL 6: Logging sensitive data
  → Never console.log tokens, passwords, PII.

PITFALL 7: Animated API instead of Reanimated
  → Old Animated goes through bridge → janky. Use Reanimated 3.

PITFALL 8: AsyncStorage for everything
  → Slow + async. Use MMKV (30x faster, sync).

PITFALL 9: Missing keys in lists
  → Use stable, unique keys (item.id, not index).

PITFALL 10: Image without dimensions
  → Specify width/height to prevent layout jumps.

PITFALL 11: No iOS/Android testing
  → Differences exist (KeyboardAvoidingView, SafeArea, status bar).

PITFALL 12: Slow startup
  → Profile with --profiler. Lazy-load non-critical screens.

PITFALL 13: Ignoring native code requirements
  → Pure RN apps: cheap. Custom native: more complex maintenance.

PITFALL 14: Outdated dependencies
  → Update RN regularly (every 3-6 months). Old versions = no security patches.

PITFALL 15: Skipping accessibility
  → Apple/Google enforce in store reviews. Add accessibility props from day one.
```