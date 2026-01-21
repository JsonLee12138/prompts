// ============================================
// PM2 配置文件
// 用于后端应用
// ============================================

module.exports = {
  apps: [{
    name: 'app-name',  // 修改为你的应用名称
    script: './dist/main.js',  // 修改为你的入口文件
    instances: 'max',  // 使用所有 CPU 核心
    exec_mode: 'cluster',  // 集群模式
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true,
    max_memory_restart: '1G',  // 内存超过 1G 时重启
    wait_ready: true,
    listen_timeout: 10000,
    kill_timeout: 5000
  }]
};
