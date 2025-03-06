import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from web3_test_framework.core.account.manager import Manager
from web3_test_framework.core.account.wallet import Wallet

# @pytest.fixture
# def manager():
#     with patch('src.core.account.manager.ConfigLoader') as mock_config_loader, \
#          patch('src.core.account.wallet.Wallet') as mock_wallet:
#         mock_config_loader.return_value.load_accounts.return_value = {
#             "account1": {"address": "0xc48BF222123b8e00C36d43B24375132ECC2467F8", "private_key": "01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec"},
#             "account2": {"address": "0x70359Aa1E05A56d2a055079316866Bef98C09817", "private_key": "5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575"}
#         }
#         mock_wallet.generate.side_effect = [
#             Wallet(address="0x4fa2Eaf521811f241F1D0d06Fd7Fb4E66eDeAD82", private_key="0x35325898660ada2c9e6844a01bedde334f9bfcc10fcb243ba6ce08c2e660ae2e", alias="temp_0"),
#             Wallet(address="0x32C1f150A5845b05cBb731B13AF5e44a531e8489", private_key="0xb75568a6357c374dd714a17adc71063199942e4fdb49df2793dbe8bf5e811a5d", alias="temp_1"),
#             Wallet(address="0x9452714F62E246B9A0E707f5CCf0F75194517D6f", private_key="0xf2b0fbbbaa10a855ad92017cf171ae3df2b3b308b0933b45d4938d90abc4b5df", alias="temp_2")
#         ]
#         manager = Manager("test_project", "test")
#     return manager


@pytest.fixture
def manager():
    with patch("src.core.account.manager.ConfigLoader") as mock_config_loader:
        with patch("src.core.account.manager.Wallet") as mock_wallet:
            manager = Manager("test_project")
            yield manager


@patch("src.core.account.manager.Wallet.generate_batch")
def test_create_batch_accounts(mock_generate_batch, manager):
    mock_generate_batch.return_value = [
        Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="batch1_1"),
        Wallet(address="0x70359Aa1E05A56d2a055079316866Bef98C09817", private_key="5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575", alias="batch1_2")
    ]
    wallets = manager.create_batch_accounts(2, "batch1")
    assert len(wallets) == 2
    assert "batch1_1" in manager._wallets
    assert "batch1_2" in manager._wallets


@patch("src.core.account.manager.Wallet.load_batch")
def test_get_batch_accounts(mock_load_batch, manager):
    mock_load_batch.return_value = [
        Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="batch1_1"),
        Wallet(address="0x70359Aa1E05A56d2a055079316866Bef98C09817", private_key="5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575", alias="batch1_2")
    ]
    wallets = manager.get_batch_accounts("batch1")
    assert len(wallets) == 2
    assert "batch1_1" in [w.alias for w in wallets]
    assert "batch1_2" in [w.alias for w in wallets]


def test_get_wallet(manager):
    wallet = Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="test_wallet")
    manager._wallets["test_wallet"] = wallet
    retrieved_wallet = manager.get_wallet("test_wallet")
    assert retrieved_wallet == wallet


def test_get_all_wallets(manager):
    wallet1 = Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="wallet1")
    wallet2 = Wallet(address="0x70359Aa1E05A56d2a055079316866Bef98C09817", private_key="5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575", alias="temp_wallet")
    manager._wallets["wallet1"] = wallet1
    manager._wallets["temp_wallet"] = wallet2
    wallets = manager.get_all_wallets()
    assert wallet1 in wallets
    assert wallet2 not in wallets


def test_add_wallet(manager):
    wallet = Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="new_wallet")
    manager.add_wallet(wallet)
    assert "new_wallet" in manager._wallets


@patch("src.core.account.manager.Wallet.generate_batch")
def test_dump_temp_accounts(mock_generate_batch, manager):
    mock_generate_batch.return_value = [
        Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="temp_1", keyfile_path=Path("temp_1.json"))
    ]
    export_dir = Path("./export")
    manager.dump_temp_accounts(export_dir)
    assert (export_dir / "temp_1.json").exists()


@patch("src.core.account.manager.Wallet.load_batch")
def test_load_batch_accounts(mock_load_batch, manager):
    mock_load_batch.return_value = [
        Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="batch1_1"),
        Wallet(address="0x70359Aa1E05A56d2a055079316866Bef98C09817", private_key="5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575", alias="batch1_2")
    ]
    manager._load_batch_accounts()
    assert "batch1_1" in manager._wallets
    assert "batch1_2" in manager._wallets


@patch("src.core.account.manager.Wallet.load_batch", side_effect=Exception("Failed to load"))
def test_load_batch_accounts_exception(mock_load_batch, manager, caplog):
    manager._load_batch_accounts()
    assert "Failed to load" in caplog.text


@patch("src.core.account.manager.ConfigLoader")
def test_load_config_accounts(mock_config_loader, manager):
    mock_config_loader.return_value.load_accounts.return_value = {
        "test_wallet": {"address": "0xc48BF222123b8e00C36d43B24375132ECC2467F8", "private_key": "01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec"}
    }
    manager._load_config_accounts()
    assert "test_wallet" in manager._wallets


@patch("src.core.account.manager.Wallet.generate_batch")
def test_generate_temp_accounts(mock_generate_batch, manager):
    mock_generate_batch.return_value = [
        Wallet(address="0xc48BF222123b8e00C36d43B24375132ECC2467F8", private_key="01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec", alias="temp_1"),
        Wallet(address="0x70359Aa1E05A56d2a055079316866Bef98C09817", private_key="5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575", alias="temp_2")
    ]
    manager._generate_temp_accounts()
    assert "temp_1" in manager._wallets
    assert "temp_2" in manager._wallets


if __name__ == "__main__":
    # 使用pytest运行测试
    pytest.main(['-s', '-v', '--tb=short', __file__])