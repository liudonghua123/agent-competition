# 智能体大赛网站

基于 Python FastAPI + Vue3/Vite/TailwindCSS 开发的智能体创新大赛管理系统。

## 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **数据库**: SQLite (默认) / MySQL / PostgreSQL
- **认证**: JWT + 统一身份认证 (SSO)
- **依赖管理**: uv

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 8
- **UI框架**: TailwindCSS 4
- **状态管理**: Pinia
- **路由**: Vue Router

## 功能模块

### 前台功能

#### 1. 首页 / 作品展览
- 展示大赛主题、参赛作品
- 支持投票（每人每天5票，可投不同作品）
- 公开访问，无需登录

#### 2. 统一身份认证登录
- 支持 SSO Header 自动获取用户信息
- 支持授权码登录
- 首次登录自动创建用户（默认为普通用户）

#### 3. 内容发布
- 支持 Markdown/HTML 可视化编辑
- 支持预览
- 一键生成静态页面
- 前台显示静态页面

### 后台管理

#### 1. 用户管理
- 角色：普通用户、评审用户、超级用户
- 统一身份认证登录自动创建用户
- 启用/禁用用户
- 修改用户角色

#### 2. 权限管理 (RBAC)
- 基于角色的访问控制
- 超级用户：全部权限
- 评审用户：审核、评审、日志
- 普通用户：报名、提交作品、投票

#### 3. 队伍管理
- 创建队伍（队名、描述、成员）
- 成员1-5人，队长+队员
- 学工号、姓名验证
- 重复组队检测
- 审核功能（评审/超级用户）

#### 4. 作品管理
- 队长管理作品信息
- 每队最多5个作品
- 作品信息：
  - 名称
  - 描述
  - 主题（下拉选择）
  - 智能体URL
  - 智能体编排URL
  - PDF文档（≤10MB）
  - 演示视频（≤50MB）

#### 5. 评审管理
- 专家打分（0-100分）
- 评价功能
- 筛选过滤：
  - 按队伍名称
  - 按作品名称
  - 按是否已打分
- 快捷操作：
  - 点击URL新窗口打开
  - PDF/MP4弹窗显示/播放
  - 打分、输入评价
  - 保存、详情按钮

#### 6. 内容管理
- 首页内容编辑
- 栏目管理
- 内容管理
- Markdown/HTML双模式编辑
- 实时预览
- 静态页面生成

#### 7. 配置管理
- 每人每天投票数
- 队伍最大成员数
- 每队最大作品数
- 比赛主题名称
- 比赛主题描述
- 报名开始/结束时间
- 作品提交截止时间

#### 8. 日志管理
- 登录日志
- 操作日志（新增/编辑/删除）
- 按时间、操作用户、操作类型筛选

## 数据库设计

### 用户表 (users)
```sql
- id: 主键
- username: 用户名（唯一）
- nickname: 昵称
- email: 邮箱
- hashed_password: 密码哈希
- role: 角色 (user/reviewer/admin)
- auth_source: 认证来源 (local/unified)
- is_active: 是否启用
- created_at: 创建时间
- updated_at: 更新时间
```

### 队伍表 (teams)
```sql
- id: 主键
- name: 队名
- description: 描述
- leader_id: 队长用户ID
- status: 状态 (pending/approved/rejected)
- created_at: 创建时间
- updated_at: 更新时间
```

### 队伍成员表 (team_members)
```sql
- id: 主键
- team_id: 队伍ID
- user_id: 用户ID
- student_id: 学工号
- name: 姓名
- is_leader: 是否队长
- created_at: 创建时间
```

### 作品表 (works)
```sql
- id: 主键
- team_id: 队伍ID
- name: 作品名称
- description: 描述
- theme: 主题
- agent_url: 智能体URL
- agent_editor_url: 智能体编排URL
- pdf_file: PDF文件路径
- video_file: 视频文件路径
- vote_count: 投票数
- score: 评审分数
- status: 状态 (pending/approved/rejected)
- created_at: 创建时间
- updated_at: 更新时间
```

### 投票表 (votes)
```sql
- id: 主键
- user_id: 用户ID
- work_id: 作品ID
- created_at: 投票时间
```

### 评审表 (reviews)
```sql
- id: 主键
- work_id: 作品ID
- user_id: 评审用户ID
- score: 分数 (0-100)
- comment: 评价
- created_at: 创建时间
- updated_at: 更新时间
```

### 内容表 (contents)
```sql
- id: 主键
- title: 标题
- slug: 别名（URL）
- type: 类型 (page/category/post)
- content: 内容
- content_format: 内容格式 (markdown/html)
- parent_id: 父级ID
- order: 排序
- is_published: 是否发布
- created_at: 创建时间
- updated_at: 更新时间
```

### 配置表 (settings)
```sql
- id: 主键
- key: 键
- value: 值
- description: 描述
- created_at: 创建时间
- updated_at: 更新时间
```

### 日志表 (logs)
```sql
- id: 主键
- user_id: 用户ID
- action: 操作类型
- resource: 资源类型
- details: 详情
- ip_address: IP地址
- created_at: 创建时间
```

## 项目结构

```
agent-competition/
├── backend/
│   ├── app/
│   │   ├── api/            # API路由
│   │   │   ├── auth.py     # 认证
│   │   │   ├── users.py    # 用户管理
│   │   │   ├── teams.py    # 队伍管理
│   │   │   ├── works.py    # 作品管理
│   │   │   ├── reviews.py  # 评审管理
│   │   │   ├── contents.py # 内容管理
│   │   │   ├── settings.py # 配置管理
│   │   │   └── logs.py     # 日志管理
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 配置
│   │   │   ├── database.py # 数据库
│   │   │   └── security.py # 安全/JWT
│   │   ├── models/         # 数据模型
│   │   │   ├── user.py
│   │   │   ├── team.py
│   │   │   ├── work.py
│   │   │   ├── content.py
│   │   │   └── setting.py
│   │   └── schemas/        # Pydantic schemas
│   ├── main.py             # 应用入口
│   ├── init_db.py          # 数据库初始化
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/            # API调用
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   │   ├── admin/      # 管理后台
│   │   │   ├── HomePage.vue
│   │   │   ├── WorksPage.vue
│   │   │   ├── LoginPage.vue
│   │   │   └── ...
│   │   ├── router/         # 路由
│   │   ├── stores/         # Pinia状态
│   │   └── App.vue
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+

### 后端启动

```bash
cd backend

# 安装依赖
uv pip install -e .

# 初始化数据库
uv run python init_db.py

# 启动服务
uv run python main.py
```

后端地址: http://localhost:8000

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端地址: http://localhost:5173

### 登录信息
- 管理员账号: admin / admin123

## 配置说明

### 数据库配置

修改 `backend/app/core/config.py` 或创建 `.env` 文件：

```env
# SQLite (默认)
DATABASE_URL=sqlite:///./agent_competition.db

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### JWT密钥

```env
SECRET_KEY=your-secret-key-change-in-production
```

## API 文档

启动后端后访问: http://localhost:8000/docs

## 统一身份认证配置

支持两种模式：

1. **SSO Header 模式**：从 HTTP Header 获取用户信息
   - X-Remote-User: 用户名
   - X-Remote-Nickname: 昵称
   - X-Remote-Email: 邮箱

2. **授权码模式**：使用授权码获取用户信息
   - 格式：`username|nickname|email`

## 页面预览

### 前台
- 首页：渐变背景、动画效果、统计卡片、大赛流程
- 作品展览：卡片布局、投票功能、分页
- 登录页：现代化设计、图标输入框

### 后台
- 仪表盘：数据统计、最近操作
- 管理页面：列表、详情、编辑、审核功能