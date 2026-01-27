# Issue Fixed: DateTime Parsing Issue

## Problem Description
The backend was returning a 422 error when the frontend sent an empty string (`""`) for the `due_date` field. The error message was:

```
{
    "detail": [
        {
            "type": "datetime_parsing",
            "loc": ["body", "due_date"],
            "msg": "Input should be a valid datetime, input is too short",
            "input": "",
            "ctx": { "error": "input is too short" },
            "url": "https://errors.pydantic.dev/2.5/v/datetime_parsing"
        }
    ]
}
```

## Root Cause
- The frontend sends an empty string `""` for the `due_date` field when no date is selected
- The backend Pydantic schema expected `Optional[datetime] = None` but didn't handle empty strings
- Pydantic tried to parse the empty string as a datetime format and failed immediately with "input is too short"

## Solution Implemented
Added a custom field validator to the `TaskBase`, `TaskCreate`, and `TaskUpdate` schemas in `backend/schemas/task.py`:

```python
@field_validator('due_date', mode='before')
@classmethod
def validate_due_date(cls, value):
    if value == "" or value is None:
        return None
    if isinstance(value, str):
        # Handle string datetime formats
        if value.strip() == "":
            return None
        # If it's a date-only string like "2023-12-31", convert to datetime
        if len(value) == 10 and '-' in value:  # YYYY-MM-DD format
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                pass  # Fall through to try datetime parsing
        # Try to parse as datetime
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            pass
    return value
```

## What the Fix Handles
1. ✅ Empty string `""` → converted to `None`
2. ✅ Null values → remain as `None`
3. ✅ Valid datetime strings → parsed correctly
4. ✅ Date-only strings (YYYY-MM-DD) → converted to datetime with 00:00:00 time
5. ✅ Proper datetime strings → parsed correctly

## Verification
- All existing functionality continues to work
- Empty due_date fields no longer cause 422 errors
- Valid due_date values are still processed correctly
- The frontend-backend communication test passes completely
- The original datetime fix test confirms the issue is resolved

## Files Modified
- `backend/schemas/task.py` - Added field validators to handle empty strings properly

The fix ensures backward compatibility while resolving the 422 error that occurred when frontend forms submitted empty date fields.