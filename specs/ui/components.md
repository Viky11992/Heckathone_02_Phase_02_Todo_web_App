# UI Components Specification

## Overview
This document defines the user interface components for the Todo Full-Stack Web Application. The UI is built with Next.js and follows responsive design principles.

## Design Principles
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Accessibility**: WCAG 2.1 AA compliance
- **Consistency**: Consistent design language across all components
- **Performance**: Fast loading and smooth interactions
- **User Experience**: Intuitive and efficient task management

## Color Palette
- Primary: #3B82F6 (Blue-500) - For primary actions and highlights
- Secondary: #6B7280 (Gray-500) - For secondary elements
- Success: #10B981 (Emerald-500) - For success states
- Warning: #F59E0B (Amber-500) - For warnings
- Danger: #EF4444 (Red-500) - For errors and deletions
- Background: #FFFFFF (White) - For main background
- Surface: #F9FAFB (Gray-50) - For card backgrounds
- Text: #1F2937 (Gray-800) - For primary text

## Typography
- Font Family: Inter (system font stack)
- Body: 16px, 400 weight
- Headings: 24px-36px, 600-700 weight
- Small Text: 14px, 400 weight

## Components

### 1. TaskCard
**Purpose**: Display individual task information
**Props**:
- task: Task object
- onToggle: Function to handle completion toggle
- onEdit: Function to handle task editing
- onDelete: Function to handle task deletion

**Features**:
- Shows task title with strikethrough when completed
- Shows task description (truncated if long)
- Completion checkbox with toggle functionality
- Due date display (if set)
- Edit and delete buttons
- Visual indication of completion status

### 2. TaskForm
**Purpose**: Create and edit tasks
**Props**:
- task?: Task object (for editing, undefined for creation)
- onSubmit: Function to handle form submission
- onCancel: Function to handle form cancellation

**Features**:
- Title input field (required, 1-200 characters)
- Description textarea (optional, max 1000 characters)
- Due date picker (optional)
- Form validation with error messages
- Submit and cancel buttons
- Loading state during submission

### 3. TaskList
**Purpose**: Display a list of tasks with filtering options
**Props**:
- tasks: Array of Task objects
- onToggle: Function to handle task completion toggle
- onEdit: Function to handle task editing
- onDelete: Function to handle task deletion
- filter: Current filter status ("all", "pending", "completed")
- onFilterChange: Function to handle filter change

**Features**:
- Filter tabs (All, Pending, Completed)
- Empty state message when no tasks
- Loading state during data fetch
- Individual task cards
- Pagination for large task lists

### 4. Header
**Purpose**: Main navigation and user controls
**Props**:
- user: User object (if authenticated)
- onSignOut: Function to handle sign out

**Features**:
- App logo/title
- Navigation links
- User profile dropdown (when authenticated)
- Sign out button (when authenticated)
- Sign in/up links (when not authenticated)

### 5. AuthModal
**Purpose**: Handle user authentication (sign up/sign in)
**Props**:
- isOpen: Boolean to control modal visibility
- onClose: Function to close the modal
- mode: "signin" | "signup"

**Features**:
- Email input field
- Password input field
- Password strength indicator
- Form validation
- Mode toggle (sign in/sign up)
- Submit button with loading state
- Social login options (future enhancement)

### 6. LoadingSpinner
**Purpose**: Indicate loading states
**Props**:
- size: "sm" | "md" | "lg" (default: "md")

**Features**:
- Animated spinner
- Accessible loading indicator
- Different sizes for different contexts

### 7. Alert
**Purpose**: Display important messages and notifications
**Props**:
- type: "success" | "error" | "warning" | "info"
- message: String message to display
- onClose?: Function to handle dismissal

**Features**:
- Different styling based on type
- Optional close button
- Auto-dismiss for certain types
- Accessible message announcement

## Layout Components

### 1. MainLayout
**Purpose**: Main page layout with header and content area
**Props**:
- children: React children
- title: Page title for SEO

**Features**:
- Responsive header
- Main content area
- Footer (optional)
- SEO metadata

### 2. AuthLayout
**Purpose**: Layout for authentication pages
**Props**:
- children: React children
- title: Page title

**Features**:
- Centered auth form
- App branding
- Background pattern
- Minimal navigation

## Pages

### 1. Dashboard Page
**Route**: /
**Features**:
- Welcome message for authenticated users
- Quick task creation form
- Recent tasks preview
- Stats summary (total tasks, completed tasks)

### 2. Tasks Page
**Route**: /tasks
**Features**:
- Task list with filtering
- Add new task button
- Search functionality
- Empty state with call to action

### 3. Task Detail Page
**Route**: /tasks/[id]
**Features**:
- Full task details
- Edit task form
- Back to list button
- Task metadata (created/updated dates)

### 4. Sign In Page
**Route**: /auth/signin
**Features**:
- Sign in form
- Sign up link
- Password reset link
- Social login options

### 5. Sign Up Page
**Route**: /auth/signup
**Features**:
- Sign up form
- Sign in link
- Terms and conditions
- Social login options

## Responsive Breakpoints
- Mobile: 0px - 640px
- Tablet: 641px - 1024px
- Desktop: 1025px+

## Accessibility Features
- Semantic HTML structure
- Proper ARIA attributes
- Keyboard navigation support
- Focus management
- Screen reader compatibility
- Sufficient color contrast
- Resizable text support

## Performance Considerations
- Lazy loading for components outside viewport
- Code splitting for different pages
- Image optimization and lazy loading
- Efficient state management
- Debounced search inputs
- Virtualized lists for large datasets

## Error Boundaries
- Global error boundary for unhandled errors
- Component-specific error boundaries where appropriate
- User-friendly error messages
- Error reporting to monitoring service

## Internationalization
- Support for multiple languages
- Right-to-left layout support (future enhancement)
- Date and number formatting
- Proper text direction handling