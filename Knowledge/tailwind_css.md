# Tailwind CSS Complete Reference


---

# CHAPTER 1: CORE UTILITIES


## Layout

```html
<!-- Flexbox -->
<div class="flex items-center justify-between gap-4">
    <div class="flex-1">Grows</div>
    <div class="flex-shrink-0">Fixed</div>
</div>

<!-- Grid -->
<div class="grid grid-cols-3 gap-6">
    <div class="col-span-2">Wide</div>
    <div>Normal</div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- 1 col mobile, 2 tablet, 3 desktop -->
</div>

<!-- Center everything -->
<div class="flex items-center justify-center min-h-screen">Centered</div>

<!-- Container -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">Content</div>
```


## Common Components

```html
<!-- Button -->
<button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
    Click me
</button>

<!-- Card -->
<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
    <h3 class="text-lg font-semibold text-gray-900">Title</h3>
    <p class="text-gray-600 mt-2">Description here</p>
</div>

<!-- Input -->
<input class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" placeholder="Type here...">

<!-- Badge -->
<span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Active</span>

<!-- Avatar -->
<img class="w-10 h-10 rounded-full object-cover ring-2 ring-white" src="avatar.jpg" alt="User">

<!-- Navbar -->
<nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <span class="text-xl font-bold text-gray-900">Logo</span>
        <div class="flex items-center gap-6">
            <a href="#" class="text-gray-600 hover:text-gray-900 transition">Home</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 transition">About</a>
            <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm">Sign Up</button>
        </div>
    </div>
</nav>

<!-- Modal overlay -->
<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-2xl p-8 w-full max-w-md mx-4 shadow-xl">
        <h2 class="text-xl font-bold">Modal Title</h2>
        <p class="text-gray-600 mt-2">Content here</p>
    </div>
</div>
```


## Responsive Design

```html
<!-- Breakpoints: sm:640px md:768px lg:1024px xl:1280px 2xl:1536px -->

<!-- Stack on mobile, row on desktop -->
<div class="flex flex-col md:flex-row gap-4">
    <div class="w-full md:w-1/3">Sidebar</div>
    <div class="w-full md:w-2/3">Content</div>
</div>

<!-- Hide/show based on screen -->
<div class="hidden md:block">Desktop only</div>
<div class="md:hidden">Mobile only</div>

<!-- Responsive text -->
<h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">Title</h1>

<!-- Responsive padding -->
<div class="p-4 sm:p-6 md:p-8 lg:p-12">Content</div>
```


## Dark Mode

```html
<!-- Add dark: prefix -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <p class="text-gray-600 dark:text-gray-400">Adapts to theme</p>
    <button class="bg-indigo-600 dark:bg-indigo-500 text-white">Button</button>
</div>
```


## Animations

```html
<!-- Hover effects -->
<div class="hover:scale-105 transition-transform duration-200">Zoom on hover</div>
<div class="hover:-translate-y-1 hover:shadow-lg transition-all duration-200">Lift on hover</div>

<!-- Spin -->
<svg class="animate-spin h-5 w-5">...</svg>

<!-- Pulse -->
<div class="animate-pulse bg-gray-200 h-4 rounded w-3/4"></div>

<!-- Bounce -->
<div class="animate-bounce">↓</div>
```