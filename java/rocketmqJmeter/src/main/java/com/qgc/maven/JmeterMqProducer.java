package com.qgc.maven;

import org.apache.jmeter.config.Arguments;
import org.apache.jmeter.protocol.java.sampler.AbstractJavaSamplerClient;
import org.apache.jmeter.protocol.java.sampler.JavaSamplerContext;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.rocketmq.client.exception.MQClientException;
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.client.producer.SendStatus;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.remoting.common.RemotingHelper;
import com.alibaba.fastjson.JSONObject;
import java.io.UnsupportedEncodingException;


public class JmeterMqProducer extends AbstractJavaSamplerClient {
    //这里定义类变量（不能定义为static，会报错）
    private DefaultMQProducer producer;
    private String producerName;
    private String producerGroup;
    private String serverUrl;
    private String topic;
    private String tags;
    private String keys;
    private String body;
    private String delayTime;
    private String timeout;
    private String sendType;
    private long cur_time;
    private byte[] bodyBytes;
    private String orginData;
//    private final Logger log = LogManager.getLogger(JmeterMqProducer.class);

    //这里定义这里作为请求的前置处理
    @Override
    public void setupTest(JavaSamplerContext context) {
        serverUrl = context.getParameter("serverUrl");
        topic = context.getParameter("topic");
        tags = context.getParameter("tags");
        keys = context.getParameter("keys");
        body = context.getParameter("messageBody");
        bodyBytes = body.getBytes();
        producerName = context.getParameter("producerName");
        producerGroup = context.getParameter("producerGroup");
        timeout = context.getParameter("timeout");
        sendType = context.getParameter("sendType");
        delayTime = context.getParameter("delayTime");

        try {
            producer = getProducer(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

    //这里自定义了一个Producer的单例方法
    public DefaultMQProducer getProducer(int type) throws InterruptedException {
        if (producer == null){
            producer = new DefaultMQProducer(producerName);
            if (type == 1){
                System.out.println("=======init producer =====");
                cur_time = System.currentTimeMillis();
            }else {
                System.out.println("=======runtest producer =====");
            }
            producer.setNamesrvAddr(serverUrl); //serverUrl
            // 设置超时时间
            producer.setSendMsgTimeout(Integer.parseInt(timeout));
        }
        try {
            producer.start();
        } catch (MQClientException e) {
            System.out.println("启动init！忽略");
        }
        return producer;
    }

    //这里是一个请求结束的后置处理
    @Override
    public void teardownTest(JavaSamplerContext context) {
        producer.shutdown();
    }

    //这里是一个请求主体执行部分
    @Override
    public SampleResult runTest(JavaSamplerContext context) {

        SampleResult sr = new SampleResult();
        sr.sampleStart();
        Message msg = null;
        try {
            msg = new Message(topic, tags, keys, body.getBytes(RemotingHelper.DEFAULT_CHARSET));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        try {
            JSONObject json = new JSONObject();
            json.put("serverUrl", serverUrl);
            json.put("sendType", sendType);
            json.put("topic", topic);
            json.put("tags", tags);
            json.put("keys", keys);
            json.put("producerName", producerName);
            sr.setRequestHeaders(json.toString());
            sr.setSamplerData(body);
            if ("oneWay".equals(sendType)){
                producer.sendOneway(msg);
                sr.setResponseData("{\"code\": \"200\", \"SendStatus\" : \"success\"}","utf-8");
            }else {
                SendResult sendResult = producer.send(msg);
                sr.setResponseData(sendResult.toString(),"utf-8");
                if(sendResult !=null || sendResult.getSendStatus() == SendStatus.SEND_OK){
                    sr.setResponseData("{\"code\": \"200\", \"SendStatus\" : \"" + sendResult.getSendStatus() + "\",\"MsgId\" : \"" + sendResult.getMsgId() +"\"}","utf-8");
                }
                else {
                    System.err.println(sendResult);
                    sr.setResponseData("{\"code\" : \"500\", \"msg\": \"失败\", \"Error\": \""+ sendResult.toString() +"\"}","utf-8");
                }
            }
        }catch (Exception e){
            e.printStackTrace();
            sr.setResponseData("{\"code\" : \"501\", \"msg\": \"其他失败\", \"Error\": "+ e +"}","utf-8");
            producer.shutdown();

        }
        try {
            sr.setDataType(SampleResult.TEXT);
            sr.setSuccessful(true);
        }catch(Exception e){
            sr.setSuccessful(false);
            e.printStackTrace();
        }
        finally {
            sr.sampleEnd();
        }
        return sr;

    }

    // 给参数填充默认值
    @Override
    public Arguments getDefaultParameters() {
        Arguments params = new Arguments();
        params.addArgument("serverUrl", "18.162.126.78:9876");
        params.addArgument("topic", "");
        params.addArgument("tags", "");
        params.addArgument("keys", "");
        params.addArgument("messageBody", "");
        params.addArgument("producerName", "");
        params.addArgument("producerGroup", "producerGroup");
        params.addArgument("timeout", "6000");
        params.addArgument("sendType", "oneWay");
        params.addArgument("delayTime", "100");

        return params;
    }

    public static void main(String[] args) throws Exception {
        JmeterMqProducer a = new JmeterMqProducer();
        DefaultMQProducer producer = a.getProducer(1);
//        producer.start();
//        for (int i = 0; i < 100; i++) {
//            Message msg = new Message("qgc_TopicTest", "qgc_TagA", ("Hello RocketMQ " + i).getBytes(RemotingHelper.DEFAULT_CHARSET));
//            SendResult sendResult = producer.send(msg);
//            System.out.printf("%s%n", sendResult);
//        }
//        producer.shutdown();
    }
}
