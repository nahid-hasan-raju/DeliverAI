# Contributing to QuikDel

Thank you for your interest in contributing to QuikDel! This project represents academic research in distributed reinforcement learning for urban delivery optimization.

## Project Overview

QuikDel is a research implementation accompanying the paper "QuikDel: A Novel & Scalable Q-learning based Distributed Approach for Efficient Long-haul Delivery" published in IEEE Transactions on Intelligent Transportation Systems.

## Types of Contributions

### Research Contributions
- **Algorithm improvements**: Enhancements to Q-learning, ride-sharing, or network construction
- **New baselines**: Implementation of additional comparison methods
- **Experimental validation**: Testing on new cities or parameter configurations
- **Performance optimizations**: Scalability improvements for larger urban areas

### Engineering Contributions
- **Bug fixes**: Corrections to existing functionality
- **Documentation**: Improvements to code documentation, tutorials, or examples
- **Testing**: Additional unit tests, integration tests, or validation scripts
- **Tooling**: Enhancements to QCense or visualization utilities

### Data Contributions
- **New city datasets**: Extension to additional U.S. cities
- **Validation data**: Ground truth for algorithm comparison
- **Benchmark scenarios**: Standardized test cases for reproducible evaluation

## Development Setup

### Prerequisites
- Python 3.8+
- GDAL library installed system-wide
- Git and standard development tools

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/quikdel.git
cd quikdel

# Create development environment
python -m venv quikdel-dev
source quikdel-dev/bin/activate  # Windows: quikdel-dev\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
python -m pytest tests/
```

## Coding Standards

### Code Style
- **Python**: Follow PEP 8, enforced by `black` and `flake8`
- **Imports**: Use `isort` for consistent import ordering
- **Type hints**: Encouraged for new functions, required for public APIs
- **Docstrings**: Use Google-style docstrings for all public functions

### Example Function Documentation

```python
def calculate_ses_score(producers: int, consumers: int, bordering_tracts: int) -> float:
    """Calculate Superspot Eligibility Score for hotspot selection.
    
    Args:
        producers: Number of food producers in census tract
        consumers: Number of consumers in census tract  
        bordering_tracts: Number of adjacent census tracts
        
    Returns:
        Normalized SES score between 0 and 1
        
    Example:
        >>> score = calculate_ses_score(25, 150, 6)
        >>> print(f"SES Score: {score:.3f}")
        SES Score: 0.742
    """
```

### Testing Requirements
- **Unit tests**: All new functions must include unit tests
- **Integration tests**: Multi-component features require integration tests
- **Regression tests**: Bug fixes should include tests preventing regression
- **Performance tests**: Algorithm changes should include performance validation

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test categories
python -m pytest tests/test_network_construction.py -v
```

## Research Workflow

### Experimental Validation
All algorithmic changes should be validated experimentally:

```bash
# Run baseline comparison
python scripts/validate_contribution.py \
    --city Columbus \
    --method your_new_method \
    --baseline quikdel_original \
    --runs 10

# Statistical significance testing
python scripts/statistical_validation.py \
    --results results/contribution_comparison/ \
    --significance_level 0.05
```

### Documentation Requirements
- **Algorithm changes**: Update relevant sections in `docs/architecture.md`
- **New features**: Include usage examples in `docs/tutorial.md`
- **Performance improvements**: Document benchmarks and complexity analysis
- **Paper references**: Cite relevant literature for new methods

## Submission Process

### Pull Request Guidelines

1. **Fork the repository** and create a feature branch
2. **Make your changes** following coding standards
3. **Add comprehensive tests** for new functionality
4. **Update documentation** as needed
5. **Run the full test suite** to ensure no regressions
6. **Submit a pull request** with clear description

### PR Template

```markdown
## Description
Brief description of the change and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Algorithm improvement
- [ ] Documentation update
- [ ] Performance optimization

## Experimental Validation
- [ ] Tested on existing benchmark cities
- [ ] Compared against baselines
- [ ] Statistical significance verified
- [ ] Performance impact measured

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] No regression in existing functionality

## Documentation
- [ ] Code documentation updated
- [ ] User-facing documentation updated
- [ ] Examples/tutorials added if needed

## Additional Notes
Any additional context, caveats, or considerations.
```

### Review Process
- **Academic review**: Algorithmic contributions reviewed by research team
- **Code review**: All contributions reviewed for code quality and testing
- **Experimental validation**: Performance claims verified independently
- **Documentation review**: Clarity and completeness of documentation

## Academic Research Ethics

### Attribution
- **Proper citation**: Reference original papers for implemented algorithms
- **Contribution acknowledgment**: Credit all contributors appropriately
- **Data sources**: Acknowledge data providers (Census Bureau, OSM, etc.)

### Reproducibility
- **Deterministic results**: Use fixed random seeds for reproducible experiments
- **Complete methodology**: Document all parameters and experimental setup
- **Data availability**: Ensure contributed datasets can be publicly shared

### Open Science
- **Open data**: Prefer publicly available datasets
- **Open methods**: Implementation should be transparent and well-documented
- **Reproducible research**: Others should be able to replicate your results

## Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and research discussions
- **Email**: Direct contact with maintainers for sensitive issues

### Resources
- **Paper**: [QuikDel IEEE TITS Paper](docs/QuikDel_IEEE_TITS.pdf)
- **Documentation**: [Full documentation](docs/)
- **Examples**: [Tutorial notebooks](notebooks/)
- **API Reference**: [Code documentation](docs/api_reference.md)

## Recognition

Contributors will be acknowledged in:
- **Repository README**: All contributors listed
- **Academic papers**: Significant algorithmic contributions may warrant co-authorship
- **Release notes**: Feature contributions highlighted in releases
- **Documentation**: Tutorial and example contributors credited

## License

By contributing to QuikDel, you agree that your contributions will be licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Thank you for contributing to QuikDel and advancing research in distributed reinforcement learning for urban logistics!
