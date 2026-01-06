# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development
All development follows documented specifications using the Agentic Dev Stack workflow (Spec → Plan → Tasks → Implement). Every feature must be specified before implementation begins, ensuring alignment between requirements and deliverables.

### II. Full-Stack Architecture
Maintain clear separation between frontend (Next.js) and backend (FastAPI) with well-defined API contracts. Both layers must be independently deployable and scalable.

### III. Security-First Approach
Implement authentication and authorization from the start using Better Auth with JWT tokens. All API endpoints require valid authentication tokens, and users can only access their own data.

### IV. Type Safety and Validation
Use TypeScript for frontend and Pydantic models for backend to ensure type safety. All user inputs must be validated and sanitized before processing.

### V. Performance and Reliability
Optimize for sub-2s initial load times on frontend and sub-200ms API response times on backend. Implement proper error handling, logging, and monitoring.

### VI. User Experience Focus
Design intuitive, responsive interfaces that work across all device sizes. Prioritize user workflows and provide clear feedback for all actions.

## Technology Stack Standards

### Frontend (Next.js 16+)
- Use App Router for routing and navigation
- Server components by default, client components only when interactivity is required
- Tailwind CSS for styling with consistent design system
- TypeScript for type safety and better developer experience
- Follow React best practices and performance optimization techniques

### Backend (Python FastAPI)
- Pydantic models for request/response validation and serialization
- SQLModel for database operations with proper ORM patterns
- Proper error handling with HTTPException and custom error responses
- Automatic API documentation via OpenAPI/Swagger UI
- Structured logging for observability and debugging

### Database (Neon Serverless PostgreSQL)
- Proper indexing for performance-critical queries
- Foreign key constraints to maintain data integrity
- Connection pooling for efficient resource utilization
- Database migrations for schema evolution
- Use SQLModel for all database interactions

### Authentication (Better Auth with JWT)
- JWT tokens for stateless authentication between frontend and backend
- Proper token expiration and refresh mechanisms
- Secure password handling and storage
- Session management with proper cleanup
- Shared secret key (BETTER_AUTH_SECRET) for token verification

## Development Workflow

### Spec-First Development
1. Write comprehensive specifications before implementation
2. Use Claude Code and Spec-Kit Plus for automated development
3. Reference specifications with @specs/ notation during implementation
4. Update specifications when requirements change

### Quality Standards
- Comprehensive unit and integration tests for all critical functionality
- Code reviews required for all pull requests
- Automated testing and linting in CI/CD pipeline
- Documentation for all public APIs and components
- Performance benchmarks and monitoring

### API Design Principles
- RESTful API design with consistent endpoint patterns
- Proper HTTP status codes and error responses
- Input validation and sanitization for all endpoints
- Rate limiting and security headers
- Versioning strategy for API evolution

## Security Requirements

### Authentication and Authorization
- JWT token-based authentication for all API endpoints
- User isolation - each user can only access their own data
- Proper token expiration and refresh mechanisms
- Secure session management
- Input validation and sanitization to prevent injection attacks

### Data Protection
- Encryption of sensitive data in transit and at rest
- Proper handling of user credentials and personal information
- Audit logging for security-relevant events
- Regular security assessments and vulnerability scanning

## Performance Standards

### Frontend Performance
- Sub-2s initial page load time
- Optimized asset delivery (images, scripts, stylesheets)
- Client-side caching strategies
- Lazy loading for non-critical resources
- Responsive design for all device sizes

### Backend Performance
- Sub-200ms API response times for 95th percentile
- Proper database indexing for query optimization
- Connection pooling and resource management
- Caching strategies for frequently accessed data
- Efficient data serialization and transfer

## Governance

### Decision Making
- Architectural decisions documented in ADRs (Architecture Decision Records)
- Team consensus required for major architectural changes
- Regular architecture reviews and retrospectives
- Clear ownership and accountability for components

### Code Quality
- All code must follow established style guides and conventions
- Automated linting and formatting enforced in CI/CD
- Comprehensive test coverage (minimum 80% for critical paths)
- Regular refactoring and technical debt management

### Compliance and Standards
- This constitution supersedes all other development practices
- All pull requests must comply with these principles
- Regular constitution reviews and updates as needed
- New team members must acknowledge and understand these principles

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
