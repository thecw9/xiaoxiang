package main

import (
	"encoding/json"
	"fmt"

	"push_layer_go/config"
	"push_layer_go/utils"

	"github.com/IBM/sarama"
	"github.com/robfig/cron/v3"
)

func main() {
	// 初始化配置
	cfg, err := config.NewConfig()
	if err != nil {
		panic(err)
	}
	// print config key: value
	cfgJson, _ := json.MarshalIndent(cfg, "", "  ")
	fmt.Println(string(cfgJson))

	defer cfg.DB.Close()

	// 初始化 Kafka 生产者
	producer, err := sarama.NewSyncProducer([]string{cfg.KafkaBootstrapServers}, nil)
	if err != nil {
		panic(err)
	}
	defer producer.Close()

	// 立即执行一次数据推送
	err = IngestOilChromatography(cfg, producer)
	if err != nil {
		fmt.Println("Error ingesting oil chromatography data:", err)
	}

	err = IngestPartDischarge(cfg, producer)
	if err != nil {
		fmt.Println("Error ingesting part discharge data:", err)
	}

	err = IngestIronCore(cfg, producer)
	if err != nil {
		fmt.Println("Error ingesting iron core data:", err)
	}

	// 设置任务调度
	c := cron.New()
	// 每小时的第 0 分钟执行
	c.AddFunc("0 * * * *", func() {
		err := IngestOilChromatography(cfg, producer)
		if err != nil {
			fmt.Println("Error ingesting oil chromatography data:", err)
		}
	})

	// 每 5 分钟执行一次
	c.AddFunc("@every 5m", func() {
		err := IngestPartDischarge(cfg, producer)
		if err != nil {
			fmt.Println("Error ingesting part discharge data:", err)
		}
	})

	// 每小时的第 0 分钟执行
	c.AddFunc("0 * * * *", func() {
		err := IngestIronCore(cfg, producer)
		if err != nil {
			fmt.Println("Error ingesting iron core data:", err)
		}
	})

	c.Start()

	// 阻塞主线程
	select {}
}

// IngestOilChromatography 推送油色谱数据
func IngestOilChromatography(cfg *config.Config, producer sarama.SyncProducer) error {
	keyInfo, err := utils.GetKeyInfoByKeywords(cfg.DB, []string{"油色谱"}, nil)
	if err != nil {
		return err
	}
	var keys []string
	for _, k := range keyInfo {
		keys = append(keys, k.Key)
	}

	data, err := utils.FetchRealTimeData(cfg, keys)
    // print data
	if err != nil {
		return err
	}

	mergedData := utils.MergeData(keyInfo, data, "key")

	// 发送数据到 Kafka
	for _, msg := range mergedData {
		jsonData, err := json.Marshal(msg)
		if err != nil {
			return err
		}
		message := &sarama.ProducerMessage{
			Topic: cfg.KafkaRealdataTopic,
			Value: sarama.ByteEncoder(jsonData),
		}
		_, _, err = producer.SendMessage(message)
		if err != nil {
			return err
		}
	}
	fmt.Println("油色谱数据推送成功！")
	return nil
}

// IngestPartDischarge 推送局部放电数据
func IngestPartDischarge(cfg *config.Config, producer sarama.SyncProducer) error {
	keyInfo1, err := utils.GetKeyInfoByKeywords(cfg.DB, []string{"局部放电"}, nil)
	if err != nil {
		return err
	}
	keyInfo2, err := utils.GetKeyInfoByKeywords(cfg.DB, []string{"局放"}, nil)
	if err != nil {
		return err
	}
	keyInfoMap := make(map[string]utils.KeyInfo)
	for _, k := range keyInfo1 {
		keyInfoMap[k.Key] = k
	}
	for _, k := range keyInfo2 {
		keyInfoMap[k.Key] = k
	}
	var keyInfo []utils.KeyInfo
	for _, v := range keyInfoMap {
		keyInfo = append(keyInfo, v)
	}

	var keys []string
	for _, k := range keyInfo {
		keys = append(keys, k.Key)
	}

	data, err := utils.FetchRealTimeData(cfg, keys)
	if err != nil {
		return err
	}

	mergedData := utils.MergeData(keyInfo, data, "key")

	// 发送数据到 Kafka
	for _, msg := range mergedData {
		jsonData, err := json.Marshal(msg)
		if err != nil {
			return err
		}
		message := &sarama.ProducerMessage{
			Topic: cfg.KafkaRealdataTopic,
			Value: sarama.ByteEncoder(jsonData),
		}
		_, _, err = producer.SendMessage(message)
		if err != nil {
			return err
		}
	}
	fmt.Println("局部放电数据推送成功！")
	return nil
}

// IngestIronCore 推送铁芯夹件数据
func IngestIronCore(cfg *config.Config, producer sarama.SyncProducer) error {
	keyInfo, err := utils.GetKeyInfoByKeywords(cfg.DB, []string{"接地", "电流"}, nil)
	if err != nil {
		return err
	}
	var keys []string
	for _, k := range keyInfo {
		keys = append(keys, k.Key)
	}

	data, err := utils.FetchRealTimeData(cfg, keys)
	if err != nil {
		return err
	}

	mergedData := utils.MergeData(keyInfo, data, "key")

	// 发送数据到 Kafka
	for _, msg := range mergedData {
		jsonData, err := json.Marshal(msg)
		if err != nil {
			return err
		}
		message := &sarama.ProducerMessage{
			Topic: cfg.KafkaRealdataTopic,
			Value: sarama.ByteEncoder(jsonData),
		}
		_, _, err = producer.SendMessage(message)
		if err != nil {
			return err
		}
	}
	fmt.Println("铁芯夹件数据推送成功！")
	return nil
}
