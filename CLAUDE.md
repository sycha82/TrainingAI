# CLAUDE.md - AI Assistant Guide for TrainingAI Repository

## 🎯 Project Overview

**TrainingAI** is a logistics center facility matching AI engine that automatically matches orders to the most suitable facilities based on various attributes. The project is designed to be beginner-friendly for Python learners and .NET developers.

### Purpose
- Automatically match warehouse orders to optimal facilities
- Support both rule-based and machine learning matching engines
- Provide educational resources for Python beginners
- Offer production-ready web APIs

### Target Audience
- Python beginners (학습자)
- .NET developers transitioning to Python
- Logistics/warehouse automation systems

---

## 📁 Codebase Structure

```
TrainingAI/
├── README.md                          # Main documentation (Korean)
├── PRACTICE_GUIDE.md                  # Practice guide for learners (Korean)
├── WEB_APP_GUIDE.md                   # Web application guide (Korean)
├── CLAUDE.md                          # This file - AI assistant guide
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
│
├── src/                               # Source code (core engine)
│   ├── models/                        # Data models
│   │   ├── order.py                  # Order class with validation
│   │   └── facility.py               # Facility class with validation
│   ├── engine/                        # Matching engines
│   │   ├── matcher.py                # Rule-based matching engine
│   │   └── ml_matcher.py             # Machine learning engine (Random Forest)
│   └── data/                          # Data generation
│       ├── sample_data.py            # Sample facilities/orders
│       └── training_data_generator.py # ML training data generator
│
├── examples/                          # Usage examples
│   ├── basic_matching.py             # Rule-based engine examples
│   ├── ml_matching.py                # ML engine examples
│   ├── compare_engines.py            # Compare both engines
│   └── interactive_practice.py       # Interactive CLI practice
│
├── exercises/                         # Practice exercises (beginner/intermediate/advanced)
│   ├── beginner_exercises.py
│   ├── intermediate_exercises.py
│   └── advanced_exercises.py
│
├── tests/                             # Automated tests
│   ├── test_basic.py                 # Basic functionality tests (14 tests)
│   └── test_ml.py                    # ML engine tests (13 tests)
│
├── webapp/                            # Web applications
│   ├── api.py                        # FastAPI backend (REST API)
│   ├── streamlit_app.py              # Streamlit dashboard
│   └── static/                       # Static HTML/CSS/JS files
│
└── verify_ml_fix.py                  # ML verification script

```

---

## 🏗️ Architecture & Key Components

### 1. Data Models (`src/models/`)

**Order (`order.py`)**
- Represents warehouse orders
- Key attributes: `order_id`, `weight`, `volume`, `item_count`, `fragile`, `priority`, `destination_zone`, `order_type`
- Validation in `__post_init__()`: ensures valid weight, volume, item_count, and priority
- Helper methods: `get_density()`, `is_heavy()`, `is_bulk()`

**Facility (`facility.py`)**
- Represents warehouse facilities/equipment
- Key attributes: `facility_id`, `name`, `facility_type`, `max_weight`, `max_volume`, `can_handle_fragile`, `speed_rating`, `supported_zones`, `available`
- Validation in `__post_init__()`: ensures valid max_weight, max_volume, and speed_rating
- Key methods: `can_handle_order()`, `get_capacity_utilization()`

### 2. Matching Engines (`src/engine/`)

**FacilityMatcher (`matcher.py`)** - Rule-based Engine
- Scores facilities based on weighted factors:
  - Capacity utilization (25%): Efficient use of facility capacity
  - Speed (25%): Matches priority requirements
  - Fragile handling (20%): Safety for fragile items
  - Zone matching (15%): Direct connection to destination
  - Facility type (15%): Suitability for order type
- Customizable weights via constructor
- Methods:
  - `calculate_score()`: Compute 0.0-1.0 score for order-facility pair
  - `find_best_facility()`: Find single best match
  - `rank_facilities()`: Rank all facilities by score
  - `batch_match()`: Process multiple orders at once

**MLMatcher (`ml_matcher.py`)** - Machine Learning Engine
- Uses **Random Forest Classifier** (scikit-learn)
- Learns from historical matching data
- Feature extraction: Converts Order objects to numerical feature vectors (10 features)
- Methods:
  - `train()`: Train model on historical data
  - `predict()`: Predict best facility for new order
  - `predict_top_k()`: Get top K predictions
  - `save_model()` / `load_model()`: Persist models using joblib
  - `evaluate()`: Measure accuracy on test data

### 3. Web Applications (`webapp/`)

**FastAPI Backend (`api.py`)**
- RESTful API similar to ASP.NET Core
- Endpoints:
  - `GET /`: Root API info
  - `GET /health`: Health check
  - `GET /facilities`: List all facilities
  - `POST /match/rule-based`: Rule-based matching
  - `POST /match/ml`: ML-based matching
  - `POST /train/ml`: Train ML model
- Auto-generated Swagger UI at `/docs`
- CORS enabled for frontend integration

**Streamlit Dashboard (`streamlit_app.py`)**
- Interactive web UI for testing
- ML model training interface
- Real-time matching visualization

---

## 🎨 Coding Conventions & Patterns

### Language & Documentation
- **Primary Language**: Korean (for user-facing documentation)
- **Code Comments**: Mix of Korean and English
- **Docstrings**: Korean with .NET comparison notes for developers

### Code Style
- **Python Version**: 3.7+
- **Type Hints**: Used throughout (PEP 484)
- **Dataclasses**: Used for models (`@dataclass` decorator)
- **Naming Conventions**:
  - Classes: `PascalCase` (e.g., `FacilityMatcher`)
  - Functions/methods: `snake_case` (e.g., `find_best_facility`)
  - Constants: `UPPER_SNAKE_CASE` (rare in this codebase)
  - Private members: `_leading_underscore` (e.g., `_model`, `_extract_features`)

### Validation Pattern
All models use `__post_init__()` for validation:
```python
def __post_init__(self):
    if self.weight < 0:
        raise ValueError("무게는 0 이상이어야 합니다")
```

### .NET Developer Bridge Comments
Code includes comments like:
```python
# .NET 비유:
# - C#의 클래스와 동일한 구조
# - 인스턴스 필드(self._model 등)는 C#의 private 필드와 같음
```

---

## 🔧 Development Workflows

### Setting Up Development Environment

```bash
# Clone repository (if needed)
cd TrainingAI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run basic tests (14 tests)
python tests/test_basic.py

# Run ML tests (13 tests)
python tests/test_ml.py

# Expected output: All tests should pass
```

### Running Examples

```bash
# Rule-based engine
python examples/basic_matching.py

# ML engine
python examples/ml_matching.py

# Compare engines
python examples/compare_engines.py

# Interactive practice
python examples/interactive_practice.py
```

### Running Web Applications

```bash
# FastAPI (REST API)
uvicorn webapp.api:app --reload
# Access: http://localhost:8000
# Swagger: http://localhost:8000/docs

# Streamlit (Dashboard)
streamlit run webapp/streamlit_app.py
# Access: http://localhost:8501
```

### Git Workflow
- **Branch Naming**: Use `claude/` prefix for AI assistant branches
- **Current Branch**: `claude/claude-md-mis23q1orx1pj5dx-01Xv3NCbtBewJX8v3LxkSzBY`
- **Main Branch**: (not specified in git status)
- **Commit Style**: Clear, descriptive messages in English
- **Recent Pattern**: Feature additions and bug fixes

---

## ⚠️ Important Considerations

### When Modifying Code

1. **Validation is Critical**: Both `Order` and `Facility` have strict validation in `__post_init__()`. Always maintain validation when adding new attributes.

2. **Feature Consistency**: If adding attributes to `Order`, update:
   - `Order.__post_init__()` for validation
   - `MLMatcher._extract_features()` for ML features
   - Test cases in `tests/`
   - Example data generators

3. **Facility ID Consistency**: The ML matcher relies on consistent facility IDs. When generating training data, use the SAME facility IDs that will be used in prediction.
   - **Critical Bug Fixed**: `verify_ml_fix.py` documents a bug where training used different facility IDs than prediction
   - Always use `generator.generate_facilities()` consistently

4. **Score Ranges**:
   - Rule-based scores: 0.0 to 1.0
   - ML confidence: 0.0 to 1.0 (probabilities)

5. **Korean Text**: Maintain Korean for user-facing messages, errors, and documentation. Code comments can be mixed.

### Dependencies
- **Core**: numpy, scikit-learn, joblib (for ML)
- **Web**: fastapi, uvicorn, pydantic, streamlit
- **No external data storage**: Uses in-memory data (consider adding DB in future)

### Testing Philosophy
- **Test Coverage**: 27 automated tests total
- **Test Files**: Separate files for basic (`test_basic.py`) and ML (`test_ml.py`)
- **Test Pattern**: Uses `unittest.TestCase`
- **Assertions**: Standard unittest assertions (`assertEqual`, `assertTrue`, etc.)

---

## 🚀 Common Tasks for AI Assistants

### Task 1: Add a New Order Attribute

Example: Adding `temperature_controlled` attribute

1. **Update Order model** (`src/models/order.py`):
   ```python
   @dataclass
   class Order:
       # ... existing attributes ...
       temperature_controlled: bool = False
   ```

2. **Update ML feature extraction** (`src/engine/ml_matcher.py`):
   ```python
   def _extract_features(self, order: Order) -> np.ndarray:
       features = [
           # ... existing features ...
           1.0 if order.temperature_controlled else 0.0,
       ]
       return np.array(features)
   ```

3. **Update feature names**:
   ```python
   def get_feature_names(self) -> List[str]:
       return [
           # ... existing names ...
           "temperature_controlled"
       ]
   ```

4. **Add tests** in `tests/test_basic.py` and `tests/test_ml.py`

5. **Update documentation** (README.md, relevant guides)

### Task 2: Adjust Matching Weights

To prioritize speed over capacity:
```python
matcher = FacilityMatcher(
    weight_capacity=0.1,   # Reduced
    weight_speed=0.5,      # Increased
    weight_fragile=0.2,
    weight_zone=0.1,
    weight_type=0.1
)
```

### Task 3: Train ML Model

```python
from src.engine.ml_matcher import MLMatcher
from src.data.training_data_generator import TrainingDataGenerator

# Generate training data
generator = TrainingDataGenerator(seed=42)
train_orders, train_labels = generator.generate_training_data(1000)

# Train model
ml_matcher = MLMatcher(n_estimators=100, random_state=42)
ml_matcher.train(train_orders, train_labels)

# Save for reuse
ml_matcher.save_model("trained_model.pkl")
```

### Task 4: Add New API Endpoint

In `webapp/api.py`:
```python
@app.get("/api/new-endpoint")
def new_endpoint():
    return {"message": "New endpoint"}
```

### Task 5: Debug ML Predictions

Check feature importances:
```python
importances = ml_matcher.get_feature_importances()
for feature, importance in sorted(importances.items(), key=lambda x: x[1], reverse=True):
    print(f"{feature}: {importance:.4f}")
```

---

## 📊 Testing Guidelines

### Running All Tests
```bash
python tests/test_basic.py
python tests/test_ml.py
```

### Test Structure
- Each test class inherits from `unittest.TestCase`
- Test methods start with `test_`
- Use descriptive test names in Korean or English

### Common Assertions
```python
self.assertEqual(a, b)           # a == b
self.assertTrue(condition)        # condition is True
self.assertFalse(condition)       # condition is False
self.assertIsNone(value)          # value is None
self.assertIsNotNone(value)       # value is not None
self.assertGreater(a, b)          # a > b
self.assertIn(item, container)    # item in container
```

### Test Data
- Use `create_sample_facilities()` from `src.data.sample_data`
- Use `TrainingDataGenerator` for ML test data

---

## 🔍 Code Navigation Tips

### Finding Specific Functionality

- **Order validation**: `src/models/order.py` → `__post_init__()`
- **Facility matching logic**: `src/engine/matcher.py` → `calculate_score()`
- **ML feature engineering**: `src/engine/ml_matcher.py` → `_extract_features()`
- **API endpoints**: `webapp/api.py` → search for `@app.get` or `@app.post`
- **Sample data**: `src/data/sample_data.py` → `create_sample_facilities()`, `create_sample_orders()`

### Key Files to Read First
1. `README.md` - Project overview
2. `src/models/order.py` - Understand data structure
3. `src/models/facility.py` - Understand facility structure
4. `src/engine/matcher.py` - Understand rule-based logic
5. `examples/basic_matching.py` - See usage patterns

---

## 🌐 Web Application Architecture

### FastAPI Backend
- **Framework**: FastAPI (Python's equivalent to ASP.NET Core)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic models (similar to C# DTOs)
- **Documentation**: Auto-generated at `/docs` (Swagger UI)

### Streamlit Dashboard
- **Purpose**: Quick prototyping and data science apps
- **Style**: Declarative UI (simpler than Blazor)
- **State**: Session state management built-in

### Static Files
- HTML/CSS/JS in `webapp/static/`
- Served by FastAPI using `StaticFiles`

---

## 📚 Additional Resources

### Documentation Files
- **README.md**: Main project documentation (Korean)
- **PRACTICE_GUIDE.md**: Learning guide for Python beginners (Korean)
- **WEB_APP_GUIDE.md**: Web application setup and deployment (Korean)

### Learning Path
1. Beginners: `examples/basic_matching.py` → `exercises/beginner_exercises.py`
2. Intermediate: `exercises/intermediate_exercises.py` → `examples/interactive_practice.py`
3. Advanced: `exercises/advanced_exercises.py` → `examples/ml_matching.py`

---

## 🎯 Project Goals & Future Enhancements

### Current Status
- ✅ Rule-based matching engine
- ✅ ML-based matching engine (Random Forest)
- ✅ Web APIs (FastAPI + Streamlit)
- ✅ Comprehensive test suite
- ✅ Educational materials

### Potential Future Additions (from README)
- [ ] Real-time facility availability tracking
- [ ] Database integration
- [ ] Advanced analytics and reporting
- [ ] Facility utilization prediction
- [ ] Performance optimization and caching

---

## 💡 Tips for AI Assistants

1. **Respect Korean Documentation**: Maintain Korean for user-facing content, can use English for code comments
2. **Validate Everything**: Both models have strict validation - maintain it
3. **Test After Changes**: Run `python tests/test_basic.py` and `python tests/test_ml.py`
4. **Feature Extraction Sync**: When adding Order attributes, update ML feature extraction
5. **Facility ID Consistency**: Critical for ML predictions - use same IDs in training and prediction
6. **Weight Normalization**: FacilityMatcher automatically normalizes weights to sum to 1.0
7. **.NET Developer Friendly**: Include .NET comparisons when adding new patterns
8. **Educational Focus**: Code should be readable for beginners

---

## 🐛 Known Issues & Solutions

### Issue: ML Matching Failure
**Symptom**: `verify_ml_fix.py` was created to fix ML matching issues
**Root Cause**: Training data used different facility IDs than prediction data
**Solution**: Always use `generator.generate_facilities()` consistently for both training and prediction

### Issue: Module Not Found
**Symptom**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Run from project root: `cd /home/user/TrainingAI`

### Issue: ML Model Not Trained
**Symptom**: `RuntimeError: 모델이 학습되지 않았습니다`
**Solution**: Call `ml_matcher.train()` before `predict()`, or load saved model

---

## 📝 Commit Message Guidelines

Based on recent commits:
- Use descriptive English commit messages
- Format: `<Action> <what was done>`
- Examples:
  - "Add machine learning matching engine"
  - "Fix ML matching failure by using consistent facility IDs"
  - "Add web application support with FastAPI and Streamlit"

---

## 🔐 Security Considerations

- **Input Validation**: All models validate inputs in `__post_init__()`
- **No Authentication**: Current web API has no auth (add JWT/OAuth for production)
- **CORS**: Enabled for all origins in development (restrict in production)
- **File Uploads**: No file upload functionality (safe)

---

## 🎓 Educational Philosophy

This project is designed for learning:
- **Gradual Complexity**: Starts simple, adds ML complexity
- **Commented Code**: Extensive comments in Korean and English
- **.NET Bridging**: Helps .NET developers understand Python
- **Hands-on Practice**: Interactive exercises and examples
- **Real-world Application**: Practical logistics problem

---

**Last Updated**: 2025-12-04
**Repository Path**: `/home/user/TrainingAI`
**Python Version**: 3.7+
**License**: MIT
