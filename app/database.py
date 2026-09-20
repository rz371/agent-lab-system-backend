# 只干一件事情 ‘把手机准备好’ 别的文件想用数据库，就得来这里拿工具
from datetime import datetime

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase
from app.config import settings

# 第一步：把数据库地址拿到放到引擎里面 - 引擎是SQLAlchemy的核心对象
#           负责管理数据库驱动和连接池的 ，目前只是初始配置
engine = create_engine(settings.DATABASE_URL) # 创建引擎

# 第二步：只要调用一次 SessionLocal ，那么就是一次session
SessionLocal = sessionmaker( # 配置会话工厂
        bind=engine,
        autocommit=False, 
        autoflush=False, 
    )

# 第三步：真正的创建连接 ,get_db 是规则，真正创建连接的是db = SessionLocal()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 普通写法  Base = declarative_base()
#
# 给 Base新加两个字段，以后继承这个的话，自动有这俩字段
# DeclarativeBase 继承 这个，就Base这个类就获取了ORM能力
# 而 ORM 是 对象关系映射 ，可以用操作python对象的方式来操作数据库
class Base(DeclarativeBase):
    # Mapped[] 就得这么写，是类型标注
    # mapped_column 这一列的细节配置
    id:Mapped[int] = mapped_column(primary_key=True,comment='主键ID')
    # DateTime ： 建表的时候，`create_time`这一列，给我建成**时间类型 DATETIME**，不要存成普通字符串、数字。
    create_time:Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment='创建时间')
    update_time:Mapped[datetime] = mapped_column(
        DateTime,default=datetime.now,onupdate=datetime.now,comment='更新时间')
