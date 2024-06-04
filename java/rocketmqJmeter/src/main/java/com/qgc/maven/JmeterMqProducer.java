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
import sun.awt.windows.WPrinterJob;

import java.util.Random;


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

    //这里定义这里作为请求的前置处理
    @Override
    public void setupTest(JavaSamplerContext context) {
        serverUrl = context.getParameter("serverUrl");
        topic = context.getParameter("topic");
        tags = context.getParameter("tags");
        keys = context.getParameter("keys");
        body = context.getParameter("messageBody");
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
            producer = new DefaultMQProducer(producerGroup);
            if (type == 1){
                System.out.println("=======init producer == null===========");
                cur_time = System.currentTimeMillis();
            }else {
                System.out.println("=======runtest producer == null===========");
            }
            producer.setNamesrvAddr(serverUrl);
            producer.setInstanceName(producerName);
            producer.setVipChannelEnabled(false);
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
        // sr.setRequestHeaders("请求原始的msg_body:"+ orginData); 设置请求头内容
        Message msg = new Message(topic,
                tags,
                keys,
                bodyBytes);
        // msg.getProperties().put("traceparent", "xxx");
        try {
            if ("oneWay".equals(sendType)){
                producer.sendOneway(msg);
                sr.setResponseData("Oneway发送成功","utf-8");
            }else {
                SendResult sendResult = producer.send(msg);
                sr.setResponseData(sendResult.toString(),"utf-8");
                if(sendResult ==null || sendResult.getSendStatus() != SendStatus.SEND_OK){
                    System.err.println(sendResult);
                    sr.setResponseData("{'code' : 1, 'msg': '失败'}","utf-8");
                }
            }
        }catch (Exception e){
            e.printStackTrace();
            sr.setResponseData("{'code' : 2, 'msg': '其他失败啊'}","utf-8");
            producer.shutdown();

        }
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
        params.addArgument("serverUrl", "http://mq.xxx.com");
        params.addArgument("topic", "test_topic");
        params.addArgument("tags", "test_tag");
        params.addArgument("keys", "test_key");
        params.addArgument("messageBody", "test_body");
        params.addArgument("producerName", "test_producerName");
        params.addArgument("producerGroup", "producerGroup");
        params.addArgument("timeout", "6000");
        params.addArgument("sendType", "oneWay");
        params.addArgument("delayTime", "100");

        return params;
    }
}
