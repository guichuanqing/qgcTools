package com.qgc.Web3Sign;
import org.web3j.crypto.Credentials;
import org.web3j.utils.Numeric;
//import java.math.BigDecimal;
//import java.math.BigInteger;
//import java.util.concurrent.ExecutionException;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.jmeter.engine.util.CompoundVariable;
import org.apache.jmeter.functions.InvalidVariableException;
import org.apache.jmeter.samplers.Sampler;
import org.web3j.crypto.*;
import org.apache.jmeter.functions.AbstractFunction;

public class App extends AbstractFunction {

    //定义一个obect对象去接受传入变量值
    private Object[] values;
    //存储第一个和第二个参数
    private CompoundVariable signMessage, privateKey;

    @Override
    /**
     * 执行方法
     * @param sampleResult
     * @param sampler
     * @return
     * @throws InvalidVariableException
     */
    public String execute(SampleResult sampleResult, Sampler sampler) throws InvalidVariableException {
        //接住第一个参数值
        signMessage = (CompoundVariable) values[0];
        privateKey = (CompoundVariable) values[1];

        if (signMessage.execute() != null && !signMessage.execute().isEmpty()){
            try {
//                String address = getKeyAddress(privateKey.execute());
                String signature = signMessage(privateKey.execute(), signMessage.execute());
                return signature;
            }
            catch (Exception e){
                e.printStackTrace();
            }

        }
        return null;
    }

    @Override
    /**
     * 设置参数，接受用户传递的参数
     * @param collection
     * @throws InvalidVariableException
     */
    public void setParameters(Collection<CompoundVariable> collection) throws InvalidVariableException {
        //检查参数是否合法
        checkParameterCount(collection,2);
        //转换成数组
        values = collection.toArray();
    }

    @Override
    /**
     * 函数名称
     * @return
     */
    public String getReferenceKey() {
        System.out.println("-----------------init：" );
        return "qgcWalletSign";
    }

    @Override
    /**
     * 函数描述，获取参数描述
     * @return
     */
    public List<String> getArgumentDesc() {
        List desc = new ArrayList();
        //界面上显示两行参数描述
        desc.add("message：需要签名的字符串");
        desc.add("privateKey：私钥");
        System.out.println("私钥：111" );
        return desc;
    }

    public static String signMessage(String privateKey, String message) throws Exception {
        // 创建Credentials对象
        Credentials credentials = Credentials.create(privateKey);
        // 计算消息的哈希值
        byte[] messageHash = Hash.sha3(message.getBytes());
        // 使用私钥对消息哈希进行签名
        Sign.SignatureData signatureData = Sign.signMessage(messageHash, credentials.getEcKeyPair());
        // 将签名结果编码为Hex字符串
        String signature = Numeric.toHexString(signatureData.getR()) + Numeric.toHexString(signatureData.getS()) + Numeric.toHexString(signatureData.getV());
        return signature;
    }
}