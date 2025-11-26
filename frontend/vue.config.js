const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    host: "0.0.0.0",
    port: 5173,
    client: {
      webSocketURL: "ws://localhost:5173/ws"
    }
  }
})
