const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/scan',
    createProxyMiddleware({
      target: 'https://future-campaign-410806.uk.r.appspot.com',
      changeOrigin: true,
      secure: false
    })
  );
};