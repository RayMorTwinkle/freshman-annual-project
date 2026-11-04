# Colab Session: annual-gpu-probe

## Session Created: 2026-11-03 13:46:12
- Endpoint: `gpu-t4-s-usw1b2-qubbqysxo102`

### Execution (2026-11-03 13:46:29)
```python
import torch, subprocess
print(subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.total','--format=csv,noheader'],text=True).strip())
print('torch:',torch.__version__)
print('CUDA available:',torch.cuda.is_available())
x=torch.arange(10,device='cuda'); print('CUDA sum:',x.sum().item())

```

**Output**:
```
Tesla T4, 15360 MiB
torch: 2.11.0+cu130
CUDA available: True
```

**Output**:
```
CUDA sum: 45
```

