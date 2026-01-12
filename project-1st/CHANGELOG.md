# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-01-12

### Security
- **CRITICAL**: Updated FastAPI from 0.109.0 to 0.109.1 to fix ReDoS vulnerability
  - CVE: Content-Type Header Regular Expression Denial of Service (ReDoS)
  - Affected versions: <= 0.109.0
  - Patched version: 0.109.1
  - Impact: Potential DoS attack via malicious Content-Type headers
  - Resolution: All backend tests pass with updated version

### Changed
- Backend requirements.txt: FastAPI version bump from 0.109.0 to 0.109.1

### Verified
- ✅ All 20 backend tests passing with FastAPI 0.109.1
- ✅ Docker image builds successfully with patched version
- ✅ No breaking changes in API behavior

## [1.0.0] - 2026-01-12

### Added
- Initial release of YouTube Video Summarizer MVP
- Backend FastAPI application with transcript extraction and Gemini integration
- Frontend React application with Vite and TailwindCSS
- Docker containerization with docker-compose orchestration
- CI/CD pipeline with GitHub Actions
- Comprehensive test suite (38 tests total)
- Complete documentation (README.md, AGENTS.md, PROJECT_SUMMARY.md, QUICKSTART.md)
- OpenAPI 3.0 specification
- GitHub Codespaces configuration

### Features
- YouTube transcript extraction (multiple URL format support)
- AI-powered summarization with Google Gemini Pro
- Chapter breakdown with timestamps
- Copy-to-clipboard functionality
- Responsive UI design
- Error handling with user-friendly messages
- Health check endpoint
- CORS configuration

### Testing
- 20 backend tests (pytest)
- 18 frontend tests (vitest)
- 100% test pass rate

### Documentation
- README.md: Comprehensive guide with architecture and setup
- AGENTS.md: AI-assisted development workflow
- PROJECT_SUMMARY.md: Implementation details and validation
- QUICKSTART.md: 5-minute setup guide
- OpenAPI specification for API contract
