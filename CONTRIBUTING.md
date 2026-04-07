# 🤝 Contributing to AegisTrader

Thank you for your interest in contributing to AegisTrader! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Standards](#development-standards)
- [Testing](#testing)

## 📜 Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of trading concepts
- Familiarity with computer vision (for vision-related contributions)

### Areas for Contribution

We welcome contributions in the following areas:

1. **🧠 Trading Strategies**: New strategy implementations
2. **👁️ Vision System**: Improvements to YOLO/OCR components
3. **🔗 Broker Integration**: New broker API implementations
4. **📊 Analytics**: Performance metrics and reporting
5. **🐛 Bug Fixes**: Issue resolution and stability improvements
6. **📚 Documentation**: Guides, tutorials, and API documentation
7. **🧪 Testing**: Unit tests, integration tests, and test coverage
8. **🎨 UI/UX**: Monitoring dashboards and user interfaces

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# Add upstream remote
git remote add upstream https://github.com/originalowner/aegistrader.git
```

### 2. Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pre-commit

# Install pre-commit hooks
pre-commit install
```

### 3. Docker Development (Alternative)

```bash
# Use development Docker setup
docker-compose -f docker-compose.dev.yml up -d

# Enter development container
docker exec -it aegistrader-dev bash
```

### 4. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit for development
# Set DEBUG_MODE=true
# Set SAVE_DEBUG_SCREENSHOTS=true
```

## 📝 Contributing Guidelines

### Branch Naming

Use descriptive branch names with prefixes:

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical fixes
- `docs/` - Documentation updates
- `test/` - Test improvements
- `refactor/` - Code refactoring

Examples:
```bash
git checkout -b feature/rsi-strategy
git checkout -b bugfix/ocr-confidence-threshold
git checkout -b docs/api-integration-guide
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(strategy): add RSI mean reversion strategy"
git commit -m "fix(ocr): improve confidence threshold handling"
git commit -m "docs(api): add Binance integration examples"
```

### Code Style

We use Python PEP 8 with some modifications:

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking (optional but recommended)
mypy .
```

**Key standards:**
- Line length: 88 characters (Black default)
- Use type hints where possible
- Docstrings for all public functions and classes
- Meaningful variable and function names

## 🔄 Pull Request Process

### 1. Before Creating PR

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: your feature description"

# Push to your fork
git push origin feature/your-feature
```

### 2. PR Requirements

**Before submitting:**
- [ ] Code follows style guidelines
- [ ] Tests pass: `pytest tests/`
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No merge conflicts with main branch
- [ ] Pre-commit hooks pass

**PR Description should include:**
- Clear description of changes
- Motivation and context
- Type of change (bug fix, new feature, etc.)
- Testing performed
- Screenshots (if applicable)

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### 4. Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Approval** and merge

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- AegisTrader Version: [e.g. 1.0.0]

**Additional Context**
Any other context about the problem

**Logs**
```
Paste relevant log entries here
```
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other solutions you've considered

**Additional Context**
Any other context or screenshots
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_strategy.py

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

### Writing Tests

**Test file naming:** `test_*.py`

**Test function naming:** `test_*`

**Example test:**
```python
import pytest
from strategy.strategy_engine import StrategyEngine

class TestStrategyEngine:
    def test_strategy_initialization(self):
        """Test strategy engine initialization."""
        engine = StrategyEngine()
        assert engine is not None
        assert len(engine.enabled_strategies) > 0
    
    def test_signal_generation(self):
        """Test trading signal generation."""
        engine = StrategyEngine()
        # Add test implementation
        pass
    
    @pytest.fixture
    def sample_data(self):
        """Fixture for test data."""
        return {
            'symbol': 'BTCUSDT',
            'price': 50000.0,
            'volume': 1000.0
        }
```

### Test Categories

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test system performance

## 🏗️ Development Standards

### Code Organization

```
aegistrader/
├── vision/           # Computer vision components
├── browser/          # Browser automation
├── scanner/          # Market scanning
├── strategy/         # Trading strategies
├── execution/        # Trade execution
├── broker/           # Broker APIs
├── risk/             # Risk management
├── utils/            # Utilities
├── tests/            # Test files
└── docs/             # Documentation
```

### Documentation Standards

- **Docstrings**: Use Google-style docstrings
- **Type hints**: Include type hints for function parameters and returns
- **Comments**: Explain complex logic, not obvious code
- **README updates**: Update relevant documentation

**Example docstring:**
```python
def calculate_position_size(self, signal: TradingSignal, account_balance: float) -> float:
    """
    Calculate position size based on risk management rules.
    
    Args:
        signal: Trading signal with entry and stop loss prices
        account_balance: Current account balance
        
    Returns:
        Position size in base currency units
        
    Raises:
        ValueError: If signal or balance is invalid
    """
    pass
```

### Security Guidelines

- **Never commit secrets**: Use environment variables
- **Validate inputs**: Sanitize all external inputs
- **Error handling**: Don't expose sensitive information in errors
- **Dependencies**: Keep dependencies updated

## 🎯 Contribution Ideas

### Beginner-Friendly

- Fix typos in documentation
- Add unit tests for existing functions
- Improve error messages
- Add configuration validation

### Intermediate

- Implement new trading strategies
- Add new broker integrations
- Improve OCR accuracy
- Add performance metrics

### Advanced

- Implement machine learning models
- Add real-time data streaming
- Create web dashboard
- Optimize performance bottlenecks

## 📞 Getting Help

- **Discord**: Join our development Discord server
- **GitHub Discussions**: Ask questions and discuss ideas
- **Email**: Contact maintainers directly
- **Documentation**: Check existing docs first

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to maintainer team (for significant contributions)

Thank you for contributing to AegisTrader! 🚀
