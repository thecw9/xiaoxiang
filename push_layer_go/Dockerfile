# 第一阶段：构建阶段
FROM golang:1.23.2 AS builder

# 为了加速构建过程，设置GOPROXY
ENV GOPROXY=https://goproxy.cn,direct

# 设置工作目录
WORKDIR /app

# 将 go.mod 和 go.sum 复制到工作目录
COPY go.mod go.sum ./

# 下载依赖项
RUN go mod download

# 复制项目源代码
COPY . .

# 构建可执行文件
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o your_project .

# 第二阶段：运行阶段
FROM alpine:latest

# 设置时区（可选）
# RUN apk add --no-cache tzdata
# ENV TZ=Asia/Shanghai

# 将可执行文件从构建阶段复制到运行阶段
COPY --from=builder /app/your_project /app/your_project

# 设置工作目录
WORKDIR /app

# 暴露端口（如果您的应用程序需要）
# EXPOSE 8080

# 设置环境变量（根据您的应用程序需要）
# ENV ENVIRONMENT=production

# 运行可执行文件
ENTRYPOINT ["./your_project"]

