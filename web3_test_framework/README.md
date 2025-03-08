##目录结构
```markdown
web3_test_framework/                  # 项目根目录
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
│   ├── ask/                 # Dapp项目名
│   │   └── test_user_api.py
│
├── conftest.py              # Pytest全局fixture
├── pyproject.toml           # 项目依赖配置
└── README.md                # 项目文档
```

###创建处理器自动加载ABI（名称为项目名+合约名.json，约定默认abi存放路径）
```python
from web3 import Web3
from core.account import Wallet
from core.contract.handler import ContractHandler

# 初始化
w3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = Wallet.from_private_key("0x...")

try:
    # 创建处理器（自动加载ABI）
    handler = ContractHandler(
        w3=w3,
        wallet=wallet,
        project="ask",              # 对应test/ask目录
        contract_name="ERC20",      # 自动查找ERC20_abi.json
        contract_address="0x123..."
    )
except FileNotFoundError as e:
    print(e)

# 调用合约方法
balance = handler.call("balanceOf", wallet.address)
print(f"余额: {balance}")
```
###基础调用链路使用:
```python
from web3 import Web3
from core.account.wallet import Wallet
from core.transaction.builder import TransactionBuilder
from core.transaction.sender import TransactionSender

# 初始化组件
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=..., abi=...)
wallet = Wallet.from_private_key("0x...")
builder = TransactionBuilder(w3)
sender = TransactionSender(w3)

# 构建合约调用交易
tx_data = builder.build(
    func=contract.functions.transfer("0x...", 100),
    sender=wallet.address,
    gas_strategy="high"
)

# 签名并发送
signed_tx = wallet.sign_transaction(tx_data)
receipt = sender.send_and_confirm(signed_tx)

print(f"Tx confirmed in block {receipt.blockNumber}")
```
###handler.py的使用
1. 初始化合约处理器
```python
from web3 import Web3
from core.account import Wallet
from core.contract.handler import ContractHandler

w3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = Wallet.from_private_key("0x...")

# 加载合约
erc20 = w3.eth.contract(
    address="0x...",
    abi=ERC20_ABI
)

# 创建处理器
handler = ContractHandler(
    w3=w3,
    wallet=wallet,
    contract=erc20
)
```
2. 基础调用场景
```python
# 只读调用
balance = handler.call("balanceOf", wallet.address)
print(f"Current balance: {balance}")

# 交易调用（自动处理Gas/Nonce）
result = handler.transact(
    func_name="transfer",
    to_address="0x...",
    amount=100,
    gas_strategy="high"
)

if result["status"] == "success":
    print(f"Tx confirmed in block {result['receipt'].blockNumber}")
else:
    print(f"Transaction failed: {result['error']}")
```
3. 高级使用模式
```python
# 直接访问原始合约方法（需要手动处理）
raw_transfer = handler.functions.transfer("0x...", 100)
tx_data = raw_transfer.build_transaction({
    "from": wallet.address,
    "nonce": handler.builder._get_next_nonce(wallet.address)
})

# 事件监听
transfer_events = handler.events("Transfer", from_block=12345)
for event in transfer_events:
    print(f"Transfer: {event.args}")
```

###工具类转账（ERC20，与ERC721）
```python
# 使用示例
utils = TransferUtils(w3)

# ETH转账
eth_result = utils.send_eth(
    sender=alice_wallet,
    to_address=bob_address,
    amount_wei=Web3.to_wei(0.1, 'ether'),
    gas_strategy="fast"
)

# NFT转账
nft_result = utils.send_erc721(
    sender=alice_wallet,
    contract_address=nft_contract,
    receiver=bob_address,
    token_id=123
)
```