package com.qgc.functions;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
//import java.security.*;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.jmeter.engine.util.CompoundVariable;
import org.apache.jmeter.functions.InvalidVariableException;
import org.apache.jmeter.samplers.Sampler;
import org.web3j.crypto.*;
//import org.web3j.utils.Numeric;
import org.apache.jmeter.functions.AbstractFunction;

public class App extends AbstractFunction {

    //定义一个obect对象去接受传入变量值
    private Object[] values;
    //存储第一个和第二个参数
    private CompoundVariable type, privateKey;

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
        type = (CompoundVariable) values[0];
        privateKey = (CompoundVariable) values[1];

        if (type.execute().equals("3")){
            try {
                String address = getKeyAddress(privateKey.execute());
                return address;
            }
            catch (Exception e){
                e.printStackTrace();
            }

        }
        else {
            try {
                String str = getRandomAddress(type.execute());
                return str;
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
        return "__qgcWalletApp";
    }

    @Override
    /**
     * 函数描述，获取参数描述
     * @return
     */
    public List<String> getArgumentDesc() {
        List desc = new ArrayList();
        //界面上显示两行参数描述
        desc.add("type(1随机返回私钥，2随机返回地址，3返回指定私钥的地址)");
        desc.add("privateKey(type为3的时候传)");

        return desc;
    }

    public static String getKeyAddress(String privateKey) throws Exception {
        // 生成随机的私钥
//        SecureRandom secureRandom = new SecureRandom();
//        byte[] privateKeyBytes = new byte[32];
//        secureRandom.nextBytes(privateKeyBytes);
//        String privateKey = Numeric.toHexStringNoPrefix(privateKeyBytes);
//        String privateKey = "1f55cff019296e2f627cfc7cd1af2338a57c463ccda82a1bdb4489eef6ad25a3";

        // 通过私钥生成公钥和地址
        if (privateKey !=null || privateKey.equals("")){
            String address = null;
            try {
                ECKeyPair keyPair = ECKeyPair.create(new BigInteger(privateKey, 16));
//              String publicKey = keyPair.getPublicKey().toString(16);
                address = "0x" + Keys.getAddress(keyPair.getPublicKey());
                // 输出私钥、公钥和地址
//            System.out.println("私钥：" + privateKey);
//            System.out.println("公钥：" + publicKey);
//            System.out.println("地址：" + address);
            }
            catch (Exception e){
                throw new InvalidVariableException(e);
            }
            finally {
                return address;
            }
        }
        else {
            System.out.println("privateKey不合法！");
            return null;
        }
    }


    public static String getRandomAddress(String type) throws Exception {
            // 生成随机的ECKeyPair
            ECKeyPair ecKeyPair = Keys.createEcKeyPair();

            // 根据ECKeyPair生成Credentials对象
            Credentials credentials = Credentials.create(ecKeyPair);

            // 输出生成的私钥和地址
            if (type.equals("1")){
            String privateKey = credentials.getEcKeyPair().getPrivateKey().toString(16);
//                System.out.println("Private Key: " + privateKey);
                return privateKey;
            }
            else if (type.equals("2")){
                String address = credentials.getAddress();
//                System.out.println("Address: " + address);
                return address;
            }
            else {
                return null;
            }
    }

}
