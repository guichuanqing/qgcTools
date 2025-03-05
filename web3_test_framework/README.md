pydapptest/                  # 项目根目录
├── contracts/               # Solidity智能合约源文件
│   ├── ERC20/               # 代币合约示例目录
│   │   └── ERC20.sol        # 合约源码
│   └── Marketplace.sol      # 其他业务合约
│
├── artifacts/               # 编译输出目录（自动生成）
│   ├── ERC20/               
│   │   ├── ERC20.json       # 编译产物（包含ABI/bytecode）
│   │   └── ERC20.dbg.json   # 调试信息
│   └── Marketplace.json     
│
├── scripts/                 # 部署和维护脚本
│   ├── deploy.py            # 合约部署入口脚本
│   └── upgrade_contract.py  # 合约升级脚本
│
├── src/                     # 框架核心代码
│   ├── core/                # 区块链核心模块
│   │   ├── blockchain/      
│   │   │   ├── compiler.py  # Solidity编译器
│   │   │   └── deployer.py  # 合约部署器
│   │   ├── account.py       # 账户管理
│   │   └── network.py       # 网络连接
│   │
│   ├── services/            # 中心化服务测试模块
│   │   ├── http_client.py   # REST API测试客户端 
│   │   └── db_client.py     # 数据库测试工具
│   │
│   ├── utils/               # 工具类
│   │   ├── crypto.py        # 加密相关
│   │   └── file_utils.py    # 文件处理
│   │
│   └── config/              # 配置管理
│       ├── __init__.py
│       ├── networks.yaml    # 网络配置
│       └── accounts.yaml    # 账户配置
│
├── tests/                   # 测试用例目录
│   ├── blockchain/          # 合约测试用例
│   │   └── test_erc20.py    
│   ├── api/                 # API接口测试用例
│   │   └── test_user_api.py
│   └── integration/         # 混合测试用例
│       └── test_marketplace.py
│
├── conftest.py              # Pytest全局fixture
├── pyproject.toml           # 项目依赖配置
└── README.md                # 项目文档