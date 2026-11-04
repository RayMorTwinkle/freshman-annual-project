# CLI 实测结论

2026-11-03 实测版本 0.7.5。结论：适合本地写 Python、云端跑短实验，也适合 Agent 调度。不是自动同步项目的完整远程开发环境。

## 已实际验证

| 能力 | 结果 |
|---|---|
| OAuth + CPU Hello Colab | 用户亲自验证成功并停止实例 |
| CSV 上传 → 本地脚本远程执行 → JSON 下载 | 成功，1+2+3=6，返回 3 条输入 |
| 连续 exec 保留变量 | 成功，第二次 exec 可读取 experiment_total=6 |
| 云端 Python | 本次 CPU 实例为 3.13.18，本机 CLI Python 版本与它互不等同 |
| 默认工作目录 | 本次远端为 /content |
| colab run 参数传递 | 成功，demo 作为 sys.argv 参数传入，计算结果 5050 |
| run 自动释放实例 | 成功，输出 Session terminated |
| T4 GPU 分配 | 此次成功：Tesla T4，15360 MiB 显存 |
| CUDA 运算 | torch 2.11.0+cu130，CUDA available=True，GPU 张量求和结果 45 |
| 日志导出 | 成功，可导出 Markdown；原始历史默认在 ~/.config/colab-cli/history |
| 清理 | 最终 sessions 返回 No active sessions found on server |

测试脚本、CSV、下载的 JSON、会话日志保存在 CLI实测/。GPU 分配只代表本次可用，未据此推断账户订阅档位、固定配额或长期稳定性。

## 使用上方便的地方

- 本地写脚本可直接 exec，不必在网页来回复制。
- 同一实例的内核会保留变量、导入和已加载模型，便于迭代。
- stdout 可以回传终端，输入输出文件有明确的上传下载命令。
- 一次性只需 stdout 的任务用 run，默认自动清理。
- 日志能保存执行代码和输出，适合复现实验、辅助回忆。

## 实际限制与注意点

- exec 和 run 的默认执行 timeout 是 30 秒。耗时实验需显式增加，例如 --timeout 1800；这不是保证实例可持续运行 1800 秒。
- run 默认自动销毁实例；本版帮助没有自动拉取输出文件的选项，源码清理流程也没有自动下载步骤。要取回模型或图表，应使用持久会话，下载后再 stop，或用 run --keep 后自行下载并停止。此前“run 自动取回文件”的泛化描述不适用于这里。
- exec 只发送脚本内容，不会自动同步整个工程。输入数据、自定义模块、模型权重和环境需要另行准备。
- CLI运行环境和 Mac 不同。本次远端 Python 3.13.18，项目依赖需在云端检查，不能照搬本机环境就认定兼容。
- CLI 日志会包含执行代码、输出和文件路径；不要把带令牌、私人数据的日志直接提交到公开 GitHub。
- 导出的 Markdown 日志时间显示 13:45 等，是 UTC；本地北京时间为 21:45。源码中的原始 JSONL 使用带时区的 UTC 时间戳。
- Drive 挂载、SSH/IDE 远程开发、Notebook 输出回写、长时间训练、断线恢复、本地与远端目录同步未实测。

## 对大一年度项目的建议

先用已验证可用的 T4 跑小型 PyTorch/SmolVLA 推理测试；本次没有下载模型或验证 SmolVLA 依赖。完整 RoboTwin 仿真还要单独验证依赖、渲染与资源需求。

有输入和输出文件的实验优先走：new → install → upload → exec → download → stop。首次先做 1 个样本，确认结果能下载，再扩大计算量。

例子（路径和包名需按实际项目调整）：

```bash
colab --auth=oauth2 new -s annual-exp --gpu T4
colab --auth=oauth2 install -s annual-exp -r requirements.txt
colab --auth=oauth2 upload -s annual-exp ./input.csv /content/input.csv
colab --auth=oauth2 exec -s annual-exp -f experiment.py --timeout 1800
colab --auth=oauth2 download -s annual-exp /content/result.json ./result.json
colab log -s annual-exp -o execution.md
colab --auth=oauth2 stop -s annual-exp
```

以上模板不是已跑通的 SmolVLA 训练步骤。
