# 程康华 · IT 实战笔记网站

> 一个持续积累的 Linux 运维、Kubernetes、Python 全栈、数据库与测试/运维自动化实战笔记站点。
> 本站使用 [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建为静态文档站。

---

## 一、项目结构

仓库根目录（即本文件所在目录）下的关键文件与目录：

| 路径 | 说明 |
|------|------|
| `README.md` | 本文件，项目说明 |
| `requirement.txt` | Python 依赖清单（`mkdocs`、`mkdocs-material` 等），用 `pip install -r requirement.txt` 安装 |
| `CNAME` | 自定义域名绑定（GitHub Pages 用） |
| `mkdocs-docs/` | MkDocs 工程目录 |
| `mkdocs-docs/mkdocs.yml` | **站点总配置**：导航（`nav`）、主题、插件、自定义样式等 |
| `mkdocs-docs/mkdocs-docs/` | **文档源目录（docs_dir）**：所有 `.md` 内容与媒体资源 |
| `mkdocs-docs/site/` | **构建产物**：`mkdocs build` 生成的静态网站（无需手改，可忽略） |

文档源目录 `mkdocs-docs/mkdocs-docs/` 内的组成：

| 路径 | 说明 |
|------|------|
| `README.md` | 站点首页（对应顶部 `En` 标签） |
| `extra.css` | 自定义样式（让顶部导航标签在窄屏也横排显示） |
| `_media/` | 站点媒体资源 |
| `python/` | Python 全栈开发笔记（基础、函数模块、面向对象、MySQL、前端、Django、DRF/Vue、路飞、嘤鸣 APP 等） |
| `auto/` | 测试自动化 / 运维自动化笔记 |
| `k8s-note/` | Kubernetes 笔记 2022 版（对应顶部 `k8s-2022` 标签） |
| `k8s-2023/` | Kubernetes 笔记 2023 版（对应顶部 `k8s-2023` 标签） |
| `dba-note/` | 数据库 DBA 笔记（MySQL、Redis、MongoDB 等） |
| `linux/` | Linux 运维笔记 |

> 站点顶部共 **7 个导航标签**：`En` / `python` / `auto` / `k8s-2022` / `k8s-2023` / `dba` / `linux`，每个标签对应上面一个目录。

---

## 二、如何更新内容

### 1. 修改已有笔记
直接编辑 `mkdocs-docs/mkdocs-docs/` 下对应的 `.md` 文件即可。例如改 Linux 基础命令页：
```
mkdocs-docs/mkdocs-docs/linux/linux基础命令.md
```

### 2. 新增一篇笔记
1. 在对应栏目目录新建 `.md` 文件，例如 `python/我的新笔记.md`；
2. 打开 `mkdocs-docs/mkdocs.yml`，在 `nav:` 下对应栏目里加一行：
   ```yaml
   - 我的新笔记: python/我的新笔记.md
   ```
3. 保存后本地预览即可看到（见下方第三节）。

> 不加入 `nav` 的页面不会被发布；加入后它才会出现在对应标签的侧边栏中。

### 3. 插入图片
把图片放进对应目录的 `assets/` 子目录（没有就新建），在 `.md` 里用相对路径引用：
```
![说明](assets/截图.png)
```
注意：链接里的文件名（含大小写、空格）必须与磁盘文件**完全一致**，否则构建会出现“图片找不到”的 WARNING。

### 4. 本地预览
```bash
cd mkdocs-docs
mkdocs serve
```
浏览器打开 http://127.0.0.1:8000/ 即可实时预览（修改文件会自动刷新）。

### 5. 发布到 GitHub Pages
本站使用 `mkdocs gh-deploy` 一键发布（自动构建并推送到仓库的 `gh-pages` 分支）：
```bash
cd mkdocs-docs
mkdocs gh-deploy
```
- 首次发布会在仓库创建 `gh-pages` 分支并启用 GitHub Pages；
- 之后每次修改只需重新执行该命令，站点即更新；
- 自定义域名由文档源目录中的 `CNAME` 文件控制，发布后会自动生效，无需手动设置。

---

## 三、常见问题

- **依赖怎么装？** 在仓库根执行 `pip install -r requirement.txt`。
- **顶部标签在窄窗口没显示？** 已通过 `extra.css` 让其在窄屏也横排；若仍看不到，请刷新（Ctrl+F5）或重启 `mkdocs serve`。
- **构建出现“图片/链接找不到”的 WARNING？** 通常是源笔记引用了图片但图片没放进对应 `assets/`，不影响构建，把图补到正确路径即可消除。
- **改了 `mkdocs.yml` 没生效？** `mkdocs serve` 会监听配置文件变化并自动重建，刷新浏览器即可；若异常可重启 `mkdocs serve`。
