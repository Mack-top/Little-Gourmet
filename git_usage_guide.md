# Git 使用完整指南

本指南涵盖了从零开始使用 Git 的完整流程，包括初始化仓库、日常提交、问题解决以及自动化工具。

## 目录

1. [从0到1的新项目提交流程](#从0到1的新项目提交流程)
2. [日常开发提交流程](#日常开发提交流程)
3. [自动提交工具](#自动提交工具)
4. [常见问题及解决方案](#常见问题及解决方案)
5. [最佳实践](#最佳实践)

## 从0到1的新项目提交流程

### 1. 创建项目目录

```bash
mkdir my-new-project
cd my-new-project
```

### 2. 初始化Git仓库

```bash
git init
```

### 3. 配置用户信息

```bash
# 为当前项目配置
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 或全局配置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. 创建项目文件

```bash
echo "# My New Project" > README.md
touch main.py
mkdir src docs
```

### 5. 检查Git状态

```bash
git status
```

### 6. 添加文件到暂存区

```bash
# 添加所有文件
git add .

# 或选择性添加特定文件
git add README.md main.py
```

### 7. 首次提交

```bash
git commit -m "Initial commit"
```

### 8. 关联远程仓库

```bash
# HTTPS方式
git remote add origin https://github.com/username/my-new-project.git

# SSH方式（推荐）
git remote add origin git@github.com:username/my-new-project.git
```

### 9. 首次推送（设置上游分支）

```bash
git push -u origin master
```

## 日常开发提交流程

在项目创建完成后，日常开发遵循以下流程：

```bash
# 1. 修改代码
# 编辑文件...

# 2. 检查更改状态
git status

# 3. 添加更改到暂存区
git add .

# 4. 提交更改
git commit -m "描述本次更改的内容"

# 5. 推送到远程仓库
git push
```

### 更详细的日常流程

```bash
# 查看具体更改内容
git diff

# 添加特定文件到暂存区
git add file1.py file2.py

# 或添加所有更改
git add .

# 提交更改（编写有意义的提交信息）
git commit -m "实现用户登录功能"

# 推送到远程仓库
git push origin master
```

## 自动提交工具

为了简化日常Git操作，项目提供了以下自动提交工具：

### Python 脚本（跨平台）

文件：[auto_commit.py](file:///d:/0000_AI/Little-Gourmet/auto_commit.py)

使用方法：
```bash
python auto_commit.py "提交信息"
```

如果没有提供提交信息，脚本会提示输入。

### Windows 批处理脚本

文件：[quick_commit.bat](file:///d:/0000_AI/Little-Gourmet/quick_commit.bat)

使用方法：
```cmd
quick_commit.bat "提交信息"
```

### Bash 脚本

文件：[quick_commit.sh](file:///d:/0000_AI/Little-Gourmet/quick_commit.sh)

使用方法：
```bash
./quick_commit.sh "提交信息"
```

## 常见问题及解决方案

### 1. 分支名称不匹配

推送时确保本地分支名称与远程仓库匹配：
```bash
# 如果远程使用main而不是master
git push -u origin master:main
```

### 2. 远程仓库已存在错误

错误提示：`error: remote origin already exists.`

解决方案：无需重复添加远程仓库，直接使用推送命令：
```bash
git push
```

### 3. 网络连接失败

遇到`Failed to connect to github.com`错误时：

```bash
# 配置HTTP代理
git config --global http.proxy http://proxy.server:port

# 配置HTTPS代理
git config --global https.proxy https://proxy.server:port

# 清除代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 4. Recv failure: Connection was reset

建议改用 SSH 方式进行推送：

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 启动ssh-agent并添加私钥
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# 更改远程仓库URL为SSH方式
git remote set-url origin git@github.com:username/repository.git

# 推送代码
git push -u origin master
```

### 5. 强制推送与分支同步

如果标准推送失败（提示非快进更新）：

```bash
# 强制推送本地master分支到远程main分支
git push origin master:main --force
```

注意：强制推送会覆盖远程分支的历史记录，应谨慎使用。

## 最佳实践

### 1. 提交信息规范

编写清晰、有意义的提交信息：
- 使用祈使句，如"添加用户登录功能"而不是"添加了用户登录功能"
- 第一行简要描述更改，后续行详细说明（如有必要）
- 避免无意义的提交信息如"修复"、"更新"等

### 2. 频繁小步提交

- 每次提交保持逻辑相关且改动范围明确
- 避免一次提交包含过多不相关的更改
- 在完成一个功能或修复一个bug后及时提交

### 3. .gitignore配置

创建`.gitignore`文件排除不需要版本控制的文件：
```
# 虚拟环境
.venv/
venv/
env/

# 编译产物
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE配置
.vscode/
.idea/

# 操作系统文件
.DS_Store
Thumbs.db
```

### 4. 定期推送

确保代码变更及时备份到远程仓库：
```bash
git push
```

### 5. 使用分支

对于新功能或实验性开发，使用分支：
```bash
# 创建并切换到新分支
git checkout -b new-feature

# 在分支上开发...

# 切换回主分支
git checkout master

# 合并分支
git merge new-feature

# 删除已合并的分支
git branch -d new-feature
```