# AIGC Metadata Injector (AIGC 元数据注入器)

这是一个基于 Python 和 ExifTool 的小工具，旨在为 AI 生成的内容（PNG/JPG）自动注入符合行业标准的 AIGC 结构化元数据。通过该工具，你可以将生产 ID、预留码及来源信息直接嵌入图像文件的 XMP 隐形数据区块中。

## ✨ 功能特性
* **多格式支持**：完美支持 PNG格式。
* **动态配置**：根据文件格式自动生成 ExifTool 临时配置文件。
* **XMP 合规**：针对 JPG 使用 `XMP-dc` 命名空间，针对 PNG 使用 `TextualData` 结构。
* **自动化处理**：支持 JSON 格式的 AIGC 字典数据自动序列化与转义。

## 🛠️ 前置条件
在运行脚本之前，请确保你的系统中已安装 **ExifTool**。

* **Windows**: [下载 ExifTool](https://exiftool.org/)，并重命名为 `exiftool.exe` 放入系统 Path 或脚本根目录。
* **macOS**: `brew install exiftool`
* **Linux**: `sudo apt-get install libimage-exiftool-perl`

## 🚀 快速开始

### 1. 安装依赖
本项目仅使用 Python 标准库，无需额外执行 `pip install`，但需确保 `exiftool` 命令在终端可调用。

### 2. 修改配置
在 `main` 函数中修改你的 `aigc_info` 字典：
```python
aigc_info = {
    "Label": "1",
    "ContentProducer": "你的ID",
    "ProduceID": "唯一生成标识",
    # ... 其他字段
}
