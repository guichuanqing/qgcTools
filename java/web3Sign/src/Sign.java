import org.web3j.crypto.Credentials;
import org.web3j.crypto.RawTransaction;
import org.web3j.crypto.TransactionEncoder;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.DefaultBlockParameterNumber;
import org.web3j.protocol.core.methods.request.Transaction;
import org.web3j.protocol.core.methods.response.EthSendTransaction;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.Transfer;
//import org.web3j.utils.Numeric;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.concurrent.ExecutionException;

public class Sign {
    public static void main(String[] args) throws Exception {

//         钱包私钥
        String privateKey = "your_private_key_here";
        Credentials credentials = Credentials.create(privateKey);

        // 构建要发送的交易
        BigInteger gasPrice = BigInteger.valueOf(20_000_000_000L);
        BigInteger gasLimit = BigInteger.valueOf(4300000);
        BigInteger value = Convert.toWei("1.0", Convert.Unit.ETHER).toBigInteger();
        String toAddress = "0x1234567890123456789012345678901234567890";

        RawTransaction rawTransaction = RawTransaction.createEtherTransaction(
                BigInteger.valueOf(1),
                gasPrice,
                gasLimit,
                toAddress,
                value);

        // 对交易进行签名
        byte[] signedMessage = TransactionEncoder.signMessage(rawTransaction, credentials);
        String hexValue = Numeric.toHexString(signedMessage);

        System.out.println("Signed transaction hash: " + hexValue);
    }
}