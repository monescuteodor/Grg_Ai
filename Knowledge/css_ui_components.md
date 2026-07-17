# CSS UI Components and Design Patterns


---

# CHAPTER 1: COMMON UI COMPONENTS


## Modal / Dialog

```html
<div class="modal-overlay" id="modal" onclick="if(event.target===this)closeModal()">
    <div class="modal">
        <div class="modal-header">
            <h2>Modal Title</h2>
            <button class="modal-close" onclick="closeModal()">&times;</button>
        </div>
        <div class="modal-body">
            <p>Modal content goes here.</p>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
            <button class="btn btn-primary">Confirm</button>
        </div>
    </div>
</div>
```

```css
.modal-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.5);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000; opacity: 0; pointer-events: none; transition: opacity 0.2s;
}
.modal-overlay.active { opacity: 1; pointer-events: auto; }
.modal {
    background: white; border-radius: 12px; width: 90%; max-width: 500px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15); transform: translateY(20px) scale(0.95);
    transition: transform 0.3s ease;
}
.modal-overlay.active .modal { transform: translateY(0) scale(1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #e5e7eb; }
.modal-body { padding: 24px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 8px; padding: 16px 24px; border-top: 1px solid #e5e7eb; }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: #888; }
```


## Toast Notifications

```css
.toast-container {
    position: fixed; top: 20px; right: 20px; z-index: 9999;
    display: flex; flex-direction: column; gap: 8px;
}
.toast {
    padding: 12px 20px; border-radius: 8px; color: white; font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15); min-width: 250px;
    display: flex; align-items: center; gap: 10px;
    animation: toast-in 0.3s ease, toast-out 0.3s ease 2.7s forwards;
}
.toast.success { background: #22c55e; }
.toast.error { background: #ef4444; }
.toast.info { background: #3b82f6; }
@keyframes toast-in { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes toast-out { from { opacity: 1; } to { opacity: 0; transform: translateX(100%); } }
```

```javascript
function showToast(message, type = 'info') {
    const container = document.querySelector('.toast-container') || (() => {
        const c = document.createElement('div');
        c.className = 'toast-container';
        document.body.appendChild(c);
        return c;
    })();
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
```


## Dropdown Menu

```html
<div class="dropdown">
    <button class="dropdown-trigger" onclick="this.parentElement.classList.toggle('open')">
        Options ▾
    </button>
    <div class="dropdown-menu">
        <a href="#" class="dropdown-item">Edit</a>
        <a href="#" class="dropdown-item">Duplicate</a>
        <div class="dropdown-divider"></div>
        <a href="#" class="dropdown-item danger">Delete</a>
    </div>
</div>
```

```css
.dropdown { position: relative; display: inline-block; }
.dropdown-trigger { padding: 8px 16px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; }
.dropdown-menu {
    position: absolute; top: 100%; left: 0; margin-top: 4px;
    background: white; border: 1px solid #e5e7eb; border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1); min-width: 160px;
    opacity: 0; transform: translateY(-8px); pointer-events: none;
    transition: all 0.2s ease;
}
.dropdown.open .dropdown-menu { opacity: 1; transform: translateY(0); pointer-events: auto; }
.dropdown-item { display: block; padding: 8px 16px; color: #333; text-decoration: none; font-size: 14px; }
.dropdown-item:hover { background: #f5f5f5; }
.dropdown-item.danger { color: #ef4444; }
.dropdown-divider { height: 1px; background: #e5e7eb; margin: 4px 0; }
```


## Tabs

```html
<div class="tabs">
    <div class="tab-list">
        <button class="tab active" onclick="switchTab(this, 'tab1')">General</button>
        <button class="tab" onclick="switchTab(this, 'tab2')">Settings</button>
        <button class="tab" onclick="switchTab(this, 'tab3')">Advanced</button>
    </div>
    <div class="tab-content active" id="tab1">General content here</div>
    <div class="tab-content" id="tab2">Settings content here</div>
    <div class="tab-content" id="tab3">Advanced content here</div>
</div>
```

```css
.tab-list { display: flex; border-bottom: 2px solid #e5e7eb; }
.tab { padding: 10px 20px; background: none; border: none; font-size: 14px; cursor: pointer;
    color: #888; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
.tab.active { color: #6366f1; border-bottom-color: #6366f1; }
.tab-content { display: none; padding: 20px 0; }
.tab-content.active { display: block; }
```

```javascript
function switchTab(btn, tabId) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}
```


## Cards Grid

```css
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px; padding: 20px;
}
.card {
    background: white; border-radius: 12px; overflow: hidden;
    border: 1px solid #e5e7eb; transition: all 0.2s;
}
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.card-img { width: 100%; height: 200px; object-fit: cover; }
.card-body { padding: 20px; }
.card-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.card-text { color: #666; font-size: 14px; line-height: 1.6; }
.card-footer { padding: 12px 20px; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }
```


---

# CHAPTER 2: FORM PATTERNS


## Complete Form with Validation

```html
<form class="form" onsubmit="return validateForm(event)">
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" placeholder="you@example.com" required>
        <span class="error-msg" id="email-error"></span>
    </div>
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" placeholder="Min 8 characters" required>
        <div class="password-strength" id="strength"></div>
        <span class="error-msg" id="password-error"></span>
    </div>
    <button type="submit" class="btn btn-primary btn-full">Sign Up</button>
</form>
```

```css
.form { max-width: 400px; margin: 40px auto; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px; color: #333; }
.form-group input {
    width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px;
    font-size: 15px; transition: border-color 0.2s; outline: none;
}
.form-group input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.form-group input.invalid { border-color: #ef4444; }
.error-msg { font-size: 12px; color: #ef4444; margin-top: 4px; display: block; }
.password-strength { height: 4px; border-radius: 2px; margin-top: 6px; background: #eee; }
.password-strength::after {
    content: ''; display: block; height: 100%; border-radius: 2px;
    transition: width 0.3s, background 0.3s;
}
.strength-weak::after { width: 33%; background: #ef4444; }
.strength-medium::after { width: 66%; background: #f59e0b; }
.strength-strong::after { width: 100%; background: #22c55e; }
.btn { padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: 500; }
.btn-primary { background: #6366f1; color: white; }
.btn-primary:hover { background: #5558e6; }
.btn-full { width: 100%; }
```

```javascript
function validateForm(e) {
    e.preventDefault();
    let valid = true;
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    // Email validation
    if (!email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById('email-error').textContent = 'Please enter a valid email';
        email.classList.add('invalid');
        valid = false;
    } else {
        document.getElementById('email-error').textContent = '';
        email.classList.remove('invalid');
    }

    // Password validation
    if (password.value.length < 8) {
        document.getElementById('password-error').textContent = 'Password must be at least 8 characters';
        password.classList.add('invalid');
        valid = false;
    }

    if (valid) { alert('Form submitted!'); }
    return false;
}

// Password strength meter
document.getElementById('password').addEventListener('input', function() {
    const s = document.getElementById('strength');
    const v = this.value;
    s.className = 'password-strength';
    if (v.length >= 12 && /[A-Z]/.test(v) && /[0-9]/.test(v)) s.classList.add('strength-strong');
    else if (v.length >= 8) s.classList.add('strength-medium');
    else if (v.length > 0) s.classList.add('strength-weak');
});
```


---

# CHAPTER 3: ANIMATION PATTERNS

```css
/* Fade in on scroll */
.fade-in { opacity: 0; transform: translateY(20px); transition: all 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

/* Skeleton loading */
.skeleton { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%; animation: skeleton 1.5s infinite; border-radius: 4px; }
@keyframes skeleton { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Smooth page transitions */
.page-enter { animation: pageIn 0.3s ease; }
@keyframes pageIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }

/* Hover lift effect */
.lift { transition: transform 0.2s, box-shadow 0.2s; }
.lift:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

/* Ripple effect on click */
.ripple { position: relative; overflow: hidden; }
.ripple::after { content: ''; position: absolute; border-radius: 50%; background: rgba(255,255,255,0.3);
    width: 100px; height: 100px; top: 50%; left: 50%; transform: translate(-50%,-50%) scale(0);
    transition: transform 0.5s; }
.ripple:active::after { transform: translate(-50%,-50%) scale(4); transition: 0s; }
```