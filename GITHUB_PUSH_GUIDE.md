# GitHub 推送指南

## 当前状态
✅ 代码已提交到本地 git 仓库
⏳ 待推送到 GitHub

## 推送步骤

### 1. 创建 GitHub 仓库
在 GitHub 上创建新仓库：
- 仓库名：`ai-content-factory`
- 可见性：Private 或 Public（根据需要）
- 不要初始化 README（我们已经有代码了）

### 2. 配置认证
**方式 1：使用 SSH（推荐）**
```bash
# 生成 SSH key（如果没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加 SSH key 到 GitHub
# 访问：https://github.com/settings/keys
# 复制 ~/.ssh/id_ed25519.pub 内容

# 切换 remote 为 SSH
git remote set-url origin git@github.com:admin/ai-content-factory.git
```

**方式 2：使用 Personal Access Token**
```bash
# 在 GitHub 创建 Token
# 访问：https://github.com/settings/tokens
# 权限：repo (Full control of private repositories)

# 推送时使用 token 代替密码
git push -u origin main
# 输入用户名，密码处填写 token
```

### 3. 推送代码
```bash
cd /home/admin/.openclaw/workspace/ai-content-factory
git branch -M main
git push -u origin main
```

### 4. 验证推送
访问 GitHub 仓库确认代码已推送成功。

---

## 当前提交记录
- Commit: `5c76380`
- 文件数：39 个
- 代码量：2752 行
- 提交信息：feat: AI 内容工厂 v1.0 初始版本

---

## 后续更新
```bash
cd /home/admin/.openclaw/workspace/ai-content-factory
git add -A
git commit -m "feat: 更新说明"
git push
```
