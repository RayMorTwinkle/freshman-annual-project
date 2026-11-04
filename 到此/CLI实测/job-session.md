# Colab Session: annual-cli-job

## Session Created: 2026-11-03 13:45:59
- Endpoint: `m-s-euw4b2-1phh7q7zj2ok0`

### Execution (2026-11-03 13:46:02)
```python
import sys, warnings
sys.argv = ['job.py', 'demo']
__name__ = '__main__'
warnings.filterwarnings('ignore', message="To exit: use")
import sys
print("job arguments:", sys.argv[1:])
print("job result:", sum(range(101)))

```

**Output**:
```
job arguments: ['demo']
job result: 5050
```

