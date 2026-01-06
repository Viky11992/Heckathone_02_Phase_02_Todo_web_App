# Frontend Guidelines

## Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth for authentication

## Patterns
- Use server components by default
- Client components only when needed (interactivity)
- API calls go through `/lib/api.ts`

## Component Structure
- `/components` - Reusable UI components
- `/app` - Pages and layouts
- `/hooks` - Custom React hooks
- `/lib` - Utilities and API clients

## API Client
All backend calls should use the api client:

import { api } from '@/lib/api'
const tasks = await api.getTasks()

## Styling
- Use Tailwind CSS classes
- No inline styles
- Follow existing component patterns

## Authentication
- Use Better Auth client for authentication
- Implement protected routes using the protected route component
- Handle JWT tokens automatically in API calls