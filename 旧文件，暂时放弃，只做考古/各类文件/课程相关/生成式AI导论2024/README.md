# 字幕JSON转Markdown工具

## 项目说明

这个Python脚本用于将JSON格式的字幕文件转换为只包含content内容的Markdown格式。

## 虚拟环境说明

- **虚拟环境目录**: `subtitle_env`
- **占用空间**: 约20-50MB（非常轻量）
- **作用**: 隔离项目依赖，防止影响系统Python环境

## 使用方法

### 1. 激活虚拟环境
```bash
source subtitle_env/bin/activate
```

### 2. 运行转换脚本
```bash
python convert_subtitles.py
```

### 3. 退出虚拟环境
```bash
deactivate
```

## 输出结果

- 所有转换后的Markdown文件保存在 `markdown_output` 目录中
- 每个Markdown文件包含原始JSON中的所有字幕内容
- 内容按顺序编号，方便阅读

## 支持的文件格式

脚本会自动处理目录中的所有 `.json` 文件：
- 10.json
- 10p1.json  
- 20.json
- 30.json
- 40.json
- 50.json
- 60.json
- 60p1.json

## 注意事项

- 脚本使用Python标准库，无需额外安装依赖
- 虚拟环境只在当前终端会话中有效
- 转换后的文件会保留原始文件名（去掉.json扩展名）

## 其他Prompt
创建一个任务清单，依次阅读每个md的内容并给他们一个标题，并更改他们的文件名（接在原先文件名后，比如10：学习.md)