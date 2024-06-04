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

import java.util.List;

public class rocketmqJmeter {

    // 发送消息
//        public static void main(String[] args) throws Exception {
//            // 初始化一个producer并设置Producer group name
//            DefaultMQProducer producer = new DefaultMQProducer("qgc_producer_name"); //（1）
//            // 设置NameServer地址
//            producer.setNamesrvAddr("18.162.126.78:9876");  //（2）
//            // 启动producer
//            producer.start();
//            for (int i = 0; i < 100; i++) {
//                // 创建一条消息，并指定topic、tag、body等信息，tag可以理解成标签，对消息进行再归类，RocketMQ可以在消费端对tag进行过滤
//                Message msg = new Message("qgc_TopicTest" /* Topic */,
//                        "qgc_TagA" /* Tag */,
//                        ("Hello RocketMQ " + i).getBytes(RemotingHelper.DEFAULT_CHARSET) /* Message body */
//                );   //（3）
//                // 利用producer进行发送，并同步等待发送结果
//                SendResult sendResult = producer.send(msg);   //（4）
//                System.out.printf("%s%n", sendResult);
//            }
//            // 一旦producer不再使用，关闭producer
//            producer.shutdown();
//        }

    // 消费消息Lite Pull Consumer
    public static volatile boolean running = true;
    public static void main(String[] args) throws Exception {
        DefaultLitePullConsumer litePullConsumer = new DefaultLitePullConsumer("qgc_consumer_name");
        litePullConsumer.setNamesrvAddr("18.162.126.78:9876");
        litePullConsumer.subscribe("qgc_TopicTest", "*");
        litePullConsumer.setPullBatchSize(20);
        litePullConsumer.start();
        try {
            while (running) {
                List<MessageExt> messageExts = litePullConsumer.poll();
                System.out.printf("%s%n", messageExts);
            }
        } finally {
            litePullConsumer.shutdown();
        }
    }
}
