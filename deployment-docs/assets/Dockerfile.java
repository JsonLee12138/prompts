# ============================================
# Java Spring Boot 项目 Dockerfile
# ============================================

# Stage 1: Builder - 构建阶段
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# 复制 POM 文件
COPY pom.xml .

# 下载依赖（缓存层）
RUN mvn dependency:go-offline

# 复制源码
COPY src ./src

# 构建 JAR（跳过测试）
RUN mvn clean package -DskipTests

# Stage 2: Runner - 运行阶段
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# 复制构建好的 JAR
COPY --from=builder /app/target/*.jar app.jar

# 创建非 root 用户
RUN addgroup -g 1000 java && \
    adduser -D -u 1000 -G java javauser

USER javauser

# 暴露端口
EXPOSE 8080

# 健康检查（需要 Spring Boot Actuator）
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# 启动命令
ENTRYPOINT ["java", "-jar", "app.jar"]
