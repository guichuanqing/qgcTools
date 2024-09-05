package com.qgc.maven;

import org.apache.rocketmq.client.consumer.DefaultLitePullConsumer;
import org.apache.rocketmq.client.consumer.DefaultMQPushConsumer;
import org.apache.rocketmq.client.consumer.listener.ConsumeConcurrentlyContext;
import org.apache.rocketmq.client.consumer.listener.ConsumeConcurrentlyStatus;
import org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently;
import org.apache.rocketmq.client.exception.MQClientException;
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.common.message.MessageExt;
import org.apache.rocketmq.remoting.common.RemotingHelper;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.util.List;

public class rocketmqJmeter {
    public static volatile boolean running = true;

    // 发送消息
    public static void main(String[] args) throws Exception {
        // 初始化一个producer并设置Producer group name
        DefaultMQProducer producer = new DefaultMQProducer("qgc_producer_name"); //（1）
        // 设置NameServer地址
        producer.setNamesrvAddr("18.162.126.78:9876");  //（2）
        // 启动producer
        producer.start();
        for (int i = 0; i < 1; i++) {
            Date date = new Date();
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy年MM月dd日 HH时mm分ss秒");
            String currentTime = sdf.format(date);
            String originMsg = "{\"buyerAddress\":\"0xb270b2fa0c9033f1d81fc418fbeec99fe0182f50\",\"numbers\":[{\"number\":\"\",\"price\":19.9,\"tbaAccount\":\"0x8adcca160f8374c8a04f8d7846955a3fa93c1f87\"}],\"timestamp\":1718431824000,\"uid\":1729102500008869888}";
            String LotteryDrawingMessage = "{\"round\":2,\"winners\":[{\"awardType\":\"SECOND\",\"desc\":\"tba账户:0x1f6f5d24cd196d6862c77937195c8cdfeb806e3a获得二等奖,发放2.28奖励\",\"prize\":\"2.28\",\"tbaAccount\":\"0x1f6f5d24cd196d6862c77937195c8cdfeb806e3a\"},{\"awardType\":\"FIRST\",\"desc\":\"tba账户:0xa8268b9511ca581afe1dab0bfc3937c1ffcfebc6获得一等奖,发放9.12奖励\",\"prize\":\"9.12\",\"tbaAccount\":\"0xa8268b9511ca581afe1dab0bfc3937c1ffcfebc6\"}]}";
            String LotteryDrawingResultMessage ="{\"quota\":0,\"round\":3}";
            // 创建一条消息，并指定topic、tag、body等信息，tag可以理解成标签，对消息进行再归类，RocketMQ可以在消费端对tag进行过滤
//                Message msg = new Message("qgc_TopicTest" /* Topic */,
//                        "qgc_TagA" /* Tag */,
//                        ("Hello RocketMQ " + i +" " + currentTime).getBytes(RemotingHelper.DEFAULT_CHARSET) /* Message body */
//                );   //（3）

            Message msg = new Message("qgc_TopicTest", "", LotteryDrawingMessage.getBytes(RemotingHelper.DEFAULT_CHARSET));
            // 利用producer进行发送，并同步等待发送结果
            SendResult sendResult = producer.send(msg);   //（4）
            System.out.printf("{\"code\": \"200\", \"SendResult\" : %s}", sendResult);
        }
        // 一旦producer不再使用，关闭producer
        producer.shutdown();
    }

//消费消息Lite Pull Consumer

//            DefaultLitePullConsumer litePullConsumer = new DefaultLitePullConsumer("qgc_consumer_name");
//            litePullConsumer.setNamesrvAddr("18.162.126.78:9876");
//            litePullConsumer.subscribe("qgc_TopicTest", "*");
//            litePullConsumer.setPullBatchSize(1);
//            litePullConsumer.start();
//            try {
//                while (running) {
//                    List<MessageExt> messageExts = litePullConsumer.poll();
//                    System.out.printf("%s%n", messageExts);
//                }
//            } finally {
//                litePullConsumer.shutdown();
//            }



}
