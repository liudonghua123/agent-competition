"""Initialize database and create default admin user"""
from app.core.database import init_db, SessionLocal
from app.models.user import User, UserRole
from app.models.setting import Setting
from app.models.permission import Permission, Role, get_default_permissions, get_default_roles


def main():
    print("Initializing database...")
    init_db()
    print("Database tables created.")

    db = SessionLocal()
    try:
        # Initialize permissions and roles
        existing_perms = db.query(Permission).count()
        if existing_perms == 0:
            print("Initializing permissions...")
            for perm_data in get_default_permissions():
                perm = Permission(**perm_data)
                db.add(perm)
            db.commit()
            print(f"Created {len(get_default_permissions())} permissions.")

        # Initialize roles
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            print("Initializing roles...")
            for role_data in get_default_roles():
                permission_codes = role_data.pop("permissions", [])
                role = Role(**role_data)
                db.add(role)
                db.flush()

                # 关联权限
                for perm_code in permission_codes:
                    perm = db.query(Permission).filter(Permission.code == perm_code).first()
                    if perm:
                        role.permissions.append(perm)

            # 为管理员角色添加所有权限
            admin_role = db.query(Role).filter(Role.code == "admin").first()
            if admin_role:
                all_perms = db.query(Permission).all()
                admin_role.permissions = all_perms

            db.commit()
            print(f"Created {len(get_default_roles())} roles.")

        # Create admin user if not exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                nickname="管理员",
                email="admin@example.com",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ePLF3Sp.cqGi",  # admin123
                role=UserRole.ADMIN,
                auth_source="local"
            )
            db.add(admin)
            db.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists.")

        # Initialize default settings
        default_settings = {
            "max_votes_per_day": ("5", "每人每天投票数"),
            "max_team_members": ("5", "队伍最大成员数"),
            "max_works_per_team": ("5", "每队最大作品数"),
            "themes": ("智能问答,Agent工作流,多智能体协作,智能客服,数据分析,内容生成", "作品主题选项(逗号分隔)"),
            "registration_start": ("", "报名开始时间 (ISO格式)"),
            "registration_end": ("", "报名结束时间 (ISO格式)"),
            "submission_end": ("", "作品提交截止时间 (ISO格式)"),
            "competition_theme": ("智能体创新大赛", "智能体主题名称"),
            "competition_description": ("激发创意，展现智能体开发的无限可能", "智能体主题描述")
        }

        for key, (value, desc) in default_settings.items():
            existing = db.query(Setting).filter(Setting.key == key).first()
            if not existing:
                setting = Setting(key=key, value=value, description=desc)
                db.add(setting)

        db.commit()
        print("Default settings initialized.")
        print("Done!")

    finally:
        db.close()


if __name__ == "__main__":
    main()