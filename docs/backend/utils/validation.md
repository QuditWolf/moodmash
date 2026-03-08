# Validation Utilities

## Purpose

Input validation utilities for quiz answers, UUIDs, vectors, and other data structures. Ensures data integrity and security before processing.

## Location

`backend/src/utils/validation.py`

## Functions

### validate_uuid(value, field_name)

Validates that a string is a valid UUID format (RFC 4122).

**Parameters**:
- `value` (str): String to validate
- `field_name` (str): Name of field for error messages (default: "ID")

**Returns**: bool - True if valid UUID

**Raises**:
- `ValueError`: If not a valid UUID with descriptive message

**Example**:
```python
from backend.src.utils.validation import validate_uuid

# Valid UUID
validate_uuid("550e8400-e29b-41d4-a716-446655440000", "userId")  # Returns True

# Invalid format
validate_uuid("not-a-uuid", "sessionId")
# Raises: ValueError("sessionId must be a valid UUID format")

# Empty string
validate_uuid("", "userId")
# Raises: ValueError("userId cannot be empty")
```

**UUID Format**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (8-4-4-4-12 hex digits)

---

### validate_section1_answers(answers)

Validates Section 1 quiz answers structure and content.

**Parameters**:
- `answers` (List[Dict[str, Any]]): List of answer dictionaries

**Returns**: bool - True if valid

**Raises**:
- `ValueError`: If validation fails with specific error message

**Validation Checks**:
1. Answers must be a list
2. Must contain exactly 5 answers
3. Each answer must have `questionId` and `selectedOptions`
4. Each answer must have at least one selected option
5. Each option must be a string ≤ 500 characters

**Example**:
```python
from backend.src.utils.validation import validate_section1_answers

# Valid answers
answers = [
    {'questionId': 'q1', 'selectedOptions': ['Books', 'Films']},
    {'questionId': 'q2', 'selectedOptions': ['Story-driven']},
    {'questionId': 'q3', 'selectedOptions': ['Deep']},
    {'questionId': 'q4', 'selectedOptions': ['Solo']},
    {'questionId': 'q5', 'selectedOptions': ['Evening']}
]
validate_section1_answers(answers)  # Returns True

# Invalid - wrong count
answers = [
    {'questionId': 'q1', 'selectedOptions': ['Books']}
]
validate_section1_answers(answers)
# Raises: ValueError("Section 1 must have exactly 5 answers, got 1")

# Invalid - empty options
answers = [
    {'questionId': 'q1', 'selectedOptions': []},
    # ... 4 more
]
validate_section1_answers(answers)
# Raises: ValueError("Section 1 answer 1 must have at least one selected option")
```

---

### validate_answer_structure(answer, context)

Validates the structure of a single quiz answer.

**Parameters**:
- `answer` (Dict[str, Any]): Answer dictionary to validate
- `context` (str): Context string for error messages (default: "Answer")

**Returns**: bool - True if valid

**Raises**:
- `ValueError`: If validation fails with specific error message

**Validation Checks**:
1. Answer must be a dictionary
2. Must have `questionId` field (non-empty string)
3. Must have `selectedOptions` field (list)
4. selectedOptions must have at least one element
5. Each option must be a string ≤ 500 characters

**Example**:
```python
from backend.src.utils.validation import validate_answer_structure

# Valid answer
answer = {'questionId': 'q1', 'selectedOptions': ['Option A', 'Option B']}
validate_answer_structure(answer, "Section 1 answer 1")  # Returns True

# Invalid - missing questionId
answer = {'selectedOptions': ['Option A']}
validate_answer_structure(answer)
# Raises: ValueError("Answer must have questionId field")

# Invalid - option too long
answer = {
    'questionId': 'q1',
    'selectedOptions': ['A' * 501]  # 501 characters
}
validate_answer_structure(answer)
# Raises: ValueError("Answer option 0 exceeds maximum length of 500 characters")
```

---

### validate_quiz_answers(all_answers)

Validates complete quiz answers for both sections.

**Parameters**:
- `all_answers` (Dict[str, Any]): Dictionary with section1 and section2 answer lists

**Returns**: bool - True if valid

**Raises**:
- `ValueError`: If validation fails with specific error message

**Validation Checks**:
1. all_answers must be a dictionary
2. Must contain `section1` key with valid Section 1 answers
3. Must contain `section2` key with list of answers
4. Section 2 must have at least 1 answer
5. All answers must have valid structure

**Example**:
```python
from backend.src.utils.validation import validate_quiz_answers

# Valid complete quiz
all_answers = {
    'section1': [
        {'questionId': 'q1', 'selectedOptions': ['Books']},
        # ... 4 more
    ],
    'section2': [
        {'questionId': 'q6', 'selectedOptions': ['Character development']},
        # ... 4 more
    ]
}
validate_quiz_answers(all_answers)  # Returns True

# Invalid - missing section2
all_answers = {
    'section1': [...]  # 5 valid answers
}
validate_quiz_answers(all_answers)
# Raises: ValueError("Quiz answers must contain section2")

# Invalid - empty section2
all_answers = {
    'section1': [...],  # 5 valid answers
    'section2': []
}
validate_quiz_answers(all_answers)
# Raises: ValueError("Section 2 must have at least 1 answer")
```

---

### validate_vector(vector, expected_dimension)

Validates embedding vector structure and values.

**Parameters**:
- `vector` (List[float]): Vector to validate
- `expected_dimension` (int): Expected number of dimensions (default: 1024 for Titan v2)

**Returns**: bool - True if valid

**Raises**:
- `ValueError`: If validation fails with specific error message

**Validation Checks**:
1. Vector must be a list
2. Must have exactly `expected_dimension` elements
3. All elements must be numeric (int or float)
4. All values must be between -1 and 1

**Example**:
```python
from backend.src.utils.validation import validate_vector

# Valid vector
vector = [0.5] * 1024
validate_vector(vector)  # Returns True

# Invalid dimension
vector = [0.5] * 512
validate_vector(vector)
# Raises: ValueError("Vector must have 1024 dimensions, got 512")

# Invalid value range
vector = [1.5] + [0.5] * 1023
validate_vector(vector)
# Raises: ValueError("Vector element 0 must be between -1 and 1, got 1.5")

# Custom dimension
vector = [0.1, 0.2, 0.3]
validate_vector(vector, expected_dimension=3)  # Returns True

# Non-numeric value
vector = ['string'] + [0.5] * 1023
validate_vector(vector)
# Raises: ValueError("Vector element 0 must be numeric, got <class 'str'>")
```

## Error Messages

All validation functions provide specific, actionable error messages:

```python
{
    "error": "Validation failed",
    "message": "Section 1 must have exactly 5 answers, got 3",
    "field": "section1"
}
```

## Usage in Handlers

### Quiz Handler Example
```python
from backend.src.utils.validation import validate_section1_answers, validate_uuid

def generate_section2_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        # Validate session ID
        session_id = body.get('sessionId')
        validate_uuid(session_id, 'sessionId')
        
        # Validate Section 1 answers
        section1_answers = body.get('section1Answers')
        validate_section1_answers(section1_answers)
        
        # Process request...
        
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
```

### Embedding Handler Example
```python
from backend.src.utils.validation import validate_quiz_answers, validate_vector

def generate_embedding_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        # Validate complete quiz answers
        all_answers = body.get('allAnswers')
        validate_quiz_answers(all_answers)
        
        # Generate embedding...
        vector = titan_service.generate_embedding(document)
        
        # Validate embedding before storing
        validate_vector(vector)
        
        # Store in database...
        
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
```

## Security Considerations

### Input Sanitization
- All string inputs are validated for length
- UUID format prevents injection attacks
- Vector bounds prevent numerical overflow
- No raw user input is executed or evaluated

### Privacy Protection
- Validation happens before any storage
- Invalid data is rejected immediately
- No sensitive data in error messages
- Validation errors are logged without PII

### Best Practices
```python
# Always validate at API boundary
def handler(event, context):
    # 1. Parse input
    body = json.loads(event['body'])
    
    # 2. Validate BEFORE processing
    validate_quiz_answers(body['answers'])
    
    # 3. Process validated data
    result = process_answers(body['answers'])
    
    # 4. Return response
    return {'statusCode': 200, 'body': json.dumps(result)}
```

## Performance

- **validate_uuid**: O(1) - Regex match
- **validate_section1_answers**: O(n) where n = 5 answers
- **validate_answer_structure**: O(m) where m = number of options
- **validate_quiz_answers**: O(n + m) where n = answers, m = options
- **validate_vector**: O(d) where d = vector dimension (1024)

All validation functions execute in < 1ms for typical inputs.

## Testing

Unit tests are located in:
- `backend/tests/unit/test_validation.py`

**Test Coverage**:
- Valid inputs return True
- Invalid formats raise ValueError
- Error messages are descriptive
- Edge cases (empty, null, wrong types)
- Boundary conditions (max length, dimension)

## Related

- Used by all handlers for input validation
- [vector_ops](./vector-operations.md) - Vector validation
- [embedding_builder](./embedding-builder.md) - Uses validation
- [logger](./logger.md) - Logs validation errors

## References

- **Requirements**: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9
- **Design**: Input Validation and Sanitization section
