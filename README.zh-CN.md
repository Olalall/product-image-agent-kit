# Product Image Agent Kit

本地优先的电商商品图 AI 工作流工具包：**商品 CSV 输入**、**素材图扫描**、**prompt 规划**、**mock 商品图生成**、**QA 报告**、**运行日志**、**交付包导出**，并在真实上传/发布前设置人工确认安全门。

[English README](README.md) · [中文项目介绍话术](docs/project-introduction.zh-CN.md)

![Product Image Agent Kit 报告截图](docs/screenshots/report-demo.png)

## 这个项目解决什么问题

很多 AI 图片项目只演示“生成一张图”。但真实商品图工作流还需要：

- 检查商品表格字段是否完整；
- 匹配 SKU 和素材图；
- 规划图片生成 prompt；
- 批量输出可检查结果；
- 记录每一步日志；
- 生成 QA 报告；
- 打包交付；
- 避免误上传、误覆盖、误发布。

Product Image Agent Kit 关注的是这套“图片生成前后”的可控流程，而不是单纯替代图片模型。

## 30 秒运行

```powershell
git clone https://github.com/Olalall/product-image-agent-kit.git product-image-agent-kit
cd product-image-agent-kit
python -m pip install -e .
python -m product_image_agent.cli demo --clean --out runs\demo
```

打开：

```text
runs/demo/report.html
```

预期结果：

```text
found=3 generated=3 failed=0 moved=3 skipped=1 blocked=1
```

其中 `blocked=1` 是故意设计的：示例里有一条 live publish 请求，用来证明安全门会拦截真实发布动作。

## 输出文件怎么看

```text
runs/demo/
  report.html       # 给人看的可视化报告
  report.md         # 轻量交付说明
  manifest.json     # 结构化运行清单
  qa_report.json    # QA 检查结果
  events.jsonl      # 每一步事件日志
  prompts/          # 每个 SKU 的 prompt
  mock_outputs/     # mock 商品图 SVG
  package.zip       # 可交付压缩包
```

## 适合谁

- 想做电商商品图自动化的人；
- 想学习 AI 应用工程的人；
- 想做 AI Agent / workflow 作品集的人；
- 想先用 mock 流程验证逻辑，再接真实图片 API 的开发者。

## 不适合谁

- 想直接一键上传 Amazon / Shopify 的人；
- 想找现成图片生成模型的人；
- 想直接处理真实客户数据、真实商品素材的人；
- 不关心 QA、日志、安全门，只想看一张生成图的人。

## 安全边界

默认 demo：

- 不需要 API key；
- 不调用付费图片 API；
- 不上传外部系统；
- 不删除、覆盖、发布真实素材；
- 只使用合成示例数据。

如果未来接入真实 provider，必须显式加入成本确认和人工确认，例如：

```powershell
python -m product_image_agent.cli run --provider openai --confirm-cost ...
```

## 示例数据

查看：

```text
examples/README.md
```

里面说明了：

- `products.csv` 每列含义；
- 3 个 demo SKU 分别演示什么；
- 为什么 blocked 是预期结果；
- 如何换成你自己的 mock 商品。

## 贡献

贡献前先看：

```text
CONTRIBUTING.md
```

适合新手的方向：

- JSON 输入适配；
- Shopify CSV 模板；
- Amazon 图片包模板；
- 更多 QA 规则；
- report.html 截图自动化；
- 真实 provider adapter 的安全接口设计。

## 关于 MIT License

GitHub 页面在中文自动翻译时，可能会把 `MIT license` 翻译成“麻省理工学院”。这里的 MIT 指的是 MIT 开源许可证，不代表本项目由麻省理工学院创建、赞助、维护或背书。

## License

MIT
