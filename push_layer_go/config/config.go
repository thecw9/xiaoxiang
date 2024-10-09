package config

import (
    "database/sql"
    "fmt"
    "os"

    _ "github.com/lib/pq" // PostgreSQL 驱动
)

// Config 包含了项目的配置信息
type Config struct {
    KafkaBootstrapServers string
    KafkaRealdataTopic    string

    PostgresHost     string
    PostgresPort     string
    PostgresDB       string
    PostgresUser     string
    PostgresPassword string
    PostgresURI      string

    Environment string

    DB *sql.DB
}

// NewConfig 从环境变量中读取配置并初始化数据库连接
func NewConfig() (*Config, error) {
    cfg := &Config{
        KafkaBootstrapServers: os.Getenv("KAFKA_BOOTSTRAP_SERVERS"),
        KafkaRealdataTopic:    os.Getenv("KAFKA_REALDATA_TOPIC"),

        PostgresHost:     os.Getenv("DATASOURCE_POSTGRES_HOST"),
        PostgresPort:     os.Getenv("DATASOURCE_POSTGRES_PORT"),
        PostgresDB:       os.Getenv("DATASOURCE_POSTGRES_DB"),
        PostgresUser:     os.Getenv("DATASOURCE_POSTGRES_USER"),
        PostgresPassword: os.Getenv("DATASOURCE_POSTGRES_PASSWORD"),

        Environment: os.Getenv("ENVIRONMENT"),
    }

    cfg.PostgresURI = fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
        cfg.PostgresHost, cfg.PostgresPort, cfg.PostgresUser, cfg.PostgresPassword, cfg.PostgresDB)

    var err error
    cfg.DB, err = sql.Open("postgres", cfg.PostgresURI)
    if err != nil {
        return nil, err
    }

    return cfg, nil
}

