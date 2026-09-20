# 属于项目的配置管家，之后如果需要用的env数据库配置的话，直接来这里拿就行，不需要去env拿

# 1、读取env文件的内容
# 2、做校验，防止漏配置
# 3、给整个项目提供统一入口拿配置，这样其他py文件就不需要读env文件了，导入这个就能拿到



from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 可以定位.env文件在哪里
# __file__ 这个config文件本身
# parent 上一级 app/
# parent.parent 再上一级  backend/ ，所以如果env不是在这个路径下的话，就要修改
BASE_DIR = Path(__file__).resolve().parent.parent

# BaseSettings：项目配置就要继承它，可以读取.env文件
class Settings(BaseSettings):
    DATABASE_URL: str

    # SettingsConfigDict 告诉BaseSettings 用什么样子的规则去加载配置
    # 怎么去读取，去哪里读取
    # model_config 必须得叫这个名字，是pydantic固定协议
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env', # 到这个文件找环境变量
        env_file_encoding='utf-8'

    )

settings = Settings()
